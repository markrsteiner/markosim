import math
import numpy as np


def get_fwd_rth_from_time(time, transient_thermal_values, flag):
    if transient_thermal_values['fwd_t3_value'] > 0:
        num1 = transient_thermal_values['fwd_r1a_per_rd0_value'] * (
                1.0 - math.exp(-1.0 * time / transient_thermal_values['fwd_t1a_per_jd1_value']))
        num2 = transient_thermal_values['fwd_r2a_per_jd0_value'] * (
                1.0 - math.exp(-1.0 * time / transient_thermal_values['fwd_t2a_per_td1_value']))
        num3 = transient_thermal_values['fwd_r3a_per_td0_value'] * (1.0 - math.exp(-1.0 * time / transient_thermal_values['fwd_t3_value']))
        num4 = transient_thermal_values['fwd_r4a_per_rd1_value'] * (1.0 - math.exp(-1.0 * time / transient_thermal_values['fwd_t4_value']))
        rth_from_time = (num1 + num2 + num3 + num4) * transient_thermal_values['rth_di_value']
    else:
        num1 = (1 - math.exp(-1 * pow(time, (transient_thermal_values['fwd_r2a_per_jd0_value'] / transient_thermal_values['fwd_r3a_per_td0_value']))))
        num1 = num1 * transient_thermal_values['fwd_r1a_per_rd0_value']
        num2 = (1 - math.exp(-1 * pow(time, (transient_thermal_values['fwd_t1a_per_jd1_value'] / transient_thermal_values['fwd_t2a_per_td1_value']))))
        num2 = num2 * transient_thermal_values['fwd_r4a_per_rd1_value']
        rth_from_time = (num1 + num2) * transient_thermal_values['rth_di_value']
    return rth_from_time


def rth_integral_two(step, spcd, index, scalar, growth, time):
    power_val = scalar / growth
    denom = 1 - math.exp(1)
    num_den = spcd / step * (360 * time + index + 0.5)
    num_pow = -pow(num_den, power_val)
    num1 = - math.exp(num_pow) + 1
    num2 = pow(spcd / step * (360 * time + index + 0.5), power_val)
    num3 = -math.exp(1) * pow(spcd / step * (360 * time + index + 0.5), power_val)
    output = (num1 + num2 + num3) / denom
    return output


def rth_integral_four(step, spcd, index, scalar, growth, time):
    denom = math.exp(-360 / step * spcd / growth) - 1
    num1 = -math.exp(-spcd * (720 / step * time + 2 * index + 720 / step + 1) / (2 * growth))
    num2 = -time
    num3 = time * math.exp(-360 / step * spcd / growth)
    num4 = math.exp(-spcd * (1 + 2 * index) / (2 * growth))
    num5 = -1
    num6 = math.exp(-360 / step * spcd / growth)
    out = scalar / denom * (num1 + num2 + num3 + num4 + num5 + num6)
    return out


def get_igbt_rth_from_time(time, transient_thermal_values):
    if transient_thermal_values['igbt_t3_value'] > 0:
        num1 = transient_thermal_values['igbt_r1_per_r0_value'] * (
                1.0 - math.exp(-1.0 * time / transient_thermal_values['igbt_t1_per_j1_value']))
        num2 = transient_thermal_values['igbt_r2_per_j0_value'] * (
                1.0 - math.exp(-1.0 * time / transient_thermal_values['igbt_t2_per_t1_value']))
        num3 = transient_thermal_values['igbt_r3_per_t0_value'] * (1.0 - math.exp(-1.0 * time / transient_thermal_values['igbt_t3_value']))
        num4 = transient_thermal_values['igbt_r4_per_r1_value'] * (1.0 - math.exp(-1.0 * time / transient_thermal_values['igbt_t4_value']))
        rth_from_time = (num1 + num2 + num3 + num4) * transient_thermal_values['rth_tr_value']
    else:
        num1 = (1 - math.exp(-1 * pow(time, (transient_thermal_values['igbt_r2_per_j0_value'] / transient_thermal_values['igbt_r3_per_t0_value']))))
        num1 = num1 * transient_thermal_values['igbt_r1_per_r0_value']
        num2 = (1 - math.exp(-1 * pow(time, (transient_thermal_values['igbt_t1_per_j1_value'] / transient_thermal_values['igbt_t2_per_t1_value']))))
        num2 = num2 * transient_thermal_values['igbt_r4_per_r1_value']
        rth_from_time = (num1 + num2) * transient_thermal_values['rth_tr_value']

    return rth_from_time


def integrate_rth_igbt(step, spcd, start_time, index, transient_thermal_values):
    start_time = math.floor(start_time / 360)
    if transient_thermal_values['igbt_t3_value'] > 0:
        num1 = rth_integral_four(step, spcd, index, transient_thermal_values['igbt_r1_per_r0_value'], transient_thermal_values['igbt_t1_per_j1_value'], start_time)
        num2 = rth_integral_four(step, spcd, index, transient_thermal_values['igbt_r2_per_j0_value'], transient_thermal_values['igbt_t2_per_t1_value'], start_time)
        num3 = rth_integral_four(step, spcd, index, transient_thermal_values['igbt_r3_per_t0_value'], transient_thermal_values['igbt_t3_value'], start_time)
        num4 = rth_integral_four(step, spcd, index, transient_thermal_values['igbt_r4_per_r1_value'], transient_thermal_values['igbt_t4_value'], start_time)
        rth_from_time = (num1 + num2 + num3 + num4) * transient_thermal_values['rth_tr_value']
    else:
        num1 = rth_integral_two(step, spcd, index, transient_thermal_values['igbt_r2_per_j0_value'], transient_thermal_values['igbt_r3_per_t0_value'], start_time)
        num1 = num1 * transient_thermal_values['igbt_r1_per_r0_value']
        num2 = rth_integral_two(step, spcd, index, transient_thermal_values['igbt_t1_per_j1_value'], transient_thermal_values['igbt_t2_per_t1_value'], start_time)
        num2 = num2 * transient_thermal_values['igbt_r4_per_r1_value']
        rth_from_time = (num1 + num2) * transient_thermal_values['rth_tr_value']
    return rth_from_time


def integrate_rth_fwd(step, spcd, start_time, index, transient_thermal_values):
    start_time = math.floor(start_time / 360)
    if transient_thermal_values['fwd_t3_value'] > 0:
        num1 = rth_integral_four(step, spcd, index, transient_thermal_values['fwd_r1a_per_rd0_value'], transient_thermal_values['fwd_t1a_per_jd1_value'], start_time)
        num2 = rth_integral_four(step, spcd, index, transient_thermal_values['fwd_r2a_per_jd0_value'], transient_thermal_values['fwd_t2a_per_td1_value'], start_time)
        num3 = rth_integral_four(step, spcd, index, transient_thermal_values['fwd_r3a_per_td0_value'], transient_thermal_values['fwd_t3_value'], start_time)
        num4 = rth_integral_four(step, spcd, index, transient_thermal_values['fwd_r4a_per_rd1_value'], transient_thermal_values['fwd_t4_value'], start_time)
        rth_from_time = (num1 + num2 + num3 + num4) * transient_thermal_values['rth_di_value']
    else:
        num1 = rth_integral_two(step, spcd, index, transient_thermal_values['fwd_r2a_per_jd0_value'], transient_thermal_values['fwd_r3a_per_td0_value'], start_time)
        num1 = num1 * transient_thermal_values['fwd_r1a_per_rd0_value']
        num2 = rth_integral_two(step, spcd, index, transient_thermal_values['fwd_t1a_per_jd1_value'], transient_thermal_values['fwd_t2a_per_td1_value'], start_time)
        num2 = num2 * transient_thermal_values['fwd_r4a_per_rd1_value']
        rth_from_time = (num1 + num2) * transient_thermal_values['rth_di_value']
    return rth_from_time


def create_thermal_resistance_dict(input_fo, transient_thermal_values, step):
    igbt_dc_rth = get_igbt_rth_from_time(10.0, transient_thermal_values)
    fwd_dc_rth = get_fwd_rth_from_time(10.0, transient_thermal_values, False)
    sec_per_cycle_degree = 1.0 / input_fo / 360.0 * step
    time_value = sec_per_cycle_degree / 2.0
    time_step = 0.0
    degree_count = -int(360 / step)

    rth_dict_igbt = np.zeros(int(360 / step))
    rth_dict_fwd = np.zeros(int(360 / step))

    while time_value <= 10.0:
        degree_count += 360
        time_step += sec_per_cycle_degree / step * 360
        igbt_trans_rth = get_igbt_rth_from_time(time_step, transient_thermal_values)
        fwd_trans_rth = get_fwd_rth_from_time(time_step, transient_thermal_values, False)
        # for index1 in range(360):
        #     rth_dict_igbt[index1] += get_igbt_rth_from_time(time_value, transient_thermal_values)  # integrate to reach this value somehow
        #     rth_dict_fwd[index1] += get_fwd_rth_from_time(time_value, transient_thermal_values, False)
        #     time_value += sec_per_cycle_degree
        if igbt_trans_rth / igbt_dc_rth >= 0.99 and fwd_trans_rth / fwd_dc_rth >= 0.99:
            break

    rth_fwd_int = []
    rth_igbt_int = []
    time_value = time_step + sec_per_cycle_degree / 2
    for i in range(int(360 / step)):
        rth_fwd_int.append(integrate_rth_fwd(step, sec_per_cycle_degree, degree_count, i, transient_thermal_values))
        rth_igbt_int.append(integrate_rth_igbt(step, sec_per_cycle_degree, degree_count, i, transient_thermal_values))

    results = {}
    results['igbt_thermo'] = rth_igbt_int
    results['fwd_thermo'] = rth_fwd_int
    # results['igbt_thermo'] = rth_dict_igbt
    # results['fwd_thermo'] = rth_dict_fwd
    results['time_value'] = time_value
    results['sec_per_cycle_degree'] = sec_per_cycle_degree
    return results


def tj_max_calculation(p_igbt_ave, p_fwd_ave, p_igbt_inst_list, p_fwd_inst_list, input_tc, input_fo, tj_ave_igbt, tj_ave_fwd,
                       transient_thermal_values, step):
    thermo_dict = create_thermal_resistance_dict(input_fo, transient_thermal_values, step)
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

    for index1 in range(int(360 / step)):
        tj_igbt_inst = input_tc + p_igbt_ave * transient_thermal_values['rth_tr_value'] + \
                       transient_thermal_values['rth_thermal_contact'] * (
                               p_igbt_ave + p_fwd_ave)
        tj_fwd_inst = input_tc + p_fwd_ave * transient_thermal_values['rth_di_value'] + \
                      transient_thermal_values['rth_thermal_contact'] * (
                              p_igbt_ave + p_fwd_ave)

        tj_igbt_inst -= (p_igbt_inst_list[int(360 / step) - 1] - p_igbt_ave) * rth_dict_igbt[
            index1]
        tj_fwd_inst -= (p_fwd_inst_list[int(360 / step) - 1] - p_fwd_ave) * rth_dict_fwd[
            index1]
        rth_dict_igbt[index1] += get_igbt_rth_from_time(time_value, transient_thermal_values)
        rth_dict_fwd[index1] += get_fwd_rth_from_time(time_value, transient_thermal_values, False)
        tj_igbt_inst += (p_igbt_inst_list[0] - p_igbt_ave) * rth_dict_igbt[
            index1]
        tj_fwd_inst += (p_fwd_inst_list[0] - p_fwd_ave) * rth_dict_fwd[
            index1]
        time_value += sec_per_cycle_degree

        for degree_count in range(1, int(360 / step)):
            delta_p_igbt = p_igbt_inst_list[degree_count] - p_igbt_inst_list[degree_count - 1]
            delta_p_fwd = p_fwd_inst_list[degree_count] - p_fwd_inst_list[degree_count - 1]
            tj_igbt_inst += delta_p_igbt * rth_dict_igbt[(int(360 / step) + index1 - degree_count) % int(360 / step)]
            tj_fwd_inst += delta_p_fwd * rth_dict_fwd[(int(360 / step) + index1 - degree_count) % int(360 / step)]

        time_list.append(time_value)
        rad_list.append((index1 + 1))
        tj_igbt_list.append(tj_igbt_inst)
        p_igbt_list.append(p_igbt_inst_list[index1])
        tj_fwd_list.append(tj_fwd_inst)
        p_fwd_list.append(p_fwd_inst_list[index1])

    # max calc
    igbt_ave_temp = np.average(tj_igbt_list)
    fwd_ave_temp = np.average(tj_fwd_list)
    num1 = tj_ave_igbt - igbt_ave_temp
    num2 = tj_ave_fwd - fwd_ave_temp

    for index2 in range(int(360 / step)):
        tj_igbt_list[index2] = tj_igbt_list[index2] + num1
        tj_fwd_list[index2] = tj_fwd_list[index2] + num2
        time_list.append(time_list[int(360 / step) - 1] + time_list[index2])
        rad_list.append(int(360 / step) + index2 + 1)
        tj_igbt_list.append(tj_igbt_list[index2])
        p_igbt_list.append(p_igbt_list[index2])
        tj_fwd_list.append(tj_fwd_list[index2])
        p_fwd_list.append(p_fwd_list[index2])

    tj_max_igbt = max(tj_igbt_list)
    tj_max_fwd = max(tj_fwd_list)

    # tj_max_igbt = max(tj_igbt_list)
    # tj_max_fwd = max(tj_fwd_list)

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
