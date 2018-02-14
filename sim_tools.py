import numpy as np
import scipy.interpolate as sp
import os.path
import pandas as pd
import csv
import original_sim
import mark_sim
import time
import math


class InputFile(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


def input_file_checker(input_file):
    if len(input_file['input_bus_voltage']) > 1:
        return True
    return False


def m_sim_runner(file_values, input_file_values):
    count = 0
    if len(input_file_values['input_bus_voltage']) > 1:
        output_file_temp_3 = []
        input_file_temp_2 = []
        for x in range(len(input_file_values['input_bus_voltage'])):
            input_file_values_temp_1 = [y[x] for y in input_file_values.values()]
            input_file_values_temp_2 = [y for y in input_file_values.keys()]
            input_file_values_temp = {input_file_values_temp_2[x]: input_file_values_temp_1[x] for x in range(len(input_file_values_temp_1))}
            input_file_temp_2.append(input_file_values_temp_1)

            output_file = original_sim.m_sim_output_calc(file_values, input_file_values_temp)

            output_file_temp_1 = [math.floor(y * 100) / 100 for y in output_file.values()]
            output_file_temp_3.append(output_file_temp_1)
            output_file_temp_2 = [y for y in output_file.keys()]
            count += 1
            print(count)
        input_file_temp_2 = np.transpose(input_file_temp_2)
        output_file_temp_3 = np.transpose(output_file_temp_3)
        output_file_dict = {output_file_temp_2[x]: output_file_temp_3[x] for x in range(len(output_file_temp_2))}
        input_file_dict = {input_file_values_temp_2[x]: input_file_temp_2[x] for x in range(len(input_file_values_temp_2))}
        full_file_dict = {**input_file_dict, **output_file_dict}
    else:
        output_file = original_sim.m_sim_output_calc(file_values, input_file_values)
        full_file_dict = {**input_file_values, **output_file}
    return full_file_dict


def mark_sim_runner(file_values, input_file_values):
    if len(input_file_values['input_bus_voltage']) > 1:
        output_file_temp_3 = []
        input_file_temp_2 = []
        for x in range(len(input_file_values['input_bus_voltage'])):
            input_file_values_temp_1 = [y[x] for y in input_file_values.values()]
            input_file_values_temp_2 = [y for y in input_file_values.keys()]
            input_file_values_temp = {input_file_values_temp_2[x]: input_file_values_temp_1[x] for x in range(len(input_file_values_temp_1))}
            input_file_temp_2.append(input_file_values_temp_1)

            output_file = mark_sim.mark_sim_output_calc(file_values, input_file_values_temp)

            output_file_temp_1 = [y for y in output_file.values()]
            output_file_temp_3.append(output_file_temp_1)
            output_file_temp_2 = [y for y in output_file.keys()]
        input_file_temp_2 = np.transpose(input_file_temp_2)
        output_file_temp_3 = np.transpose(output_file_temp_3)
        output_file_dict = {output_file_temp_2[x]: output_file_temp_3[x] for x in range(len(output_file_temp_2))}
        input_file_dict = {input_file_values_temp_2[x]: input_file_temp_2[x] for x in range(len(input_file_values_temp_2))}
        full_file_dict = {**input_file_dict, **output_file_dict}
    else:
        output_file = original_sim.m_sim_output_calc(file_values, input_file_values)
        full_file_dict = {**input_file_values, **output_file}
    return full_file_dict


def output_file_writer(output_file):
    columns = ['input_bus_voltage',
               'input_ic_arms',
               'power_factor',
               'mod_depth',
               'freq_carrier',
               'freq_output',
               'input_rg_on',
               'input_rg_off',
               'tj_test',
               'input_tc',
               'P_total_IGBT',
               'E_sw_IGBT',
               'P_cond_IGBT',
               'E_sw_on_IGBT',
               'E_sw_off_IGBT',
               'Tc_Ave',
               'delta_Tj_Ave_IGBT',
               'Tj_Ave_IGBT',
               'delta_Tj_Max_IGBT',
               'Tj_max_IGBT',
               'P_total_FWD',
               'E_rr_FWD',
               'P_cond_FWD',
               'delta_Tj_Ave_FWD',
               'Tj_Ave_FWD',
               'delta_Tj_Max_FWD',
               'Tj_Max_FWD']
    module_file = 'output' + time.strftime("%d_%b_%y_%H_%M_%S") + '.csv'
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in output_file.items()]), columns=columns)
    df.to_csv(module_file)


def input_file_reader():
    input_file = 'input_file.csv'

    row_list = [["tj_test",
                 "input_bus_voltage",
                 "input_ic_arms",
                 "power_factor",
                 "mod_depth",
                 "freq_carrier",
                 "freq_output",
                 "input_tc",
                 "input_rg_on",
                 "input_rg_off"]]

    if not os.path.exists(input_file):
        with open(input_file, 'w+') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)

    row_list = row_list[0]
    value_dict = {}
    for x in range(len(row_list)):
        value_dict[row_list[x]] = pull_data_from_column(input_file, row_list[x])
    for x in range(len(row_list)):
        if len(value_dict[row_list[x]]) == 1:
            value_dict[row_list[x]] = value_dict[row_list[x]][0]
    return value_dict


def module_file_reader():
    module_file = 'module_file.csv'

    row_list = [["module_name",
                 "ic_from_vcesat_25",
                 "vcesat_from_vcesat_25",
                 "ic_from_vcesat_125",
                 "vcesat_from_vcesat_125",
                 "ic_from_vcesat_150",
                 "vcesat_from_vcesat_150",
                 "ie_from_vecsat_25",
                 "vecsat_from_vecsat_25",
                 "ie_from_vecsat_125",
                 "vecsat_from_vecsat_125",
                 "ie_from_vecsat_150",
                 "vecsat_from_vecsat_150",
                 "ic_from_e_sw_on_125",
                 "e_sw_on_from_e_sw_on_125",
                 "ic_from_e_sw_on_150",
                 "e_sw_on_from_e_sw_on_150",
                 "ic_from_e_sw_off_125",
                 "e_sw_off_from_e_sw_off_125",
                 "ic_from_e_sw_off_150",
                 "e_sw_off_from_e_sw_off_150",
                 "ic_from_e_rr_125",
                 "e_rr_from_e_rr_125",
                 "ic_from_e_rr_150",
                 "e_rr_from_e_rr_150",
                 "e_on_from_e_on_125",
                 "e_rg_from_e_on_125",
                 "e_on_from_e_on_150",
                 "e_rg_from_e_on_150",
                 "e_off_from_e_off_125",
                 "e_rg_from_e_off_125",
                 "e_off_from_e_off_150",
                 "e_rg_from_e_off_150",
                 "e_rr_from_e_rg_125",
                 "e_rg_from_e_rg_125",
                 "e_rr_from_e_rg_150",
                 "e_rg_from_e_rg_150",
                 "igbt_r1_per_r0_value",
                 "igbt_r2_per_j0_value",
                 "igbt_r3_per_t0_value",
                 "igbt_r4_per_r1_value",
                 "igbt_t1_per_j1_value",
                 "igbt_t2_per_t1_value",
                 "igbt_t3_value",
                 "igbt_t4_value",
                 "fwd_r1a_per_rd0_value",
                 "fwd_r2a_per_jd0_value",
                 "fwd_r3a_per_td0_value",
                 "fwd_r4a_per_rd1_value",
                 "fwd_t1a_per_jd1_value",
                 "fwd_t2a_per_td1_value",
                 "fwd_t3_value",
                 "fwd_t4_value",
                 "rth_tr_value",
                 "rth_di_value",
                 "rth_thermal_contact",
                 "vcc_value",
                 "current_value"
                 ]]

    if not os.path.exists(module_file) and not os.path.exists('module_file_revised.csv'):
        with open(module_file, 'w+') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)

    row_list = row_list[0]
    value_dict = {}

    for x in range(len(row_list)):
        value_dict[row_list[x]] = pull_data_from_column('module_file_revised.csv', row_list[x])
    for x in range(np.size(row_list)):
        if np.size(value_dict[row_list[x]]) == 1:
            value_dict[row_list[x]] = value_dict[row_list[x]][0]
    return value_dict


def module_file_updated_writer(file_values):
    column_list = ["module_name",
                   "ic_from_vcesat_25",
                   "vcesat_from_vcesat_25",
                   "ic_from_vcesat_125",
                   "vcesat_from_vcesat_125",
                   "ic_from_vcesat_150",
                   "vcesat_from_vcesat_150",
                   "ie_from_vecsat_25",
                   "vecsat_from_vecsat_25",
                   "ie_from_vecsat_125",
                   "vecsat_from_vecsat_125",
                   "ie_from_vecsat_150",
                   "vecsat_from_vecsat_150",
                   "ic_from_e_sw_on_125",
                   "e_sw_on_from_e_sw_on_125",
                   "ic_from_e_sw_on_150",
                   "e_sw_on_from_e_sw_on_150",
                   "ic_from_e_sw_off_125",
                   "e_sw_off_from_e_sw_off_125",
                   "ic_from_e_sw_off_150",
                   "e_sw_off_from_e_sw_off_150",
                   "ic_from_e_rr_125",
                   "e_rr_from_e_rr_125",
                   "ic_from_e_rr_150",
                   "e_rr_from_e_rr_150",
                   "e_on_from_e_on_125",
                   "e_rg_from_e_on_125",
                   "e_on_from_e_on_150",
                   "e_rg_from_e_on_150",
                   "e_off_from_e_off_125",
                   "e_rg_from_e_off_125",
                   "e_off_from_e_off_150",
                   "e_rg_from_e_off_150",
                   "e_rr_from_e_rg_125",
                   "e_rg_from_e_rg_125",
                   "e_rr_from_e_rg_150",
                   "e_rg_from_e_rg_150",
                   "igbt_r1_per_r0_value",
                   "igbt_r2_per_j0_value",
                   "igbt_r3_per_t0_value",
                   "igbt_r4_per_r1_value",
                   "igbt_t1_per_j1_value",
                   "igbt_t2_per_t1_value",
                   "igbt_t3_value",
                   "igbt_t4_value",
                   "fwd_r1a_per_rd0_value",
                   "fwd_r2a_per_jd0_value",
                   "fwd_r3a_per_td0_value",
                   "fwd_r4a_per_rd1_value",
                   "fwd_t1a_per_jd1_value",
                   "fwd_t2a_per_td1_value",
                   "fwd_t3_value",
                   "fwd_t4_value",
                   "rth_tr_value",
                   "rth_di_value",
                   "rth_thermal_contact",
                   "vcc_value",
                   "current_value"
                   ]

    module_file = 'module_file_revised.csv'
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in file_values.items()]), columns=column_list)
    df.to_csv(module_file)


def pull_data_from_column(module_file, column_string):
    df = pd.read_csv(module_file)
    x = df[column_string].as_matrix()
    x = x[~np.isnan(x)]
    return x


def array_cleaner(independent_var, dependent_var, start, stop,
                  length):  # could try some sort of log system here but still thinking
    output_dependent_array = []
    output_independent_array = []
    independent_var_list = []
    min = np.min(independent_var)
    if np.max(independent_var) > 100:
        list = [start, start + 7 / 2400 * stop, start + 3 / 240 * stop, start + 6 / 240 * stop, start + stop / 20, start + stop / 8, start + 45 / 240 * stop, start + stop / 4,
                start + stop / 2, stop]
    else:
        list = [min, (min + 0.6) / 10 * stop, (min + 1) / 10 * stop, (min + 1.5) / 10 * stop, (min + 2.5) / 10 * stop, (min + 4) / 10 * stop, (min + 3.7) / 10 * stop,
                (min + 5.8) / 10 * stop, (min + 8) / 10 * stop, stop]
    for x in range(10):
        independent_var_list.append(list[x])

    for x in range(0, int(length)):
        output_dependent_array.append(independent_var_list[x])
        output_independent_array.append(float(np.interp(independent_var_list[x], independent_var, dependent_var)))
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


def vce_ic_maker(ic25, vce25, ic125, vce125, ic150, vce150, max):
    output1, vcesat25 = array_cleaner(ic25, vce25, 0, max, 10)
    output1, vcesat125 = array_cleaner(ic125, vce125, 0, max, 10)
    output1, vcesat150 = array_cleaner(ic150, vce150, 0, max, 10)
    # output1 = origin_checker(output1)
    # vcesat25 = origin_checker(vcesat25)
    # vcesat125 = origin_checker(vcesat125)
    # vcesat150 = origin_checker(vcesat150)
    grid_tj = np.mgrid[25:150:10j]
    temp25 = np.full(len(vcesat25), 25.)
    temp125 = np.full(len(vcesat125), 125.)
    temp150 = np.full(len(vcesat150), 150.)
    temp_all = threepeat_array(temp25, temp125, temp150)
    vcesat_all = threepeat_array(vcesat25, vcesat125, vcesat150)
    current_all = threepeat_array(output1, output1, output1)
    out = {}
    out['grid_tj'] = grid_tj
    out['temp_all'] = temp_all
    out['vcesat_all'] = vcesat_all
    out['current_all'] = current_all
    return out


def vce_from_tj_ic_solver(ic_vce_dict, tj_in, ic_in):
    if not ic_in == 0.0:
        grid_tj = ic_vce_dict['grid_tj']
        temp_all = ic_vce_dict['temp_all']
        vcesat_all = ic_vce_dict['vcesat_all']
        current_all = ic_vce_dict['current_all']
        grid_z0 = sp.griddata((temp_all, current_all), vcesat_all, (grid_tj, ic_in), method="linear")
        vce_int = sp.interp1d(grid_tj, grid_z0, fill_value='extrapolate')
        vce = vce_int(tj_in)
        if vce < 0:
            vce = 0
        # vce = vce_for_temp(tj_in)
    else:
        vce = 0
    return vce


def esw_ic_maker(ic125, vce125, ic150, vce150, max):
    output1, vcesat125 = array_cleaner(ic125, vce125, 0, max, 10)
    output1, vcesat150 = array_cleaner(ic150, vce150, 0, max, 10)
    # output1 = origin_checker(output1)
    # vcesat125 = origin_checker(vcesat125)
    # vcesat150 = origin_checker(vcesat150)
    grid_tj = np.mgrid[125:150:10j]
    temp125 = np.full(len(vcesat125), 125.)
    temp150 = np.full(len(vcesat150), 150.)
    temp_all = twopeat_array(temp125, temp150)
    vcesat_all = twopeat_array(vcesat125, vcesat150)
    current_all = twopeat_array(output1, output1)
    out = {}
    out['grid_tj'] = grid_tj
    out['temp_all'] = temp_all
    out['vcesat_all'] = vcesat_all
    out['current_all'] = current_all
    return out


def esw_solver(esw_dict, tj_in, ic_in):
    if not ic_in == 0.0:
        grid_tj = esw_dict['grid_tj']
        temp_all = esw_dict['temp_all']
        vcesat_all = esw_dict['vcesat_all']
        current_all = esw_dict['current_all']
        grid_z0 = sp.griddata((temp_all, current_all), vcesat_all, (grid_tj, ic_in), method="linear")
        vce = sp.interp1d(grid_tj, grid_z0, fill_value='extrapolate')
        esw = vce(tj_in)
        if esw < 0:
            esw = 0
        # esw = vce_for_temp(tj_in)
    else:
        esw = 0
    return esw


def strictly_increasing(L):
    return all(x < y for x, y in zip(L, L[1:]))


def array_flipper(dependent_array, independent_array):
    if not strictly_increasing(dependent_array):
        dependent_array = np.flipud(dependent_array)
        independent_array = np.flipud(independent_array)
    return [dependent_array, independent_array]


def esw_rg_checker(e_sw_rg, e_sw_ic, ic_e_sw, current_value, threshold):
    if e_sw_rg[0] > threshold:
        e_sw_rg = esw_rg_fixer(e_sw_ic, ic_e_sw, e_sw_rg, current_value)
    return e_sw_rg


def esw_rg_fixer(esw_ic_esw, ic_ic_esw, esw_rg_esw, ic):
    baseline = np.interp(ic_ic_esw, esw_ic_esw)
    baseline_energy = float(baseline(ic))
    for x in range(0, len(esw_rg_esw)):
        esw_rg_esw[x] = esw_rg_esw[x] / float(baseline_energy)
    return esw_rg_esw


def file_value_checker(file_values):
    threshold = 10
    current_value = file_values["current_value"]

    file_values["ic_from_vcesat_25"], file_values["vcesat_from_vcesat_25"] = array_flipper(file_values["ic_from_vcesat_25"], file_values["vcesat_from_vcesat_25"])
    file_values["ic_from_vcesat_125"], file_values["vcesat_from_vcesat_125"] = array_flipper(file_values["ic_from_vcesat_125"], file_values["vcesat_from_vcesat_125"])
    file_values["ic_from_vcesat_150"], file_values["vcesat_from_vcesat_150"] = array_flipper(file_values["ic_from_vcesat_150"], file_values["vcesat_from_vcesat_150"])
    file_values["ie_from_vecsat_25"], file_values["vecsat_from_vecsat_25"] = array_flipper(file_values["ie_from_vecsat_25"], file_values["vecsat_from_vecsat_25"])
    file_values["ie_from_vecsat_125"], file_values["vecsat_from_vecsat_125"] = array_flipper(file_values["ie_from_vecsat_125"], file_values["vecsat_from_vecsat_125"])
    file_values["ie_from_vecsat_150"], file_values["vecsat_from_vecsat_150"] = array_flipper(file_values["ie_from_vecsat_150"], file_values["vecsat_from_vecsat_150"])
    file_values["ic_from_e_sw_on_125"], file_values["e_sw_on_from_e_sw_on_125"] = array_flipper(file_values["ic_from_e_sw_on_125"], file_values["e_sw_on_from_e_sw_on_125"])
    file_values["ic_from_e_sw_on_150"], file_values["e_sw_on_from_e_sw_on_150"] = array_flipper(file_values["ic_from_e_sw_on_150"], file_values["e_sw_on_from_e_sw_on_150"])
    file_values["ic_from_e_sw_off_125"], file_values["e_sw_off_from_e_sw_off_125"] = array_flipper(file_values["ic_from_e_sw_off_125"], file_values["e_sw_off_from_e_sw_off_125"])
    file_values["ic_from_e_sw_off_150"], file_values["e_sw_off_from_e_sw_off_150"] = array_flipper(file_values["ic_from_e_sw_off_150"], file_values["e_sw_off_from_e_sw_off_150"])
    file_values["ic_from_e_rr_125"], file_values["e_rr_from_e_rr_125"] = array_flipper(file_values["ic_from_e_rr_125"], file_values["e_rr_from_e_rr_125"])
    file_values["ic_from_e_rr_150"], file_values["e_rr_from_e_rr_150"] = array_flipper(file_values["ic_from_e_rr_150"], file_values["e_rr_from_e_rr_150"])
    file_values["e_rg_from_e_on_125"], file_values["e_on_from_e_on_125"] = array_flipper(file_values["e_rg_from_e_on_125"], file_values["e_on_from_e_on_125"])
    file_values["e_rg_from_e_on_150"], file_values["e_on_from_e_on_150"] = array_flipper(file_values["e_rg_from_e_on_150"], file_values["e_on_from_e_on_150"])
    file_values["e_rg_from_e_off_125"], file_values["e_off_from_e_off_125"] = array_flipper(file_values["e_rg_from_e_off_125"], file_values["e_off_from_e_off_125"])
    file_values["e_rg_from_e_off_150"], file_values["e_off_from_e_off_150"] = array_flipper(file_values["e_rg_from_e_off_150"], file_values["e_off_from_e_off_150"])
    file_values["e_rg_from_e_rg_125"], file_values["e_rr_from_e_rg_125"] = array_flipper(file_values["e_rg_from_e_rg_125"], file_values["e_rr_from_e_rg_125"])
    file_values["e_rg_from_e_rg_150"], file_values["e_rr_from_e_rg_150"] = array_flipper(file_values["e_rg_from_e_rg_150"], file_values["e_rr_from_e_rg_150"])

    file_values['e_on_from_e_on_125'] = esw_rg_checker(file_values['e_on_from_e_on_125'], file_values['e_sw_on_from_e_sw_on_125'], file_values['ic_from_e_sw_on_125'],
                                                       current_value, threshold)
    file_values['e_on_from_e_on_150'] = esw_rg_checker(file_values['e_on_from_e_on_150'], file_values['e_sw_on_from_e_sw_on_150'], file_values['ic_from_e_sw_on_150'],
                                                       current_value, threshold)
    file_values['e_off_from_e_off_125'] = esw_rg_checker(file_values['e_off_from_e_off_125'], file_values['e_sw_off_from_e_sw_off_125'], file_values['ic_from_e_sw_off_125'],
                                                         current_value, threshold)

    file_values['e_off_from_e_off_150'] = esw_rg_checker(file_values['e_off_from_e_off_150'], file_values['e_sw_off_from_e_sw_off_150'], file_values['ic_from_e_sw_off_150'],
                                                         current_value, threshold)
    file_values['e_rr_from_e_rg_125'] = esw_rg_checker(file_values['e_rr_from_e_rg_125'], file_values['e_rr_from_e_rr_125'], file_values['ic_from_e_rr_125'], current_value,
                                                       threshold)
    file_values['e_rr_from_e_rg_150'] = esw_rg_checker(file_values['e_rr_from_e_rg_150'], file_values['e_rr_from_e_rr_150'], file_values['ic_from_e_rr_150'], current_value,
                                                       threshold)

    return file_values


def origin_checker(checkee):
    found = False
    for x in range(len(checkee)):
        if checkee[x] == 0:
            found = True
    if not found:
        checkee = np.insert(checkee, 0, 0.0)
    return checkee


def doublearray_maker(array_in):
    array_out = []
    for i in range(2 * len(array_in)):
        array_out.append(array_in[i % len(array_in)])
    return array_out
