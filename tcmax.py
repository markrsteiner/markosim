import math


def get_igbt_rth_from_time(time, transient_thermal_values):
    num1 = transient_thermal_values['igbt_r1_per_r0_value'] * (
            1.0 - math.exp(-1.0 * time / transient_thermal_values['igbt_t1_per_j1_value']))
    num2 = transient_thermal_values['igbt_r2_per_j0_value'] * (
            1.0 - math.exp(-1.0 * time / transient_thermal_values['igbt_t2_per_t1_value']))
    num3 = transient_thermal_values['igbt_r2_per_j0_value'] * (
            1.0 - math.exp(-1.0 * time / transient_thermal_values['igbt_t3_value']))
    num4 = transient_thermal_values['igbt_r4_per_r1_value'] * (
            1.0 - math.exp(-1.0 * time / transient_thermal_values['igbt_t4_value']))
    rth_from_time = (num1 + num2 + num3 + num4) * transient_thermal_values['rth_tr_value']
    return rth_from_time


def get_fwd_rth_from_time(time, transient_thermal_values):
    num1 = transient_thermal_values['fwd_r1a_per_rd0_value'] * (
            1.0 - math.exp(-1.0 * time / transient_thermal_values['fwd_t1a_per_jd1_value']))
    num2 = transient_thermal_values['fwd_r2a_per_jd0_value'] * (
            1.0 - math.exp(-1.0 * time / transient_thermal_values['fwd_t2a_per_td1_value']))
    num3 = transient_thermal_values['fwd_r3a_per_td0_value'] * (
            1.0 - math.exp(-1.0 * time / transient_thermal_values['fwd_t3_value']))
    num4 = transient_thermal_values['fwd_r4a_per_rd1_value'] * (
            1.0 - math.exp(-1.0 * time / transient_thermal_values['fwd_t4_value']))
    rth_from_time = (num1 + num2 + num3 + num4) * transient_thermal_values['rth_di_value']
    return rth_from_time


def create_thermal_resistance_dict(input_fo, transient_thermal_values):
    igbt_dc_rth = get_igbt_rth_from_time(10.0, transient_thermal_values)
    fwd_dc_rth = get_fwd_rth_from_time(10.0, transient_thermal_values)
    sec_per_cycle_degree = 1.0 / input_fo / 360.0
    time_value = sec_per_cycle_degree / 2.0
    time_step = 0.0

    rth_dict_igbt = [0 for x in range(360)]
    rth_dict_fwd = [0 for x in range(360)]

    while time_value <= 10.0:
        time_step += sec_per_cycle_degree * 360.0
        igbt_trans_rth = get_igbt_rth_from_time(time_step, transient_thermal_values)
        fwd_trans_rth = get_fwd_rth_from_time(time_step, transient_thermal_values)
        for index1 in range(0, 360):
            rth_dict_igbt[index1] += get_igbt_rth_from_time(time_value, transient_thermal_values)
            rth_dict_fwd[index1] += get_fwd_rth_from_time(time_value, transient_thermal_values)
            time_value += sec_per_cycle_degree
        if igbt_trans_rth / igbt_dc_rth >= 0.99 and fwd_trans_rth / fwd_dc_rth >= 0.99:
            break

    results = {}
    results['igbt_thermo'] = rth_dict_igbt
    results['fwd_thermo'] = rth_dict_fwd
    results['time_value'] = time_value
    results['sec_per_cycle_degree'] = sec_per_cycle_degree
    return results


def tj_max_calculation(p_igbt_ave, p_fwd_ave, p_igbt_inst_list, p_fwd_inst_list, input_tc, input_fo,
                       transient_thermal_values):
    thermo_dict = create_thermal_resistance_dict(input_fo, transient_thermal_values)
    time_value = thermo_dict['time_value']
    rth_dict_igbt = thermo_dict['igbt_thermo']
    rth_dict_fwd = thermo_dict['fwd_thermo']
    sec_per_cycle_degree = thermo_dict['sec_per_cycle_degree']
    time_list = []
    rad_list = []
    tj_igbt_list = []
    p_igbt_list = []
    tj_fwd_list = []
    p_fwd_list = []

    for index1 in range(0, 360):
        tj_igbt_inst = input_tc + p_igbt_ave * transient_thermal_values['rth_tr_value'] + \
                       transient_thermal_values['rth_thermal_contact'] * (
                               p_igbt_ave + p_fwd_ave)
        tj_fwd_inst = input_tc + p_fwd_ave * transient_thermal_values['rth_di_value'] + \
                      transient_thermal_values['rth_thermal_contact'] * (
                              p_igbt_ave + p_fwd_ave)

        tj_igbt_inst -= (p_igbt_inst_list[359] - p_igbt_ave) * rth_dict_igbt[
            index1]
        tj_fwd_inst -= (p_fwd_inst_list[359] - p_fwd_ave) * rth_dict_fwd[
            index1]
        rth_dict_igbt[index1] += get_igbt_rth_from_time(time_value, transient_thermal_values)
        rth_dict_fwd[index1] += get_fwd_rth_from_time(time_value, transient_thermal_values)
        tj_igbt_inst += (p_igbt_inst_list[0] - p_igbt_ave) * rth_dict_igbt[
            index1]
        tj_fwd_inst += (p_fwd_inst_list[0] - p_fwd_ave) * rth_dict_fwd[
            index1]
        time_value += sec_per_cycle_degree
        for degree_count in range(1, 360):
            delta_p_igbt = p_igbt_inst_list[degree_count] - p_igbt_inst_list[degree_count - 1]
            delta_p_fwd = p_fwd_inst_list[degree_count] - p_fwd_inst_list[degree_count - 1]
            tj_igbt_inst += delta_p_igbt * rth_dict_igbt[(360 + index1 - degree_count) % 360]
            tj_fwd_inst += delta_p_fwd * rth_dict_fwd[(360 + index1 - degree_count) % 360]

        time_list.append(time_value)
        rad_list.append((index1 + 1))
        tj_igbt_list.append(tj_igbt_inst)
        p_igbt_list.append(p_igbt_inst_list[index1])
        tj_fwd_list.append(tj_fwd_inst)
        p_fwd_list.append(p_fwd_inst_list[index1])

        tj_max_igbt = max(tj_igbt_list)
        tj_max_fwd = max(tj_fwd_list)

    results = {}

    results['time_list'] = time_list
    results['rad_list'] = rad_list
    results['tj_igbt_list'] = tj_igbt_list
    results['p_igbt_list'] = p_igbt_list
    results['tj_fwd_list'] = tj_fwd_list
    results['p_fwd_list'] = p_fwd_list
    results['tj_max_igbt'] = tj_max_igbt
    results['tj_max_fwd'] = tj_max_fwd

    return results
