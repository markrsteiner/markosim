import numpy as np
import scipy.interpolate as sp
import os.path
import pandas as pd
import csv


def output_file_writer(output):
    row_list = [
        'input_bus_voltage', 'input_ic_arms', 'power_factor', 'mod_depth', 'freq_carrier', 'freq_output', 'input_tc',
        'input_rg_on', 'input_rg_off', 'tj_test', 'P_total_IGBT', 'P_cond_IGBT', 'E_sw_IGBT', 'E_sw_on_IGBT',
        'E_sw_off_IGBT',
        'delta_Tj_Ave_IGBT', 'Tj_Ave_IGBT', 'delta_Tj_Max_IGBT', 'Tj_max_IGBT', 'Tj_max_IGBT', 'delta_Tc_Ave',
        'P_total_FWD', 'P_cond_FWD', 'E_rr_FWD', 'delta_Tj_Ave_FWD', 'Tj_Ave_FWD', 'delta_Tj_Max_FWD', 'Tj_Max_FWD',
        'P_arm']
    print(output)
    df2 = pd.DataFrame(output, index=[0])
    df2 = pd.concat([df2, df2])
    print(df2)

    df2.to_csv('output.csv')


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
                 "vcc_value"
                 ]]

    if not os.path.exists(module_file):
        with open(module_file, 'w+') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)

    row_list = row_list[0]
    value_dict = {}
    for x in range(len(row_list)):
        value_dict[row_list[x]] = pull_data_from_column(module_file, row_list[x])
    for x in range(np.size(row_list)):
        if np.size(value_dict[row_list[x]]) == 1:
            value_dict[row_list[x]] = value_dict[row_list[x]][0]
    return value_dict


def pull_data_from_column(module_file, column_string):
    df = pd.read_csv(module_file)
    x = df[column_string].as_matrix()
    x = x[~np.isnan(x)]
    return x


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
    if not ic_in == 0.0:
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
                                           grid_z0)
        vce = vce_for_temp(tj_in)
    else:
        vce = 0
    return vce


def esw_solver(ic125, vce125, ic150, vce150, tj_in, ic_in, max):
    if not ic_in == 0.0:
        output1, vcesat125 = array_cleaner(ic125, vce125, 0, max, 10)
        output1, vcesat150 = array_cleaner(ic150, vce150, 0, max, 10)
        grid_tj = np.mgrid[125:150:10j]
        temp125 = np.full(len(vcesat125), 125.)
        temp150 = np.full(len(vcesat150), 150.)
        temp_all = twopeat_array(temp125, temp150)
        vcesat_all = twopeat_array(vcesat125, vcesat150)
        current_all = twopeat_array(output1, output1)
        grid_z0 = sp.griddata((temp_all, current_all), vcesat_all, (grid_tj, ic_in), method="linear")
        vce_for_temp = sp.UnivariateSpline(grid_tj, grid_z0)
        esw = vce_for_temp(tj_in)
    else:
        esw = 0
    return esw


def esw_rg_checker(e_sw_rg, e_rg_rg, e_sw_ic, ic_e_sw, threshold):
    if e_sw_rg[0] > threshold:
        for x in range(len(e_sw_rg)):
            e_sw_rg[x] = esw_rg_fixer(e_sw_ic, ic_e_sw, e_rg_rg, ic_e_sw[x])
    return e_sw_rg


def strictly_increasing(L):
    return all(x < y for x, y in zip(L, L[1:]))


def array_flipper(array1, array2):
    array1 = np.flipud(array1)
    array2 = np.flipud(array2)
    return [array1, array2]


def file_value_checker(file_values):
    threshold = 5

    if not strictly_increasing(file_values['ic_from_e_sw_on_150']):
        file_values['ic_from_e_sw_on_150'], file_values['e_sw_on_from_e_sw_on_150'] = array_flipper(
            file_values['ic_from_e_sw_on_150'], file_values['e_sw_on_from_e_sw_on_150'])

    file_values['e_on_from_e_on_125'] = esw_rg_checker(file_values['e_on_from_e_on_125'],
                                                       file_values['e_rg_from_e_on_125'],
                                                       file_values['e_sw_on_from_e_sw_on_125'],
                                                       file_values['ic_from_e_sw_on_125'], threshold)

    file_values['e_on_from_e_on_150'] = esw_rg_checker(file_values['e_on_from_e_on_150'],
                                                       file_values['e_rg_from_e_on_150'],
                                                       file_values['e_sw_on_from_e_sw_on_150'],
                                                       file_values['ic_from_e_sw_on_150'], threshold)

    # if file_values['e_on_from_e_on_150'][0] > threshold:
    #     for x in range(len(file_values['e_on_from_e_on_150'])):
    #         file_values['e_on_from_e_on_150'][x] = esw_rg_fixer(file_values['e_sw_on_from_e_sw_on_150'],
    #                                                             file_values['ic_from_e_sw_on_150'],
    #                                                             file_values['e_rg_from_e_on_150'],
    #                                                             file_values['ic_from_e_sw_on_150'][x])
    # if file_values['e_off_from_e_off_125'][0] > threshold:
    #     for x in range(len(file_values['e_off_from_e_off_125'])):
    #         file_values['e_off_from_e_off_125'][x] = esw_rg_fixer(file_values['e_sw_off_from_e_sw_off_125'],
    #                                                               file_values['ic_from_e_sw_off_125'],
    #                                                               file_values['e_rg_from_e_off_125'],
    #                                                               file_values['ic_from_e_sw_off_125'][x])
    # if file_values['e_off_from_e_off_150'][0] > threshold:
    #     for x in range(len(file_values['e_off_from_e_off_150'])):
    #         file_values['e_off_from_e_off_150'][x] = esw_rg_fixer(file_values['e_sw_off_from_e_sw_off_150'],
    #                                                               file_values['ic_from_e_sw_off_150'],
    #                                                               file_values['e_rg_from_e_off_150'],
    #                                                               file_values['ic_from_e_sw_off_150'][x])


def esw_rg_fixer(esw_ic_esw, ic_ic_esw, esw_rg_esw, ic):
    baseline = sp.UnivariateSpline(ic_ic_esw, esw_ic_esw)
    for x in range(0, len(esw_rg_esw)):
        esw_rg_esw[x] = esw_rg_esw[x] / float(baseline(ic))
    return esw_rg_esw


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
