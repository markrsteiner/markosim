import numpy as np
import math
import scipy.interpolate as sp

module_name = "CM600DX-24T"
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


ic_from_vcesat_25 = [1.1786726, 16.574959, 55.131268, 119.9185, 266.5271, 451.72974, 619.98773, 743.478, 953.41693]
vcesat_from_vcesat_25 = [0.6433621, 0.7273233, 0.82184154, 0.9583944, 1.1511298, 1.3719499, 1.5157973, 1.624549, 1.7999865]

# ic_from_vcesat_125 = [13.585544, 58.255844, 127.64845, 280.38892, 609.0736, 842.097, 1195.4861]
# vcesat_from_vcesat_125 = [0.55248886, 0.7589134, 0.9444309, 1.217604, 1.6975843, 2.016446, 2.5069878]
ic_from_vcesat_125 = [0, 7, 30, 60, 120, 300, 450, 600, 1200]
vcesat_from_vcesat_125 = [0.4212, 0.468, 0.64, 0.76, 0.915, 1.255, 1.49, 1.7, 2.497]
#

# ic_from_vcesat_150 = [-0.228579, 16.686268, 41.30323, 107.61698, 172.38434, 357.51346, 737.1096, 1196.9648]
# vcesat_from_vcesat_150 = [0.4020985, 0.5315188, 0.6959267, 0.86395264, 1.0354706, 1.3856615, 1.9601959, 2.6223772]
ic_from_vcesat_150 = [-0.228579, 16.686268, 17, 41.30323, 107.61698, 172.38434, 357.51346, 737.1096, 1196.9648]
vcesat_from_vcesat_150 = [0.4020985, 0.5315188, 0.54, 0.6959267, 0.86395264, 1.0354706, 1.3856615, 1.9601959, 2.6223772]
#

# ie_from_vecsat_25 = [-0.11870075, 20.927132, 40.34318, 118.18826, 257.71063, 426.48615, 869.5866, 1199.0942]
# vecsat_from_vecsat_25 = [0.666446, 0.7615978, 0.8646726, 1.0233397, 1.2376053, 1.425506, 1.8279268, 2.0953908]
ie_from_vecsat_25 = [-0.11870075, 20.927132, 21, 40.34318, 118.18826, 257.71063, 426.48615, 869.5866, 1199.0942]
vecsat_from_vecsat_25 = [0.666446, 0.7615978, 0.77, 0.8646726, 1.0233397, 1.2376053, 1.425506, 1.8279268, 2.0953908]
#

# ie_from_vecsat_125 = [6.483322, 25.872995, 61.50583, 124.74319, 273.98016, 497.89877, 1044.8606, 1210.433]
# vecsat_from_vecsat_125 = [0.5185062, 0.65856904, 0.79602045, 0.94145, 1.1980059, 1.4943329, 2.0131977, 2.1376843]
ie_from_vecsat_125 = [0, 11.4, 32.4, 60.2, 122, 299.8, 451.2, 596.2, 1197.8]
vecsat_from_vecsat_125 = [0.527690843, 0.586323159, 0.693392136, 0.785864402, 0.938353106, 1.23560378, 1.437053455,
                          1.597005917, 2.137743856]
#

ie_from_vecsat_150 = [3.2350664, 50.195343, 132.8657, 272.3636, 434.6275, 785.1546, 931.2225, 1088.6555, 1212.0176]
vecsat_from_vecsat_150 = [0.51850015, 0.714097, 0.9388233, 1.1874349, 1.3964593, 1.7960633, 1.9416492, 2.0925405, 2.1931694]

# ic_from_e_sw_on_125 = [61.337433, 323.9047, 421.82938, 501.46042, 585.3959, 738.20135, 958.8009,
#                        1200.9224]
# e_sw_on_from_e_sw_on_125 = [9.667346, 28.350306, 34.107265, 39.64698, 48.44535, 68.86626, 102.104546,
#                             138.92735]

ic_from_e_sw_on_125 = [0, 60, 300, 600, 1200]
e_sw_on_from_e_sw_on_125 = [0, 9.857142857, 26.77857143, 50.6, 139.15]

#

# e_sw_on_from_e_sw_on_150 = [146.0964, 112.42362, 79.94569, 49.748814, 42.253902, 36.171078, 28.133062,
#                             9.775968]
# e_sw_on_from_e_sw_on_150 = np.flipud(e_sw_on_from_e_sw_on_150)
# ic_from_e_sw_on_150 = [1200.9224, 993.23596, 796.31055, 597.2329, 526.21063, 454.1122, 321.7525, 60.261337]
# ic_from_e_sw_on_150 = np.flipud(ic_from_e_sw_on_150)
e_sw_on_from_e_sw_on_150 = [146.0964, 112.42362, 36.171078, 28.133062,
                            9.775968]
e_sw_on_from_e_sw_on_150 = np.flipud(e_sw_on_from_e_sw_on_150)
ic_from_e_sw_on_150 = [1200.9224, 993.23596, 454.1122, 321.7525, 60.261337]
ic_from_e_sw_on_150 = np.flipud(ic_from_e_sw_on_150)
#

# e_sw_off_from_e_sw_off_125 = [111.44603, 59.742023, 49.09708, 36.171078, 30.631365, 11.839783]
# e_sw_off_from_e_sw_off_125 = np.flipud(e_sw_off_from_e_sw_off_125)
# ic_from_e_sw_off_125 = [1199.8463, 674.71173, 550.9608, 349.731, 278.70868, 64.56572]
# ic_from_e_sw_off_125 = np.flipud(ic_from_e_sw_off_125)
e_sw_off_from_e_sw_off_125 = [0, 12.0964539, 32.98173759, 53.3, 111.1361702]
ic_from_e_sw_off_125 = [0, 60, 300, 600, 1200]
#

# e_sw_off_from_e_sw_off_150 = [131.54108, 74.84046, 61.37135, 54.31093, 42.145283, 36.605568, 30.522743,
#                               13.577732]
# e_sw_off_from_e_sw_off_150 = np.flipud(e_sw_off_from_e_sw_off_150)
# ic_from_e_sw_off_150 = [1200.9224, 719.9078, 597.2329, 524.0584, 355.11145, 289.46964, 227.0561, 62.41353]
# ic_from_e_sw_off_150 = np.flipud(ic_from_e_sw_off_150)
e_sw_off_from_e_sw_off_150 = [131.54108, 74.84046, 36.605568, 30.522743,
                              13.577732]
e_sw_off_from_e_sw_off_150 = np.flipud(e_sw_off_from_e_sw_off_150)
ic_from_e_sw_off_150 = [1200.9224, 719.9078, 289.46964, 227.0561, 62.41353]
ic_from_e_sw_off_150 = np.flipud(ic_from_e_sw_off_150)
#

# e_rr_from_e_rr_125 = [50.1833, 47.033264, 42.362526, 36.714188, 28.893415, 18.68296]
# e_rr_from_e_rr_125 = np.flipud(e_rr_from_e_rr_125)
# ic_from_e_rr_125 = [1200.9224, 994.3121, 671.48346, 323.9047, 185.0884, 63.489624]
# ic_from_e_rr_125 = np.flipud(ic_from_e_rr_125)

e_rr_from_e_rr_125 = [0, 18.87286064, 36.0207824, 41.5, 50.32762836]
ic_from_e_rr_125 = [0, 60, 300, 600, 1200]

#

# e_rr_from_e_rr_150 = [54.31093, 51.052273, 47.250507, 40.624577, 32.369316, 20.96402]
# e_rr_from_e_rr_150 = np.flipud(e_rr_from_e_rr_150)
# ic_from_e_rr_150 = [1200.9224, 823.2129, 546.65643, 330.36127, 192.62106, 59.18524]
# ic_from_e_rr_150 = np.flipud(ic_from_e_rr_150)
e_rr_from_e_rr_150 = [54.31093, 51.052273, 47.250507, 32.369316, 20.96402]
e_rr_from_e_rr_150 = np.flipud(e_rr_from_e_rr_150)
ic_from_e_rr_150 = [1200.9224, 823.2129, 546.65643, 192.62106, 59.18524]
ic_from_e_rr_150 = np.flipud(ic_from_e_rr_150)
#

# e_on_from_e_on_125 = [223.3369, 171.42764, 123.038124, 82.36316, 58.172634, 50.465195]
# e_on_from_e_on_125 = np.flipud(e_on_from_e_on_125)
# e_rg_from_e_on_125 = [6.800042, 4.7779374, 3.1743867, 1.8329057, 1.128005, 1.028435]
# e_rg_from_e_on_125 = np.flipud(e_rg_from_e_on_125)
e_on_from_e_on_125 = [1, 1.466798419, 3.33201581, 4.399209486]
e_rg_from_e_on_125 = [1, 1.6, 4.7, 6.8]
#

# e_on_from_e_on_150 = [50.46355, 74.12476, 114.44221, 168.78766, 212.80153, 230.51366]
# e_rg_from_e_on_150 = [0.9909351, 1.6021153, 2.7748663, 4.459335, 6.0881295, 6.7746415]
e_on_from_e_on_150 = [50.46355, 74.12476, 212.80153, 230.51366]
e_rg_from_e_on_150 = [0.9909351, 1.6021153, 6.0881295, 6.7746415]
#

# e_off_from_e_off_125 = [64.02215, 56.36422, 52.073097, 51.361603, 53.44001]
# e_off_from_e_off_125 = np.flipud(e_off_from_e_off_125)
# e_rg_from_e_off_125 = [6.777679, 3.809356, 1.7658453, 1.509635, 0.99701905]
# e_rg_from_e_off_125 = np.flipud(e_rg_from_e_off_125)

e_off_from_e_off_125 = [1, 0.966979362, 1.106941839, 1.195497186]
e_rg_from_e_off_125 = [1, 1.6, 4.7, 6.8]

#

e_off_from_e_off_150 = [61.8439, 61.515644, 67.96067, 75.22715]
e_rg_from_e_off_150 = [1.0090503, 1.5090686, 4.764959, 6.7895536]

# e_rr_from_e_rg_125 = [41.360477, 40.8577, 33.219738, 23.672972, 19.906239]
# e_rg_from_e_rg_125 = [1.0039428, 1.5164709, 3.004397, 4.8799295, 6.81764]

e_rr_from_e_rg_125 = [1, 0.977590361, 0.58606024, 0.474939759]
e_rg_from_e_rg_125 = [1, 1.6, 4.7, 6.8]

#

# e_rr_from_e_rg_150 = [23.932295, 25.81484, 26.486122, 30.9969, 37.07729, 41.94559, 46.28732, 48.187645]
# e_rr_from_e_rg_150 = np.flipud(e_rr_from_e_rg_150)
# e_rg_from_e_rg_150 = [6.804915, 5.81731, 5.1547728, 4.217021, 3.1416817, 2.3726602, 1.5724181, 0.99106205]
# e_rg_from_e_rg_150 = np.flipud(e_rg_from_e_rg_150)
e_rr_from_e_rg_150 = [23.932295, 25.81484, 46.28732, 48.187645]
e_rr_from_e_rg_150 = np.flipud(e_rr_from_e_rg_150)
e_rg_from_e_rg_150 = [6.804915, 5.81731, 1.5724181, 0.99106205]
e_rg_from_e_rg_150 = np.flipud(e_rg_from_e_rg_150)
#

# e_on_from_e_on_150 = esw_rg_fixer(e_sw_on_from_e_sw_on_150, ic_from_e_sw_on_150, e_on_from_e_on_150, 600)
# e_off_from_e_off_150 = esw_rg_fixer(e_sw_off_from_e_sw_off_150, ic_from_e_sw_off_150, e_off_from_e_off_150, 600)
# e_rr_from_e_rg_150 = esw_rg_fixer(e_rr_from_e_rr_150, ic_from_e_rr_150, e_rr_from_e_rg_150, 600)

# e_on_from_e_on_125 = esw_rg_fixer(e_sw_on_from_e_sw_on_125, ic_from_e_sw_on_125, e_on_from_e_on_125, 600)
# e_off_from_e_off_125 = esw_rg_fixer(e_sw_off_from_e_sw_off_125, ic_from_e_sw_off_125, e_off_from_e_off_125, 600)
# e_rr_from_e_rg_125 = esw_rg_fixer(e_rr_from_e_rr_125, ic_from_e_rr_125, e_rr_from_e_rg_125, 600)

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

input_bus_voltage = 600
input_ic_arms = 300 * math.sqrt(2)
power_factor = 0.8
mod_depth = 1
freq_carrier = 5  # kHz
freq_output = 60
input_tc = 100
input_rg_on = 1
input_rg_off = 1

power_factor_phi = math.acos(power_factor) * 180 / math.pi
step = 1
degree_count = 1.0

initflag = True

# while (abs(tj_try_igbt - tj_igbt) > 0.1):
print(tj_try_igbt - tj_igbt)
p_igbt_cond = []
e_sw_on = []
e_sw_off = []
e_sw_on_Eoff = []
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
if initflag:
    tj_try_igbt = 125
    tj_try_fwd = 125
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
        VceAtIc = float(vce_from_tj_ic_solver(ic_from_vcesat_25, vcesat_from_vcesat_25, ic_from_vcesat_125, vcesat_from_vcesat_125, ic_from_vcesat_150, vcesat_from_vcesat_150, tj_try_igbt, igbt_current, 2400))
        # vcesatcurve = sp.interp1d(ic_from_vcesat_125, vcesat_from_vcesat_125, kind='linear')
        # VceAtIc = vcesatcurve(igbt_current)
        dtTr1Pvce = igbt_current * time_division * VceAtIc * output_voltage[0] / input_bus_voltage / 1000.0
        ESwOn = esw_solver(ic_from_e_sw_on_125, e_sw_on_from_e_sw_on_125, ic_from_e_sw_on_150, e_sw_on_from_e_sw_on_150, tj_try_igbt, igbt_current, 2400)
        # ESwOncurve = sp.interp1d(ic_from_e_sw_on_125, e_sw_on_from_e_sw_on_125)
        # ESwOn = ESwOncurve(igbt_current)
        ESwOff = esw_solver(ic_from_e_sw_off_125, e_sw_off_from_e_sw_off_125, ic_from_e_sw_off_150, e_sw_off_from_e_sw_off_150, tj_try_igbt, igbt_current, 2400)
        # ESwoffcurve = sp.interp1d(ic_from_e_sw_off_125, e_sw_off_from_e_sw_off_125, kind='linear')
        # ESwOff = ESwoffcurve(igbt_current)
        if 1.0 > output_voltage[0] / input_bus_voltage > 0.0:
            dtTr1EonFcoRatio = switches_per_cycle_per_degree * ESwOn
            dtTr1EoffFcoRatio = switches_per_cycle_per_degree * ESwOff
    if diode_current >= 0.0:
        VfAtIc = vce_from_tj_ic_solver(ie_from_vecsat_25, vecsat_from_vecsat_25, ie_from_vecsat_125, vecsat_from_vecsat_125, ie_from_vecsat_150, vecsat_from_vecsat_150, tj_try_fwd, diode_current, 2400)
        # VfAtIccurve = sp.interp1d(ie_from_vecsat_125, vecsat_from_vecsat_125)
        # VfAtIc = VfAtIccurve(diode_current)
        dtDi1Pvce = diode_current * time_division * VfAtIc * output_voltage[0] / input_bus_voltage / 1000.0
        ErrFromIc = esw_solver(ic_from_e_rr_125, e_rr_from_e_rr_125, ic_from_e_rr_150, e_rr_from_e_rr_125, tj_try_fwd, diode_current, 2400)
        # ErrFromIccurve = sp.interp1d(ic_from_e_rr_125, e_rr_from_e_rr_125)
        # ErrFromIc = ErrFromIccurve(diode_current)
    if 1.0 > output_voltage[0] / input_bus_voltage > 0.0:
        dtDi1ErrFcoRatio = switches_per_cycle_per_degree * ErrFromIc

    VccRatio = input_bus_voltage / vcc_value

    eswOnFromRgEswOn = esw_solver(e_rg_from_e_on_125, e_on_from_e_on_125, e_rg_from_e_on_150, e_on_from_e_on_150, tj_try_igbt, input_rg_on, 10)
    # eswOnFromRgEswOncurve = sp.interp1d(e_rg_from_e_on_125, e_on_from_e_on_125)
    # eswOnFromRgEswOn = eswOnFromRgEswOncurve(input_rg_on)
    eswOffFromRgEswOff = esw_solver(e_rg_from_e_off_125, e_off_from_e_off_125, e_rg_from_e_off_150, e_off_from_e_off_150, tj_try_igbt, input_rg_off, 10)
    # eswoffFromRgEswoffcurve = sp.interp1d(e_rg_from_e_off_125, e_off_from_e_off_125)
    # eswOffFromRgEswOff = eswoffFromRgEswoffcurve(input_rg_off)
    errFromRgErr = esw_solver(e_rg_from_e_rg_125, e_rr_from_e_rg_125, e_rg_from_e_rg_150, e_rr_from_e_rg_150, tj_try_fwd, input_rg_on, 10)
    # errFromRgErrcurve = sp.interp1d(e_rg_from_e_rg_125, e_rr_from_e_rg_125)
    # errFromRgErr = errFromRgErrcurve(input_rg_off)
    # debug
    output_current_tot.append(output_current)
    output_voltage_tot.append(output_voltage[0])

    p_igbt_cond.append(dtTr1Pvce * freq_output / 1000.0)
    e_sw_on.append(dtTr1EonFcoRatio * freq_output / 1000.0 * VccRatio * eswOnFromRgEswOn)
    e_sw_off.append(dtTr1EoffFcoRatio * freq_output / 1000.0 * VccRatio * eswOffFromRgEswOff)
    e_sw_on_Eoff.append((dtTr1EonFcoRatio * VccRatio * eswOnFromRgEswOn + dtTr1EoffFcoRatio * VccRatio * eswOffFromRgEswOff) * freq_output / 1000.0)
    p_fwd_cond.append(dtDi1Pvce * freq_output / 1000.0)
    e_sw_err.append(dtDi1ErrFcoRatio * freq_output / 1000.0 * VccRatio * errFromRgErr)
    p_igbt.append((dtTr1EonFcoRatio * VccRatio * eswOnFromRgEswOn + dtTr1EoffFcoRatio * VccRatio * eswOffFromRgEswOff) * freq_output / 1000.0 + dtTr1Pvce * freq_output / 1000.0)
    p_fwd.append(dtDi1ErrFcoRatio * errFromRgErr * freq_output / 1000.0 * VccRatio + dtDi1Pvce * freq_output / 1000.0)
    # p_arm.append((dtTr1EonFcoRatio * VccRatio * eswOnFromRgEswOn + dtTr1EoffFcoRatio * VccRatio * eswOffFromRgEswOff) * freq_output / 1000.0 + dtTr1Pvce * freq_output / 1000.0 + (
    #         dtDi1ErrFcoRatio * errFromRgErr * freq_output / 1000.0 * VccRatio + dtDi1Pvce * freq_output / 1000.0))

    degree_count += step

delta_tj__igbt = np.sum(p_igbt) * rth_tr_value
delta_tj__fwd = np.sum(p_fwd) * rth_di_value
delta_tc = np.sum(p_arm) * thermal_contact_resistance_value
tj_igbt = delta_tj__igbt + delta_tc + input_tc
tj_fwd = delta_tj__fwd + delta_tc + input_tc

print('Tj tried to be ' + str(tj_igbt))
initflag = False

# while loop end
p_igbt_cond_total = np.sum(p_igbt_cond)
e_sw_on_total = np.sum(e_sw_on)
e_sw_off_total = np.sum(e_sw_off)
p_igbt_total = np.sum(p_igbt)
p_fwd_cond_total = np.sum(p_fwd_cond)
e_sw_err_total = np.sum(e_sw_err)
print('Tj settled at ' + str(tj_igbt))
print('P cond IGBT is ' + str(p_igbt_cond_total))
print('ESwOn losses are ' + str(e_sw_on_total))
print('ESwOff losses are ' + str(e_sw_off_total))
print('Total IGBT losses ' + str(p_igbt_total))
print('Tj diode is ' + str(tj_fwd))
print('Diode switch losses are ' + str(e_sw_err_total))
print('Diode cond losses are ' + str(p_fwd_cond_total))
print(p_igbt_cond)
print(output_current_tot)
print(output_voltage_tot)
