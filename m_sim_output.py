import numpy as np
import math
import scipy.interpolate as sp

vcc_value = 600.0
rth_tr_value = 0.048
rth_di_value = 0.076
thermal_contact_resistance_value = 0.0115


def array_cleaner(independent_var, dependent_var, start, stop,
                  length):  # could try some sort of log system here but still thinking
    output_dependent_array = []
    output_independent_array = []
    independent_var_list = np.linspace(start, stop, length, endpoint=True)

    dependent_interp = sp.UnivariateSpline(independent_var, dependent_var, k=2)
    for x in range(0, int(length)):
        output_dependent_array.append(independent_var_list[x])
        output_independent_array.append(float(dependent_interp(independent_var_list[x])))

    return output_dependent_array, output_independent_array


def array_shaper(left_array, right_array):
    boat = []
    for x in range(0, len(left_array) - 1):
        boat.append([left_array[x], right_array[x]])
    return boat


def twopeat_array(array1, array2):
    output = []
    output = np.append(output, array1)
    output = np.append(output, array2)
    return output


def threepeat_array(array1, array2, array3):
    output = []
    output = np.append(output, array1)
    output = np.append(output, array2)
    output = np.append(output, array3)
    return output


def vce_from_tj_ic_solver(ic25, vce25, ic125, vce125, ic150, vce150, tj_in, ic_in, max):
    output1, vcesat25 = array_cleaner(ic25, vce25, 0, max, 10)
    output1, vcesat125 = array_cleaner(ic125, vce125, 0, max, 10)
    output1, vcesat150 = array_cleaner(ic150, vce150, 0, max, 10)
    grid_tj = np.mgrid[25:150:10j]
    temp25 = np.full(len(vcesat25), 25.)
    temp125 = np.full(len(vcesat125), 125.)
    temp150 = np.full(len(vcesat150), 150.)
    temp_all = threepeat_array(temp25, temp125, temp150)
    vcesat_all = threepeat_array(vcesat25, vcesat125, vcesat150)
    current_all = threepeat_array(output1, output1, output1)
    grid_z0 = sp.griddata((temp_all, current_all), vcesat_all, (grid_tj, ic_in), method="linear")
    vce_for_temp = sp.UnivariateSpline(grid_tj,
                                       grid_z0)  # if change to linear instead of cubic, can get same results as MelcoSIM
    return vce_for_temp(tj_in)


def esw_solver(ic125, vce125, ic150, vce150, tj_in, ic_in, max):
    output1, vcesat125 = array_cleaner(ic125, vce125, 0, max, 10)
    output1, vcesat150 = array_cleaner(ic150, vce150, 0, max, 10)
    grid_tj = np.mgrid[125:150:10j]
    temp125 = np.full(len(vcesat125), 125.)
    temp150 = np.full(len(vcesat150), 150.)
    temp_all = twopeat_array(temp125, temp150)
    vcesat_all = twopeat_array(vcesat125, vcesat150)
    current_all = twopeat_array(output1, output1)
    grid_z0 = sp.griddata((temp_all, current_all), vcesat_all, (grid_tj, ic_in), method="linear")
    # vce_for_temp = sp.UnivariateSpline(grid_tj, grid_z0)  # if change to linear instead of cubic, can get same results as MelcoSIM
    vce_for_temp = sp.interp1d(grid_tj, grid_z0, kind='linear')
    return vce_for_temp(tj_in)


def esw_rg_fixer(esw_ic_esw, ic_ic_esw, esw_rg_esw, ic):
    baseline = sp.UnivariateSpline(ic_ic_esw, esw_ic_esw)
    for x in range(0, len(esw_rg_esw)):
        esw_rg_esw[x] = esw_rg_esw[x] / float(baseline(ic))
    return esw_rg_esw

def m_sim_output_calc(ic_from_vcesat_125, vcesat_from_vcesat_125,
                      ic_from_vcesat_150, vcesat_from_vcesat_150,
                      ie_from_vecsat_125, vecsat_from_vecsat_125,
                      ie_from_vecsat_150, vecsat_from_vecsat_150,
                      ic_from_e_sw_on_125, e_sw_on_from_e_sw_on_125,
                      ic_from_e_sw_on_150, e_sw_on_from_e_sw_on_150,
                      ic_from_e_sw_off_125, e_sw_off_from_e_sw_off_125,
                      ic_from_e_sw_off_150, e_sw_off_from_e_sw_off_150,
                      ic_from_e_rr_125, e_rr_from_e_rr_125,
                      ic_from_e_rr_150, e_rr_from_e_rr_150,
                      e_rg_from_e_on_125, e_on_from_e_on_125,
                      e_rg_from_e_on_150, e_on_from_e_on_150,
                      e_rg_from_e_off_125, e_off_from_e_off_125,
                      e_rg_from_e_off_150, e_off_from_e_off_150,
                      e_rg_from_e_rg_125, e_rr_from_e_rg_125, 
                      e_rg_from_e_rg_150, e_rr_from_e_rg_150,
                      input_bus_voltage,
                      input_ic_arms,
                      power_factor,
                      mod_depth,
                      freq_carrier,
                      freq_output,
                      input_tc,
                      input_rg_on,
                      input_rg_off)

    p_fwd_cond = []
    e_sw_rr = []
    p_igbt = []
    p_fwd = []
    p_arm = []
    delta_tj__igbt = []
    delta_tj__fwd = []
    delta_tc = []
    tj_try_igbt = 125
    tj_try_fwd = 125
    tj_igbt = 0
    tj_fwd = 0

    power_factor_phi = math.acos(power_factor) * 180 / math.pi
    step = 1
    degree_count = 1.0

    initflag = True

    p_igbt_cond = []
    e_sw_on = []
    e_sw_off = []
    e_sw_on_e_off = []
    p_fwd_cond = []
    e_sw_err = []
    p_igbt = []
    p_fwd = []
    p_arm = []
    degree_count = 1

    output_current_tot = []
    output_voltage_tot = []

    time_division = 1.0 / freq_output / 360.0 * 1000.0 * 1000.0 * step
    switches_per_cycle_per_degree = freq_carrier / freq_output / 360.0 * 1000 * step

    tj_try_igbt = 125
    tj_try_fwd = 125

    while degree_count <= 360.0:
        duty_cycle = []
        output_voltage = []
        rad_delta = (degree_count - step / 2)
        duty_cycle.append((1.0 + mod_depth * math.sin(rad_delta / 180.0 * math.pi)) / 2.0)
        duty_cycle.append(1.0 - duty_cycle[0])
        duty_cycle.append((1.0 + mod_depth * math.sin((rad_delta - 120.0) / 180.0 * math.pi)) / 2.0)
        output_voltage.append(duty_cycle[0] * input_bus_voltage)
        output_voltage.append(duty_cycle[2] * input_bus_voltage)
        if duty_cycle[0] == 0.0 and duty_cycle[1] > 0.0:
            output_voltage[0] += (1.0 - duty_cycle[1]) * input_bus_voltage
        elif duty_cycle[0] == 0.0 and duty_cycle[1] == 0.0:
            output_voltage[0] += (output_voltage[1] + output_voltage[2]) / 2.0

        output_current = input_ic_arms * math.sin((rad_delta - power_factor_phi) / 180 * math.pi)
        igbt_current = diode_current = 0.0
        if output_current > 0.0:
            igbt_current = output_current
        else:
            diode_current = -output_current

        if igbt_current >= 0.0:
            vce_sat_curve = sp.interp1d(ic_from_vcesat_125, vcesat_from_vcesat_125, kind='linear')
            vce_at_ic = vce_sat_curve(igbt_current)
            igbt_p_vce = igbt_current * time_division * vce_at_ic * output_voltage[0] / input_bus_voltage / 1000.0
            
            e_sw_on_at_ic_curve = sp.interp1d(ic_from_e_sw_on_125, e_sw_on_from_e_sw_on_125)
            e_sw_on_at_ic = e_sw_on_at_ic_curve(igbt_current)
            
            e_sw_off_at_ic_curve = sp.interp1d(ic_from_e_sw_off_125, e_sw_off_from_e_sw_off_125, kind='linear')
            e_sw_off_at_ic = e_sw_off_at_ic_curve(igbt_current)
            if 1.0 > output_voltage[0] / input_bus_voltage > 0.0:
                igbt_e_sw_on_fco_ratio = switches_per_cycle_per_degree * e_sw_on_at_ic
                igbt_e_sw_off_fco_ratio = switches_per_cycle_per_degree * e_sw_off_at_ic
        if diode_current >= 0.0:
            vec_at_ic_curve = sp.interp1d(ie_from_vecsat_125, vecsat_from_vecsat_125)
            vec_at_ic = vec_at_ic_curve(diode_current)
            fwd_p_vce = diode_current * time_division * vec_at_ic * output_voltage[0] / input_bus_voltage / 1000.0
            err_from_ic_curve = sp.interp1d(ic_from_e_rr_125, e_rr_from_e_rr_125)
            err_from_ic = err_from_ic_curve(diode_current)
        if 1.0 > output_voltage[0] / input_bus_voltage > 0.0:
            fwd_e_rr_fco_ratio = switches_per_cycle_per_degree * err_from_ic

        vcc_ratio = input_bus_voltage / vcc_value

        e_sw_on_from_rg_e_sw_on_curve = sp.interp1d(e_rg_from_e_on_125, e_on_from_e_on_125)
        e_sw_on_from_rg_e_sw_on = e_sw_on_from_rg_e_sw_on_curve(input_rg_on)

        e_sw_off_from_rg_e_sw_off_curve = sp.interp1d(e_rg_from_e_off_125, e_off_from_e_off_125)
        e_sw_off_from_rg_e_sw_off = e_sw_off_from_rg_e_sw_off_curve(input_rg_off)

        errFromRgErrcurve = sp.interp1d(e_rg_from_e_rg_125, e_rr_from_e_rg_125)
        errFromRgErr = errFromRgErrcurve(input_rg_off)

        output_current_tot.append(output_current)
        output_voltage_tot.append(output_voltage[0])

        p_igbt_cond.append(igbt_p_vce * freq_output / 1000.0)
        e_sw_on.append(igbt_e_sw_on_fco_ratio * freq_output / 1000.0 * vcc_ratio * e_sw_on_from_rg_e_sw_on)
        e_sw_off.append(igbt_e_sw_on * freq_output / 1000.0 * vcc_ratio * e_sw_off_from_rg_e_sw_off)
        e_sw_on_Eoff.append((igbt_e_sw_on_fco_ratio * vcc_ratio * e_sw_on_from_rg_e_sw_on + igbt_e_sw_off_fco_ratio * vcc_ratio * e_sw_off_from_rg_e_sw_off) * freq_output / 1000.0)
        p_fwd_cond.append(fwd_p_vce * freq_output / 1000.0)
        e_sw_err.append(fwd_e_rr_fco_ratio * freq_output / 1000.0 * vcc_ratio * errFromRgErr)
        p_igbt.append((igbt_e_sw_on_fco_ratio * vcc_ratio * e_sw_on_from_rg_e_sw_on + igbt_e_sw_off_fco_ratio * vcc_ratio * e_sw_off_from_rg_e_sw_off) * freq_output / 1000.0 + igbt_p_vce * freq_output / 1000.0)
        p_fwd.append(fwd_e_rr_fco_ratio * errFromRgErr * freq_output / 1000.0 * vcc_ratio + fwd_p_vce * freq_output / 1000.0)
        # p_arm.append((igbt_e_sw_on_fco_ratio * vcc_ratio * e_sw_on_from_rg_e_sw_on + igbt_e_sw_off_fco_ratio * vcc_ratio * e_sw_off_from_rg_e_sw_off) * freq_output / 1000.0 + igbt_p_vce * freq_output / 1000.0 + (
        #         fwd_e_rr_fco_ratio * errFromRgErr * freq_output / 1000.0 * vcc_ratio + fwd_p_vce * freq_output / 1000.0))

        degree_count += step

    delta_tj__igbt = np.sum(p_igbt) * rth_tr_value
    delta_tj__fwd = np.sum(p_fwd) * rth_di_value
    delta_tc = np.sum(p_arm) * thermal_contact_resistance_value
    tj_igbt = delta_tj__igbt + delta_tc + input_tc
    tj_fwd = delta_tj__fwd + delta_tc + input_tc


    # while loop end
    p_igbt_cond_total = np.sum(p_igbt_cond)
    e_sw_on_total = np.sum(e_sw_on)
    e_sw_off_total = np.sum(e_sw_off)
    p_igbt_total = np.sum(p_igbt)
    p_fwd_cond_total = np.sum(p_fwd_cond)
    e_sw_err_total = np.sum(e_sw_err)
