from original_sim import m_sim_output_calc
from mark_sim import mark_sim_output_calc
import numpy as np
import math
import sim_tools
import tcmax

#### device data

ic_from_vcesat_25 = [1.1786726, 16.574959, 55.131268, 119.9185, 266.5271, 451.72974, 619.98773, 743.478, 953.41693]
vcesat_from_vcesat_25 = [0.6433621, 0.7273233, 0.82184154, 0.9583944, 1.1511298, 1.3719499, 1.5157973, 1.624549,
                         1.7999865]

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
vecsat_from_vecsat_150 = [0.51850015, 0.714097, 0.9388233, 1.1874349, 1.3964593, 1.7960633, 1.9416492, 2.0925405,
                          2.1931694]

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

e_on_from_e_on_150 = sim_tools.esw_rg_fixer(e_sw_on_from_e_sw_on_150, ic_from_e_sw_on_150, e_on_from_e_on_150, 600)
e_off_from_e_off_150 = sim_tools.esw_rg_fixer(e_sw_off_from_e_sw_off_150, ic_from_e_sw_off_150, e_off_from_e_off_150,
                                              600)
e_rr_from_e_rg_150 = sim_tools.esw_rg_fixer(e_rr_from_e_rr_150, ic_from_e_rr_150, e_rr_from_e_rg_150, 600)

# e_on_from_e_on_125 = esw_rg_fixer(e_sw_on_from_e_sw_on_125, ic_from_e_sw_on_125, e_on_from_e_on_125, 600)
# e_off_from_e_off_125 = esw_rg_fixer(e_sw_off_from_e_sw_off_125, ic_from_e_sw_off_125, e_off_from_e_off_125, 600)
# e_rr_from_e_rg_125 = esw_rg_fixer(e_rr_from_e_rr_125, ic_from_e_rr_125, e_rr_from_e_rg_125, 600)

#####################

transient_thermal_values = {}

transient_thermal_values['igbt_r1_per_r0_value'] = 0.012413952
transient_thermal_values['igbt_r2_per_j0_value'] = 0.073850782
transient_thermal_values['igbt_r2_per_j0_value'] = 0.350547328
transient_thermal_values['igbt_r4_per_r1_value'] = 0.563187938
transient_thermal_values['igbt_t1_per_j1_value'] = 0.0000196
transient_thermal_values['igbt_t2_per_t1_value'] = 0.001398007
transient_thermal_values['igbt_t3_value'] = 0.017902919
transient_thermal_values['igbt_t4_value'] = 0.094420415

transient_thermal_values['fwd_r1a_per_rd0_value'] = 0.012413952
transient_thermal_values['fwd_r2a_per_jd0_value'] = 0.073850782
transient_thermal_values['fwd_r3a_per_td0_value'] = 0.350547328
transient_thermal_values['fwd_r4a_per_rd1_value'] = 0.563187938
transient_thermal_values['fwd_t1a_per_jd1_value'] = .0000196
transient_thermal_values['fwd_t2a_per_td1_value'] = 0.001398007
transient_thermal_values['fwd_t3_value'] = 0.017902919
transient_thermal_values['fwd_t4_value'] = 0.094420415

transient_thermal_values['rth_tr_value'] = 0.048
transient_thermal_values['rth_di_value'] = 0.076
transient_thermal_values['rth_thermal_contact'] = 0.023

vcc_value = 600.0

input_bus_voltage = 600
input_ic_arms = 300
power_factor = 0.8
mod_depth = 1
freq_carrier = 5  # kHz
freq_output = 60
input_tc = 100
input_rg_on = 1
input_rg_off = 1

# set floats for easy calculations
input_bus_voltage = float(input_bus_voltage)
input_ic_arms = float(input_ic_arms)
power_factor = float(power_factor)
mod_depth = float(mod_depth)
freq_carrier = float(freq_carrier)
freq_output = float(freq_output)
input_tc = float(input_tc)
input_rg_on = float(input_rg_on)
input_rg_off = float(input_rg_off)

tj_test = 125

m_sim_results = m_sim_output_calc(ic_from_vcesat_125, vcesat_from_vcesat_125,
                                  ic_from_vcesat_150, vcesat_from_vcesat_150,
                                  ie_from_vecsat_125, vecsat_from_vecsat_125,
                                  ie_from_vecsat_150, vecsat_from_vecsat_150,
                                  ic_from_e_sw_on_125, e_sw_on_from_e_sw_on_125,
                                  ic_from_e_sw_on_150, e_sw_on_from_e_sw_on_150,
                                  ic_from_e_sw_off_125, e_sw_off_from_e_sw_off_125,
                                  ic_from_e_sw_off_150, e_sw_off_from_e_sw_off_150,
                                  ic_from_e_rr_125, e_rr_from_e_rr_125,
                                  ic_from_e_rr_150, e_rr_from_e_rr_150,
                                  e_rg_from_e_on_125, e_on_from_e_on_125,
                                  e_rg_from_e_on_150, e_on_from_e_on_150,
                                  e_rg_from_e_off_125, e_off_from_e_off_125,
                                  e_rg_from_e_off_150, e_off_from_e_off_150,
                                  e_rg_from_e_rg_125, e_rr_from_e_rg_125,
                                  e_rg_from_e_rg_150, e_rr_from_e_rg_150,
                                  tj_test,
                                  input_bus_voltage,
                                  input_ic_arms,
                                  power_factor,
                                  mod_depth,
                                  freq_carrier,
                                  freq_output,
                                  input_tc,
                                  input_rg_on,
                                  input_rg_off,
                                  vcc_value,
                                  transient_thermal_values)

print(m_sim_results)
run_mine = True

if run_mine:
    mark_sim_results = mark_sim_output_calc(ic_from_vcesat_25, vcesat_from_vcesat_25,
                                            ie_from_vecsat_25, vecsat_from_vecsat_25,
                                            ic_from_vcesat_125, vcesat_from_vcesat_125,
                                            ic_from_vcesat_150, vcesat_from_vcesat_150,
                                            ie_from_vecsat_125, vecsat_from_vecsat_125,
                                            ie_from_vecsat_150, vecsat_from_vecsat_150,
                                            ic_from_e_sw_on_125, e_sw_on_from_e_sw_on_125,
                                            ic_from_e_sw_on_150, e_sw_on_from_e_sw_on_150,
                                            ic_from_e_sw_off_125, e_sw_off_from_e_sw_off_125,
                                            ic_from_e_sw_off_150, e_sw_off_from_e_sw_off_150,
                                            ic_from_e_rr_125, e_rr_from_e_rr_125,
                                            ic_from_e_rr_150, e_rr_from_e_rr_150,
                                            e_rg_from_e_on_125, e_on_from_e_on_125,
                                            e_rg_from_e_on_150, e_on_from_e_on_150,
                                            e_rg_from_e_off_125, e_off_from_e_off_125,
                                            e_rg_from_e_off_150, e_off_from_e_off_150,
                                            e_rg_from_e_rg_125, e_rr_from_e_rg_125,
                                            e_rg_from_e_rg_150, e_rr_from_e_rg_150,
                                            tj_test,
                                            input_bus_voltage,
                                            input_ic_arms,
                                            power_factor,
                                            mod_depth,
                                            freq_carrier,
                                            freq_output,
                                            input_tc,
                                            input_rg_on,
                                            input_rg_off,
                                            vcc_value,
                                            transient_thermal_values)

print(mark_sim_results)
# print(mark_sim_results['P_IGBT_for_Tcmax'])
# print(len(mark_sim_results['P_IGBT_for_Tcmax']))
