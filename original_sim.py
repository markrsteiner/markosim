import numpy as np
import scipy as sp
import math
import sim_tools
import tcmax


def m_sim_output_calc(file_values, input_file_values):
    # ins = sim_tools.InputFile(input_file_values)
    # refs = sim_tools.InputFile(file_values)

    input_bus_voltage = float(input_file_values['Vcc [V]'])
    input_ic_peak = float(input_file_values['Io [Apk]'])
    power_factor = float(input_file_values['PF [cos(\u03D5)]'])
    mod_depth = float(input_file_values['Mod. Depth'])
    freq_carrier = float(input_file_values['fc [kHz]'])
    freq_output = float(input_file_values['fo [Hz]'])
    input_tc = float(input_file_values['Ts [\u00B0C]'])
    input_rg_on = float(input_file_values['rg on [\u03A9]'])
    input_rg_off = float(input_file_values['rg off [\u03A9]'])

    ic_from_vcesat_125 = file_values['ic_from_vcesat_125']
    vcesat_from_vcesat_125 = file_values['vcesat_from_vcesat_125']
    ie_from_vecsat_125 = file_values['ie_from_vecsat_125']
    vecsat_from_vecsat_125 = file_values['vecsat_from_vecsat_125']
    ic_from_e_sw_on_125 = file_values['ic_from_e_sw_on_125']
    e_sw_on_from_e_sw_on_125 = file_values['e_sw_on_from_e_sw_on_125']
    ic_from_e_sw_off_125 = file_values['ic_from_e_sw_off_125']
    e_sw_off_from_e_sw_off_125 = file_values['e_sw_off_from_e_sw_off_125']
    ic_from_e_rr_125 = file_values['ic_from_e_rr_125']
    e_rr_from_e_rr_125 = file_values['e_rr_from_e_rr_125']
    e_rg_from_e_on_125 = file_values['e_rg_from_e_on_125']
    e_on_from_e_on_125 = file_values['e_on_from_e_on_125']
    e_rg_from_e_off_125 = file_values['e_rg_from_e_off_125']
    e_off_from_e_off_125 = file_values['e_off_from_e_off_125']
    e_rg_from_e_rg_125 = file_values['e_rg_from_e_rg_125']
    e_rr_from_e_rg_125 = file_values['e_rr_from_e_rg_125']

    ic_from_vcesat = ic_from_vcesat_125
    vcesat_from_vcesat = vcesat_from_vcesat_125
    ie_from_vecsat = ie_from_vecsat_125
    vecsat_from_vecsat = vecsat_from_vecsat_125
    ic_from_e_sw_on = ic_from_e_sw_on_125
    e_sw_on_from_e_sw_on = e_sw_on_from_e_sw_on_125
    ic_from_e_sw_off = ic_from_e_sw_off_125
    e_sw_off_from_e_sw_off = e_sw_off_from_e_sw_off_125
    ic_from_e_rr = ic_from_e_rr_125
    e_rr_from_e_rr = e_rr_from_e_rr_125
    e_rg_from_e_on = e_rg_from_e_on_125
    e_on_from_e_on = e_on_from_e_on_125
    e_rg_from_e_off = e_rg_from_e_off_125
    e_off_from_e_off = e_off_from_e_off_125
    e_rg_from_e_rg = e_rg_from_e_rg_125
    e_rr_from_e_rg = e_rr_from_e_rg_125

    ic_from_e_sw_on = sim_tools.origin_checker(ic_from_e_sw_on)
    e_sw_on_from_e_sw_on = sim_tools.origin_checker(e_sw_on_from_e_sw_on)
    ic_from_e_sw_off = sim_tools.origin_checker(ic_from_e_sw_off)
    e_sw_off_from_e_sw_off = sim_tools.origin_checker(e_sw_off_from_e_sw_off)
    ic_from_e_rr = sim_tools.origin_checker(ic_from_e_rr)
    e_rr_from_e_rr = sim_tools.origin_checker(e_rr_from_e_rr)

    power_factor_phi = math.acos(power_factor) * 180 / math.pi
    step = int(1)

    e_sw_fco = []
    p_igbt_cond = []
    e_sw_on = []
    e_sw_off = []
    e_sw_igbt = []
    p_fwd_cond = []
    e_sw_err = []
    p_igbt = []
    p_fwd = []
    p_arm = []
    p_total_igbt = []
    p_total_fwd = []

    output_current_tot = []
    output_voltage_tot = []

    time_division = 1.0 / freq_output / 360.0 * 1000.0 * 1000.0 * step
    switches_per_cycle_per_degree = freq_carrier / freq_output / 360.0 * 1000 * step * 1.0

    for degree_count in range(1, 1 + int(360 / step)):
        duty_cycle = []
        output_voltage = []
        rad_delta = (degree_count * step - step / 2)
        duty_cycle.append((1.0 + mod_depth * math.sin(rad_delta / 180.0 * math.pi)) / 2.0)
        duty_cycle.append(1.0 - duty_cycle[0])
        duty_cycle.append((1.0 + mod_depth * math.sin((rad_delta - 120.0) / 180.0 * math.pi)) / 2.0)
        output_voltage.append(duty_cycle[0] * input_bus_voltage)
        output_voltage.append(duty_cycle[2] * input_bus_voltage)
        if duty_cycle[0] == 0.0 and duty_cycle[1] > 0.0:
            output_voltage[0] += (1.0 - duty_cycle[1]) * input_bus_voltage
        elif duty_cycle[0] == 0.0 and duty_cycle[1] == 0.0:
            output_voltage[0] += (output_voltage[1] + output_voltage[2]) / 2.0

        output_current = input_ic_peak * math.sin((rad_delta - power_factor_phi) / 180 * math.pi)
        igbt_current = diode_current = 0.0
        if output_current > 0.0:
            igbt_current = output_current
        else:
            diode_current = -output_current

        if igbt_current >= 0.0:
            # vce_at_ic = np.interp(igbt_current, ic_from_vcesat, vcesat_from_vcesat)
            icvce = sp.interpolate.interp1d(ic_from_vcesat, vcesat_from_vcesat, fill_value='extrapolate')
            vce_at_ic = icvce(igbt_current)

            igbt_p_vce = igbt_current * time_division * vce_at_ic * output_voltage[0] / input_bus_voltage / 1000.0

            # e_sw_on_at_ic = np.interp(igbt_current, ic_from_e_sw_on, e_sw_on_from_e_sw_on)
            iceswon = sp.interpolate.interp1d(ic_from_e_sw_on, e_sw_on_from_e_sw_on, fill_value='extrapolate')
            e_sw_on_at_ic = iceswon(igbt_current)
            # e_sw_off_at_ic = np.interp(igbt_current, ic_from_e_sw_off, e_sw_off_from_e_sw_off)
            iceswoff = sp.interpolate.interp1d(ic_from_e_sw_off, e_sw_off_from_e_sw_off, fill_value='extrapolate')
            e_sw_off_at_ic = iceswoff(igbt_current)
            if 1.0 > output_voltage[0] / input_bus_voltage > 0.0:
                igbt_e_sw_on_fco_ratio = switches_per_cycle_per_degree * e_sw_on_at_ic
                igbt_e_sw_off_fco_ratio = switches_per_cycle_per_degree * e_sw_off_at_ic
        if diode_current >= 0.0:
            # vec_at_ic = np.interp(diode_current, ie_from_vecsat, vecsat_from_vecsat)
            ievec = sp.interpolate.interp1d(ie_from_vecsat, vecsat_from_vecsat, fill_value='extrapolate')
            vec_at_ic = ievec(diode_current)
            fwd_p_vce = diode_current * time_division * vec_at_ic * output_voltage[0] / input_bus_voltage / 1000.0
            # err_from_ic = np.interp(diode_current, ic_from_e_rr, e_rr_from_e_rr)
            icerr = sp.interpolate.interp1d(ic_from_e_rr, e_rr_from_e_rr, fill_value='extrapolate')
            err_from_ic = icerr(diode_current)
        if 1.0 > output_voltage[0] / input_bus_voltage > 0.0:
            fwd_e_rr_fco_ratio = switches_per_cycle_per_degree * err_from_ic

        vcc_ratio = input_bus_voltage / file_values['vcc_value']

        e_sw_on_from_rg_e_sw_on = np.interp(input_rg_on, e_rg_from_e_on, e_on_from_e_on)

        e_sw_off_from_rg_e_sw_off = np.interp(input_rg_off, e_rg_from_e_off, e_off_from_e_off)

        errFromRgErr = np.interp(input_rg_on, e_rg_from_e_rg, e_rr_from_e_rg)

        output_current_tot.append(output_current)
        output_voltage_tot.append(output_voltage[0])

        p_igbt_cond.append(igbt_p_vce * freq_output / 1000.0)
        e_sw_on.append(igbt_e_sw_on_fco_ratio * freq_output / 1000.0 * vcc_ratio * e_sw_on_from_rg_e_sw_on)
        e_sw_off.append(igbt_e_sw_off_fco_ratio * freq_output / 1000.0 * vcc_ratio * e_sw_off_from_rg_e_sw_off)
        e_sw_fco.append(igbt_e_sw_off_fco_ratio)
        e_sw_igbt.append((
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
        p_arm.append(p_igbt[degree_count - 1] + p_fwd[degree_count - 1])
        degree_count += step

    delta_tj__igbt = np.sum(p_igbt) * file_values['rth_tr_value']
    delta_tj__fwd = np.sum(p_fwd) * file_values['rth_di_value']
    delta_tc = np.sum(p_arm) * file_values['rth_thermal_contact'] + input_tc
    tj_igbt = delta_tj__igbt + delta_tc
    tj_fwd = delta_tj__fwd + delta_tc

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

    tc_max_results = tcmax.tj_max_calculation(p_igbt_total, p_fwd_total, p_igbt_tcmax, p_fwd_tcmax, input_tc,
                                              freq_output, tj_igbt, tj_fwd,
                                              file_values, step)

    tj_max_igbt = tc_max_results['tj_max_igbt']
    delta_tj_max_igbt = tj_max_igbt - delta_tc
    tj_max_fwd = tc_max_results['tj_max_fwd']
    delta_tj_max_fwd = tj_max_fwd - delta_tc

    results = {}

    results['P Total IGBT [W]'] = p_igbt_total
    results['P Cond IGBT [W]'] = p_igbt_cond_total
    results['Psw IGBT [W]'] = e_sw_total
    results['Psw,on IGBT [W]'] = e_sw_on_total
    results['Psw,off IGBT [W]'] = e_sw_off_total
    results['ΔT\u2C7C ave. IGBT [K]'] = delta_tj__igbt
    results['T\u2C7C ave. IGBT [\u00B0C]'] = tj_igbt
    results['ΔT\u2C7C Max_IGBT [K]'] = delta_tj_max_igbt
    results['T\u2C7C Max IGBT [\u00B0C]'] = tj_max_igbt
    results['Tc ave. [\u00B0C]'] = delta_tc
    results['P Total FWD [W]'] = p_fwd_total
    results['P Cond FWD [W]'] = p_fwd_cond_total
    results['Prr FWD [W]'] = e_sw_err_total
    results['ΔT\u2C7C Ave FWD [K]'] = delta_tj__fwd
    results['T\u2C7C Ave FWD [\u00B0C]'] = tj_fwd
    results['ΔT\u2C7C Max FWD [K]'] = delta_tj_max_fwd
    results['T\u2C7C Max FWD [\u00B0C]'] = tj_max_fwd
    results['P Arm [W]'] = p_arm_total

    results['Vcc [V]'] = input_bus_voltage
    results['Io [Apk]'] = input_ic_peak
    results['PF [cos(\u03D5)]'] = power_factor
    results['Mod. Depth'] = mod_depth
    results['fc [kHz]'] = freq_carrier
    results['fo [Hz]'] = freq_output
    results['rg on [\u03A9]'] = input_rg_on
    results['rg off [\u03A9]'] = input_rg_off
    results['Ts [\u00B0C]'] = input_tc

    return results
