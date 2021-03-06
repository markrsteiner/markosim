import numpy as np
import scipy.interpolate as sp
import os.path
import pandas as pd
import csv
import original_sim
import mark_sim
import time
import math
import xlsxwriter


def is_multiple_input(input_file):
    try:
        if len(input_file['Vcc [V]']) > 1:  # checks to see if there is more than one iteration of input values
            return True
    except:
        return False


def vcc_value_decoder(vcc_value):
    if vcc_value == 650:
        return 300
    if vcc_value == 1200:
        return 600
    return False


def m_sim_runner(file_values, input_file_values):
    if type(input_file_values['Vcc [V]']) is np.ndarray:
        output_file_temp_3 = []
        input_file_temp_2 = []
        for x in range(len(input_file_values['Vcc [V]'])):
            input_file_values_temp_1 = [y[x] for y in input_file_values.values()]
            input_file_values_temp_2 = [y for y in input_file_values.keys()]
            input_file_values_temp = {input_file_values_temp_2[x]: input_file_values_temp_1[x] for x in range(len(input_file_values_temp_1))}
            input_file_temp_2.append(input_file_values_temp_1)

            output_file = original_sim.m_sim_output_calc(file_values, input_file_values_temp)

            output_file_temp_1 = [math.floor(y * 100) / 100 for y in output_file.values()]  # limits output values to 2 decimal places
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


def tj_hold_runner(file_values, input_file_values):
    if len(input_file_values['Vcc [V]']) > 1:
        output_file_temp_3 = []
        input_file_temp_2 = []
        for x in range(len(input_file_values['Vcc [V]'])):
            input_file_values_temp_1 = [y[x] for y in input_file_values.values()]
            input_file_values_temp_2 = [y for y in input_file_values.keys()]
            input_file_values_temp = {input_file_values_temp_2[x]: input_file_values_temp_1[x] for x in range(len(input_file_values_temp_1))}
            input_file_temp_2.append(input_file_values_temp_1)

            output_file = original_sim.m_sim_output_calc(file_values, input_file_values_temp)
            MaxTemp = max(output_file['Tj_max_IGBT'], output_file['Tj_Max_FWD'])

            while (MaxTemp < 149.999) or (MaxTemp > 150.001):
                output_file = []
                increment = (150 - MaxTemp)
                if (increment > 100) or (increment < -100):
                    if (increment > 100):
                        increment = 50
                    else:
                        incremement = -50
                input_file_values_temp['input_ic_peak'] += increment

                output_file = original_sim.m_sim_output_calc(file_values, input_file_values_temp)
                MaxTemp = output_file['Tj_max_IGBT']

            output_file_temp_1 = [math.floor(y * 100) / 100 for y in output_file.values()]
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


def mark_sim_runner(file_values, input_file_values):
    if len(input_file_values['Vcc [V]']) > 1:
        output_file_temp_3 = []
        input_file_temp_2 = []
        for x in range(len(input_file_values['Vcc [V]'])):
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
    columns = ['Vcc [V]',
               'Io [Apk]',
               'PF [cos(\u03D5)]',
               'Mod. Depth',
               'fc [kHz]',
               'fo [Hz]',
               'rg on [\u03A9]',
               'rg off [\u03A9]',
               'Ts [\u00B0C]',
               'P Total IGBT [W]',
               'P Cond IGBT [W]',
               'Psw IGBT [W]',
               'Psw,on IGBT [W]',
               'Psw,off IGBT [W]',
               'ΔT\u2C7C ave. IGBT [K]',
               'T\u2C7C ave. IGBT [\u00B0C]',
               'ΔT\u2C7C Max_IGBT [K]',
               'T\u2C7C Max IGBT [\u00B0C]',
               'Tc ave. [\u00B0C]',
               'P Total FWD [W]',
               'P Cond FWD [W]',
               'Prr FWD [W]',
               'ΔT\u2C7C Ave FWD [K]',
               'T\u2C7C Ave FWD [\u00B0C]',
               'ΔT\u2C7C Max FWD [K]',
               'T\u2C7C Max FWD [\u00B0C]'
               ]
    output_file_name = 'output' + time.strftime("__%b_%d__%H_%M_%S") + '.xlsx'
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in output_file.items()]), columns=columns).T
    df.to_excel(output_file_name)
    f = open(output_file_name)
    f.close()


def input_file_reader():
    input_file = 'input_file.xlsx'

    row_list = [['Vcc [V]',
                 'Io [Apk]',
                 'PF [cos(\u03D5)]',
                 'Mod. Depth',
                 'fc [kHz]',
                 'fo [Hz]',
                 'rg on [\u03A9]',
                 'rg off [\u03A9]',
                 'Ts [\u00B0C]'
                 ]]

    if not os.path.exists(input_file):
        workbook = xlsxwriter.Workbook(input_file)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 20)
        row_list_map = row_list[0]
        worksheet.write(0, 0, "Iteration")
        worksheet.write(0, 1, "1")
        for x in range(len(row_list_map)):
            worksheet.write(0, x + 1, row_list_map[x])
        workbook.close()

    row_list = row_list[0]
    value_dict = {}
    for x in range(len(row_list)):
        value_dict[row_list[x]] = pull_data_from_column(input_file, row_list[x], None)
    for x in range(len(row_list)):
        if len(value_dict[row_list[x]]) == 1:
            value_dict[row_list[x]] = value_dict[row_list[x]][0]
    return value_dict


def module_file_reader(module_file):
    # module_string = 'module_file_revised.csv'
    module_string = module_file

    row_list = [["Module Name",
                 "IC - IC VCE",
                 "VCE - IC VCE",
                 "IF - IF VF",
                 "VF - IF VF",
                 "IC - IC ESWON",
                 "ESWON - IC ESWON",
                 "IC - IC ESWOFF",
                 "ESWOFF - IC ESWOFF",
                 "IC - IC ERR",
                 "ERR - IC ERR",
                 "ESWON - ESWON RGON",
                 "RGON - ESWON RGON",
                 "ESWOFF - ESWOFF RGOFF",
                 "RGOFF - ESWOFF RGOFF",
                 "ERR - ERR RGON",
                 "RGON - ERR RGON",
                 "IGBT R Values",
                 "IGBT T Values",
                 "FWD R Values",
                 "FWD T Values",
                 "IGBT RTH DC",
                 "FWD RTH DC",
                 "Module RTH DC",
                 "Nameplate VCC",
                 "Nameplate Current"
                 ]]

    # if not os.path.exists(module_file) and not os.path.exists(module_string):
    #     with open(module_file, 'w+') as file:
    #         writer = csv.writer(file)
    #         writer.writerows(row_list)
    #     file.close()

    if not os.path.exists(module_file):
        workbook = xlsxwriter.Workbook(module_file)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 20)
        row_list_map = row_list[0]
        for x in range(len(row_list_map)):
            worksheet.write(0, x + 1, row_list_map[x])
        workbook.close()

    row_list = row_list[0]
    value_dict = {}

    for x in range(len(row_list)):
        # value_dict[row_list[x]] = pull_data_from_column('module_file_revised.csv', row_list[x])
        value_dict[row_list[x]] = pull_data_from_column(module_string, row_list[x], None)
    for x in range(np.size(row_list)):
        if np.size(value_dict[row_list[x]]) == 1:
            value_dict[row_list[x]] = value_dict[row_list[x]][0]
    return value_dict


def module_file_updated_writer(file_values):
    column_list = ["Module Name",
                   "IC - IC VCE",
                   "VCE - IC VCE",
                   "IF - IF VF",
                   "VF - IF VF",
                   "IC - IC ESWON",
                   "ESWON - IC ESWON",
                   "IC - IC ESWOFF",
                   "ESWOFF - IC ESWOFF",
                   "IC - IC ERR",
                   "ERR - IC ERR",
                   "ESWON - ESWON RGON",
                   "RGON - ESWON RGON",
                   "ESWOFF - ESWOFF RGOFF",
                   "RGOFF - ESWOFF RGOFF",
                   "ERR - ERR RGON",
                   "RGON - ERR RGON",
                   "IGBT R Values",
                   "IGBT T Values",
                   "FWD R Values",
                   "FWD T Values",
                   "IGBT RTH DC",
                   "FWD RTH DC",
                   "Module RTH DC",
                   "Nameplate VCC",
                   "Nameplate Current"
                   ]

    module_file = 'module_file_revised.xlsx'
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in file_values.items()]), columns=column_list)
    df.to_excel(module_file)


def pull_data_from_column(module_file, column_string, indexcol):
    df = pd.read_excel(module_file, index_col=indexcol)
    x = df[column_string].as_matrix()
    # df.dropna()
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
        esw = np.interp(tj_in, grid_tj, grid_z0)
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
    baseline = sp.UnivariateSpline(ic_ic_esw, esw_ic_esw)
    baseline_energy = float(baseline(ic))
    for x in range(0, len(esw_rg_esw)):
        esw_rg_esw[x] = esw_rg_esw[x] / float(baseline_energy)
    return esw_rg_esw


def file_value_checker(file_values):
    threshold = 10
    current_value = file_values["Nameplate Current"]

    file_values["IC - IC VCE"], file_values["VCE - IC VCE"] = array_flipper(file_values["IC - IC VCE"], file_values["VCE - IC VCE"])
    file_values["IF - IF VF"], file_values["VF - IF VF"] = array_flipper(file_values["IF - IF VF"], file_values["VF - IF VF"])
    file_values["IC - IC ESWON"], file_values["ESWON - IC ESWON"] = array_flipper(file_values["IC - IC ESWON"], file_values["ESWON - IC ESWON"])
    file_values["IC - IC ESWOFF"], file_values["ESWOFF - IC ESWOFF"] = array_flipper(file_values["IC - IC ESWOFF"], file_values["ESWOFF - IC ESWOFF"])
    file_values["IC - IC ERR"], file_values["ERR - IC ERR"] = array_flipper(file_values["IC - IC ERR"], file_values["ERR - IC ERR"])
    file_values["RGON - ESWON RGON"], file_values["ESWON - ESWON RGON"] = array_flipper(file_values["RGON - ESWON RGON"], file_values["ESWON - ESWON RGON"])
    file_values["RGOFF - ESWOFF RGOFF"], file_values["ESWOFF - ESWOFF RGOFF"] = array_flipper(file_values["RGOFF - ESWOFF RGOFF"], file_values["ESWOFF - ESWOFF RGOFF"])
    file_values["RGON - ERR RGON"], file_values["ERR - ERR RGON"] = array_flipper(file_values["RGON - ERR RGON"], file_values["ERR - ERR RGON"])

    file_values["ESWON - ESWON RGON"] = esw_rg_checker(file_values["ESWON - ESWON RGON"], file_values["ESWON - IC ESWON"], file_values["IC - IC ESWON"],
                                                       current_value, threshold)

    file_values["ESWOFF - IC ESWOFF"] = esw_rg_checker(file_values["ESWOFF - IC ESWOFF"], file_values["ESWOFF - IC ESWOFF"], file_values["IC - IC ESWOFF"],
                                                       current_value, threshold)
    file_values["ERR - ERR RGON"] = esw_rg_checker(file_values["ERR - ERR RGON"], file_values["ERR - IC ERR"], file_values["IC - IC ERR"], current_value,
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
