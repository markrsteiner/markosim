import numpy as np
import math
import sim_tools
import tcmax


def mark_sim_output_calc(file_values, input_file_values):
    tj_test = float(input_file_values['tj_test'])
    input_bus_voltage = float(input_file_values['input_bus_voltage'])
    input_ic_arms = float(input_file_values['input_ic_arms'])
    power_factor = float(input_file_values['power_factor'])
    mod_depth = float(input_file_values['mod_depth'])
    freq_carrier = float(input_file_values['freq_carrier'])
    freq_output = float(input_file_values['freq_output'])
    input_tc = float(input_file_values['input_tc'])
    input_rg_on = float(input_file_values['input_rg_on'])
    input_rg_off = float(input_file_values['input_rg_off'])

    ic_from_vcesat_25 = file_values['ic_from_vcesat_25']
    vcesat_from_vcesat_25 = file_values['vcesat_from_vcesat_25']
    ie_from_vecsat_25 = file_values['ie_from_vecsat_25']
    vecsat_from_vecsat_25 = file_values['vecsat_from_vecsat_25']
    ic_from_vcesat_125 = file_values['ic_from_vcesat_125']
    vcesat_from_vcesat_125 = file_values['vcesat_from_vcesat_125']
    ic_from_vcesat_150 = file_values['ic_from_vcesat_150']
    vcesat_from_vcesat_150 = file_values['vcesat_from_vcesat_150']
    ie_from_vecsat_125 = file_values['ie_from_vecsat_125']
    vecsat_from_vecsat_125 = file_values['vecsat_from_vecsat_125']
    ie_from_vecsat_150 = file_values['ie_from_vecsat_150']
    vecsat_from_vecsat_150 = file_values['vecsat_from_vecsat_150']
    ic_from_e_sw_on_125 = file_values['ic_from_e_sw_on_125']
    e_sw_on_from_e_sw_on_125 = file_values['e_sw_on_from_e_sw_on_125']
    ic_from_e_sw_on_150 = file_values['ic_from_e_sw_on_150']
    e_sw_on_from_e_sw_on_150 = file_values['e_sw_on_from_e_sw_on_150']
    ic_from_e_sw_off_125 = file_values['ic_from_e_sw_off_125']
    e_sw_off_from_e_sw_off_125 = file_values['e_sw_off_from_e_sw_off_125']
    ic_from_e_sw_off_150 = file_values['ic_from_e_sw_off_150']
    e_sw_off_from_e_sw_off_150 = file_values['e_sw_off_from_e_sw_off_150']
    ic_from_e_rr_125 = file_values['ic_from_e_rr_125']
    e_rr_from_e_rr_125 = file_values['e_rr_from_e_rr_125']
    ic_from_e_rr_150 = file_values['ic_from_e_rr_150']
    e_rr_from_e_rr_150 = file_values['e_rr_from_e_rr_150']
    e_rg_from_e_on_125 = file_values['e_rg_from_e_on_125']
    e_on_from_e_on_125 = file_values['e_on_from_e_on_125']
    e_rg_from_e_on_150 = file_values['e_rg_from_e_on_150']
    e_on_from_e_on_150 = file_values['e_on_from_e_on_150']
    e_rg_from_e_off_125 = file_values['e_rg_from_e_off_125']
    e_off_from_e_off_125 = file_values['e_off_from_e_off_125']
    e_rg_from_e_off_150 = file_values['e_rg_from_e_off_150']
    e_off_from_e_off_150 = file_values['e_off_from_e_off_150']
    e_rg_from_e_rg_125 = file_values['e_rg_from_e_rg_125']
    e_rr_from_e_rg_125 = file_values['e_rr_from_e_rg_125']
    e_rg_from_e_rg_150 = file_values['e_rg_from_e_rg_150']
    e_rr_from_e_rg_150 = file_values['e_rr_from_e_rg_150']

    tj_try_igbt = tj_test
    tj_try_fwd = tj_test

    power_factor_phi = math.acos(power_factor) * 180 / math.pi
    step = 1

    ic_from_e_sw_on_125 = sim_tools.origin_checker(ic_from_e_sw_on_125)
    e_sw_on_from_e_sw_on_125 = sim_tools.origin_checker(e_sw_on_from_e_sw_on_125)
    ic_from_e_sw_on_150 = sim_tools.origin_checker(ic_from_e_sw_on_150)
    e_sw_on_from_e_sw_on_150 = sim_tools.origin_checker(e_sw_on_from_e_sw_on_150)
    ic_from_e_sw_off_125 = sim_tools.origin_checker(ic_from_e_sw_off_125)
    e_sw_off_from_e_sw_off_125 = sim_tools.origin_checker(e_sw_off_from_e_sw_off_125)
    ic_from_e_sw_off_150 = sim_tools.origin_checker(ic_from_e_sw_off_150)
    e_sw_off_from_e_sw_off_150 = sim_tools.origin_checker(e_sw_off_from_e_sw_off_150)
    ic_from_e_rr_125 = sim_tools.origin_checker(ic_from_e_rr_125)
    e_rr_from_e_rr_125 = sim_tools.origin_checker(e_rr_from_e_rr_125)
    ic_from_e_rr_150 = sim_tools.origin_checker(ic_from_e_rr_150)
    e_rr_from_e_rr_150 = sim_tools.origin_checker(e_rr_from_e_rr_150)

    initflag = True
    tj_igbt = 0
    tj_igbt_check = []

    while (abs(tj_try_igbt - tj_igbt) > 0.1):
        p_igbt_cond = []
        e_sw_on = []
        e_sw_off = []
        e_sw_on_Eoff = []
        p_fwd_cond = []
        p_total_igbt = []
        p_total_fwd = []
        e_sw_err = []
        p_igbt = []
        p_fwd = []
        p_arm = []
        degree_count = 1

        output_current_tot = []
        output_voltage_tot = []

        time_division = 1.0 / freq_output / 360.0 * 1000.0 * 1000.0 * step
        switches_per_cycle_per_degree = freq_carrier / freq_output / 360.0 * 1000 * step
        if initflag:
            tj_try_igbt = tj_test
            tj_try_fwd = tj_test
        else:
            tj_try_igbt = tj_igbt
            tj_try_fwd = tj_fwd
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
                VceAtIc = float(
                    sim_tools.vce_from_tj_ic_solver(ic_from_vcesat_25, vcesat_from_vcesat_25, ic_from_vcesat_125,
                                                    vcesat_from_vcesat_125,
                                                    ic_from_vcesat_150, vcesat_from_vcesat_150, tj_try_igbt,
                                                    igbt_current,
                                                    2400))
                igbt_p_vce = igbt_current * time_division * VceAtIc * output_voltage[0] / input_bus_voltage / 1000.0
                ESwOn = sim_tools.esw_solver(ic_from_e_sw_on_125, e_sw_on_from_e_sw_on_125, ic_from_e_sw_on_150,
                                             e_sw_on_from_e_sw_on_150,
                                             tj_try_igbt, igbt_current, 2400)
                ESwOff = sim_tools.esw_solver(ic_from_e_sw_off_125, e_sw_off_from_e_sw_off_125, ic_from_e_sw_off_150,
                                              e_sw_off_from_e_sw_off_150, tj_try_igbt, igbt_current, 2400)
                if 1.0 > output_voltage[0] / input_bus_voltage > 0.0:
                    igbt_e_sw_on_fco_ratio = switches_per_cycle_per_degree * ESwOn
                    igbt_e_sw_off_fco_ratio = switches_per_cycle_per_degree * ESwOff
            if diode_current >= 0.0:
                VfAtIc = sim_tools.vce_from_tj_ic_solver(ie_from_vecsat_25, vecsat_from_vecsat_25, ie_from_vecsat_125,
                                                         vecsat_from_vecsat_125, ie_from_vecsat_150,
                                                         vecsat_from_vecsat_150,
                                                         tj_try_fwd,
                                                         diode_current, 2400)

                fwd_p_vce = diode_current * time_division * VfAtIc * output_voltage[0] / input_bus_voltage / 1000.0
                ErrFromIc = sim_tools.esw_solver(ic_from_e_rr_125, e_rr_from_e_rr_125, ic_from_e_rr_150,
                                                 e_rr_from_e_rr_150,
                                                 tj_try_fwd,
                                                 diode_current, 2400)

            if 1.0 > output_voltage[0] / input_bus_voltage > 0.0:
                fwd_e_rr_fco_ratio = switches_per_cycle_per_degree * ErrFromIc

            vcc_ratio = input_bus_voltage / file_values['vcc_value']

            e_sw_on_from_rg_e_sw_on = sim_tools.esw_solver(e_rg_from_e_on_125, e_on_from_e_on_125, e_rg_from_e_on_150,
                                                    e_on_from_e_on_150,
                                                    tj_try_igbt, input_rg_on, 10)

            e_sw_off_from_rg_e_sw_off = sim_tools.esw_solver(e_rg_from_e_off_125, e_off_from_e_off_125,
                                                             e_rg_from_e_off_150,
                                                             e_off_from_e_off_150, tj_try_igbt, input_rg_off, 10)

            errFromRgErr = sim_tools.esw_solver(e_rg_from_e_rg_125, e_rr_from_e_rg_125, e_rg_from_e_rg_150,
                                                e_rr_from_e_rg_150,
                                                tj_try_fwd, input_rg_on, 10)

            output_current_tot.append(output_current)
            output_voltage_tot.append(output_voltage[0])

            p_igbt_cond.append(igbt_p_vce * freq_output / 1000.0)
            e_sw_on.append(igbt_e_sw_on_fco_ratio * freq_output / 1000.0 * vcc_ratio * e_sw_on_from_rg_e_sw_on)
            e_sw_off.append(igbt_e_sw_off_fco_ratio * freq_output / 1000.0 * vcc_ratio * e_sw_off_from_rg_e_sw_off)
            e_sw_on_Eoff.append((
                                        igbt_e_sw_on_fco_ratio * vcc_ratio * e_sw_on_from_rg_e_sw_on + igbt_e_sw_off_fco_ratio * vcc_ratio * e_sw_off_from_rg_e_sw_off) * freq_output / 1000.0)
            p_fwd_cond.append(fwd_p_vce * freq_output / 1000.0)
            e_sw_err.append(fwd_e_rr_fco_ratio * freq_output / 1000.0 * vcc_ratio * errFromRgErr)
            p_igbt.append((
                                  igbt_e_sw_on_fco_ratio * vcc_ratio * e_sw_on_from_rg_e_sw_on + igbt_e_sw_off_fco_ratio * vcc_ratio * e_sw_off_from_rg_e_sw_off) * freq_output / 1000.0 + igbt_p_vce * freq_output / 1000.0)
            p_fwd.append(
                fwd_e_rr_fco_ratio * errFromRgErr * freq_output / 1000.0 * vcc_ratio + fwd_p_vce * freq_output / 1000.0)
            p_total_igbt.append((igbt_p_vce + (
                    igbt_e_sw_on_fco_ratio * e_sw_on_from_rg_e_sw_on + igbt_e_sw_off_fco_ratio * e_sw_off_from_rg_e_sw_off) * vcc_ratio) / time_division * 1000)
            p_total_fwd.append((fwd_p_vce + fwd_e_rr_fco_ratio * errFromRgErr * vcc_ratio) / time_division * 1000)
            p_arm.append((
                                 igbt_e_sw_on_fco_ratio * vcc_ratio * e_sw_on_from_rg_e_sw_on + igbt_e_sw_off_fco_ratio * vcc_ratio * e_sw_off_from_rg_e_sw_off) * freq_output / 1000.0 + igbt_p_vce * freq_output / 1000.0 + (
                                 fwd_e_rr_fco_ratio * errFromRgErr * freq_output / 1000.0 * vcc_ratio + fwd_p_vce * freq_output / 1000.0))

            degree_count += step

        delta_tj__igbt = np.sum(p_igbt) * file_values['rth_tr_value']
        delta_tj__fwd = np.sum(p_fwd) * file_values['rth_di_value']
        delta_tc = np.sum(p_arm) * file_values['rth_thermal_contact'] + input_tc
        tj_igbt = delta_tj__igbt + delta_tc
        tj_fwd = delta_tj__fwd + delta_tc

        initflag = False
        tj_igbt_check.append(tj_igbt)


    p_igbt_cond_total = np.sum(p_igbt_cond)
    e_sw_on_total = np.sum(e_sw_on)
    e_sw_off_total = np.sum(e_sw_off)
    e_sw_total = e_sw_on_total + e_sw_off_total
    p_igbt_total = np.sum(p_igbt)
    p_fwd_total = np.sum(p_fwd)
    p_arm_total = np.sum(p_arm)
    p_fwd_cond_total = np.sum(p_fwd_cond)
    e_sw_err_total = np.sum(e_sw_err)

    p_igbt_tcmax = sim_tools.doublearray_maker(p_total_igbt)
    p_fwd_tcmax = sim_tools.doublearray_maker(p_total_fwd)

    tc_max_results = tcmax.tj_max_calculation(p_igbt_total, p_fwd_total, p_igbt_tcmax, p_fwd_tcmax, input_tc, freq_output, tj_igbt, tj_fwd, file_values)

    tj_max_igbt = tc_max_results['tj_max_igbt']
    delta_tj_max_igbt = tj_max_igbt - delta_tc
    tj_max_fwd = tc_max_results['tj_max_fwd']
    delta_tj_max_fwd = tj_max_fwd - delta_tc

    results = {}

    results['P_total_IGBT'] = p_igbt_total
    results['P_cond_IGBT'] = p_igbt_cond_total
    results['E_sw_IGBT'] = e_sw_total
    results['E_sw_on_IGBT'] = e_sw_on_total
    results['E_sw_off_IGBT'] = e_sw_off_total
    results['delta_Tj_Ave_IGBT'] = delta_tj__igbt
    results['Tj_Ave_IGBT'] = tj_igbt
    results['delta_Tj_Max_IGBT'] = delta_tj_max_igbt
    results['Tj_max_IGBT'] = tj_max_igbt
    results['Tc_Ave'] = delta_tc
    results['P_total_FWD'] = p_fwd_total
    results['P_cond_FWD'] = p_fwd_cond_total
    results['E_rr_FWD'] = e_sw_err_total
    results['delta_Tj_Ave_FWD'] = delta_tj__fwd
    results['Tj_Ave_FWD'] = tj_fwd
    results['delta_Tj_Max_FWD'] = delta_tj_max_fwd
    results['Tj_Max_FWD'] = tj_max_fwd
    results['P_arm'] = p_arm_total

    print(results)
    return results
