import numpy as np
import scipy.interpolate as sp


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
                                       grid_z0)
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
    vce_for_temp = sp.UnivariateSpline(grid_tj, grid_z0)
    return vce_for_temp(tj_in)


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
