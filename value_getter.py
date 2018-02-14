import sim_tools
import scipy.interpolate as sp
import pandas as pd
import numpy as np

file_values = sim_tools.module_file_reader()
sim_tools.file_value_checker(file_values)

e_sw_off_from_e_sw_off_125 = file_values['e_sw_off_from_e_sw_off_125']
ic_from_e_sw_off_125 = file_values['ic_from_e_sw_off_125']
ic_from_e_sw_off_150 = file_values['ic_from_e_sw_off_150']
e_sw_off_from_e_sw_off_150 = file_values['e_sw_off_from_e_sw_off_150']

e_dict = sim_tools.esw_ic_maker(ic_from_e_sw_off_125, e_sw_off_from_e_sw_off_125, ic_from_e_sw_off_150, e_sw_off_from_e_sw_off_150, 2400)

g = (1200, 175)
spline = np.zeros(g)
# linear = [ 0 for __ in range(175)]

spl = sp.interp1d(ic_from_e_sw_off_125, e_sw_off_from_e_sw_off_125, kind='cubic')

rows = 121
columns = 35
spline = [[0 for x in range(columns)] for x in range(rows)]
currs = [[0 for x in range(columns)] for x in range(rows)]
temps = [[0 for x in range(columns)] for x in range(rows)]
c = 0
t = 0
for curr in range(0, 1200, 10):
    for temp in range(0, 175, 5):
        spline[c][t] = sim_tools.esw_solver(e_dict, temp, curr)
        currs[c][t] = curr
        temps[c][t] = temp
        t += 1
    t = 0
    c += 1

out = {}
out['spline'] = spline
# out['linear'] = linear

print(out)

columns = ['spline']

kitten = pd.DataFrame(spline)
kitten.to_csv('lin_v_spl.csv')

doggy = pd.DataFrame(currs)
doggy.to_csv('currs.csv')

potata = pd.DataFrame(temps)
potata.to_csv('temps.csv')
