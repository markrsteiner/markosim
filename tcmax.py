import math
import numpy as np
import pandas as pd


# global diode_dict
# diode_dict= []

def get_igbt_rth_from_time(time, transient_thermal_values):
    num1 = transient_thermal_values['igbt_r1_per_r0_value'] * (
            1.0 - math.exp(-1.0 * time / transient_thermal_values['igbt_t1_per_j1_value']))
    num2 = transient_thermal_values['igbt_r2_per_j0_value'] * (
            1.0 - math.exp(-1.0 * time / transient_thermal_values['igbt_t2_per_t1_value']))
    num3 = transient_thermal_values['igbt_r3_per_t0_value'] * (
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
    # if flag == True:
    #     diode_dict.append([time, num1, num2, num3, num4])
    rth_from_time = (num1 + num2 + num3 + num4) * transient_thermal_values['rth_di_value']
    return rth_from_time


def rth_integral(spcd, scalar, growth, time):
    time = float(time / 360)
    index = 0
    time_check = spcd * (time * 360 + index)
    denom1 = (1 - math.exp(-spcd * 360 / growth))
    num1 = time / denom1
    num2 = math.exp(-spcd / growth * ((time + 1) * 360 + index)) / denom1
    # num3 = math.exp(-spcd*index/growth)/denom1
    # num4 = 1/denom1
    num5 = time * math.exp(-spcd * 360 / growth) / denom1
    # num6 = math.exp(-spcd*360/growth)/denom1
    out = scalar * (num1 + num2 - num5)

    return out


def integrate_rth_fwd(spcd, start_time, stop_time, transient_thermal_values):
    stop_time = start_time - 7920
    num1 = rth_integral(spcd, transient_thermal_values['fwd_r1a_per_rd0_value'], transient_thermal_values['fwd_t1a_per_jd1_value'], start_time - 0.49)
    num2 = rth_integral(spcd, transient_thermal_values['fwd_r1a_per_rd0_value'], transient_thermal_values['fwd_t1a_per_jd1_value'], stop_time)
    num9 = num1 - num2
    num3 = rth_integral(spcd, transient_thermal_values['fwd_r2a_per_jd0_value'], transient_thermal_values['fwd_t2a_per_td1_value'], start_time - 0.46)
    num4 = rth_integral(spcd, transient_thermal_values['fwd_r2a_per_jd0_value'], transient_thermal_values['fwd_t2a_per_td1_value'], stop_time)
    num10 = num3 - num4
    num5 = rth_integral(spcd, transient_thermal_values['fwd_r3a_per_td0_value'], transient_thermal_values['fwd_t3_value'], start_time - 0.194)
    num6 = rth_integral(spcd, transient_thermal_values['fwd_r3a_per_td0_value'], transient_thermal_values['fwd_t3_value'], stop_time)
    num11 = num5 - num6
    num7 = rth_integral(spcd, transient_thermal_values['fwd_r4a_per_rd1_value'], transient_thermal_values['fwd_t4_value'], start_time + 0.11)
    num8 = rth_integral(spcd, transient_thermal_values['fwd_r4a_per_rd1_value'], transient_thermal_values['fwd_t4_value'], stop_time)
    num12 = num7 - num8
    time_check = spcd * (start_time - 7920)
    num13 = get_fwd_rth_from_time(time_check, transient_thermal_values, False)
    rth_from_time = (num9 + num10 + num11 + num12 + num13) * transient_thermal_values['rth_di_value']
    return rth_from_time


def create_thermal_resistance_dict(input_fo, transient_thermal_values):
    igbt_dc_rth = get_igbt_rth_from_time(10.0, transient_thermal_values)
    fwd_dc_rth = get_fwd_rth_from_time(10.0, transient_thermal_values)
    sec_per_cycle_degree = 1.0 / input_fo / 360.0
    time_value = sec_per_cycle_degree / 2.0
    time_step = 0.0
    # degree_count = -360

    rth_dict_igbt = [0 for __ in range(360)]
    rth_dict_fwd = [0 for __ in range(360)]

    test = []
    while time_value <= 10.0:
        # degree_count += 360
        time_step += sec_per_cycle_degree * 360.0
        igbt_trans_rth = get_igbt_rth_from_time(time_step, transient_thermal_values)
        fwd_trans_rth = get_fwd_rth_from_time(time_step, transient_thermal_values)
        for index1 in range(360):
            # count = time_value/sec_per_cycle_degree
            rth_dict_igbt[index1] += get_igbt_rth_from_time(time_value, transient_thermal_values)  # integrate to reach this value somehow
            # if igbt_trans_rth / igbt_dc_rth >= 0.99 and fwd_trans_rth / fwd_dc_rth >= 0.99:
            #     test.append(rth_dict_igbt[index1])
            rth_dict_fwd[index1] += get_fwd_rth_from_time(time_value, transient_thermal_values)
            time_value += sec_per_cycle_degree
        if igbt_trans_rth / igbt_dc_rth >= 0.99 and fwd_trans_rth / fwd_dc_rth >= 0.99:
            break
    # f = pd.DataFrame(diode_dict)
    # f.to_csv('read_me.csv')
    for x in range(len(rth_dict_fwd)):
        rth_dict_fwd[x] = rth_dict_fwd[x] * transient_thermal_values['rth_di_value']
    # check = np.sum(rth_dict_fwd)
    # rth_fwd_int = []
    # for i in range(360):
    #     rth_fwd_int.append(integrate_rth_fwd(sec_per_cycle_degree, degree_count + i*sec_per_cycle_degree*360*60 + sec_per_cycle_degree*360*30, 0, transient_thermal_values))
    with open('output_test.txt', 'w+') as file:
        file.write(str(test))

    results = {}
    results['igbt_thermo'] = rth_dict_igbt
    results['fwd_thermo'] = rth_dict_fwd
    results['time_value'] = time_value
    results['sec_per_cycle_degree'] = sec_per_cycle_degree
    return results


def tj_max_calculation(p_igbt_ave, p_fwd_ave, p_igbt_inst_list, p_fwd_inst_list, input_tc, input_fo, tj_ave_igbt, tj_ave_fwd,
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

    for index1 in range(360):
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

    # max calc
    igbt_ave_temp = np.average(tj_igbt_list)
    fwd_ave_temp = np.average(tj_fwd_list)
    num1 = tj_ave_igbt - igbt_ave_temp
    num2 = tj_ave_fwd - fwd_ave_temp

    for index2 in range(360):
        tj_igbt_list[index2] = tj_igbt_list[index2] + num1
        tj_fwd_list[index2] = tj_fwd_list[index2] + num2
        time_list.append(time_list[359] + time_list[index2])
        rad_list.append(360 + index2 + 1)
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
