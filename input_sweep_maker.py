import sim_tools
import scipy.interpolate as sp
import pandas as pd
import numpy as np

iostep = 6
vstep = 3
pfstep = 7
mstep = 3
fcstep = 3
fostep = 4
tcstep = 2
rgonstep = 3
rgoffstep = 3

io = []
v = []
pf = []
m = []
fc = []
fo = []
tc = []
rgon = []
rgoff = []
tjtest = []

iolist = np.linspace(600, 1200, iostep)
vlist = np.linspace(500, 1000, vstep)
pflist = np.linspace(-1, 1, pfstep)
mlist = np.linspace(0, 1, mstep)
fclist = np.linspace(5, 20, fcstep)
folist = np.linspace(1, 120, fostep)
tclist = np.linspace(50, 150, tcstep)
rgonlist = np.linspace(1.6, 6.8, rgonstep)
rgofflist = np.linspace(1.6, 6.8, rgoffstep)

amount = iostep * vstep * pfstep * mstep * fcstep * fostep * tcstep * rgonstep * rgoffstep
time = amount * 0.266 / 60 / 60
print(str(time) + ' minutes')
if time < 15:
    for io1 in range(iostep):
        for v1 in range(vstep):
            for pf1 in range(pfstep):
                for m1 in range(mstep):
                    for fc1 in range(fcstep):
                        for fo1 in range(fostep):
                            for tc1 in range(tcstep):
                                for rgon1 in range(rgonstep):
                                    for rgoff1 in range(rgoffstep):
                                        io.append(iolist[io1])
                                        v.append(vlist[v1])
                                        pf.append(pflist[pf1])
                                        m.append(mlist[m1])
                                        fc.append(fclist[fc1])
                                        fo.append(folist[fo1])
                                        tc.append(tclist[tc1])
                                        rgon.append(rgonlist[rgon1])
                                        rgoff.append(rgofflist[rgoff1])
                                        tjtest.append(125)

results = {}

results['input_ic_arms'] = io
results['input_bus_voltage'] = v
results['power_factor'] = pf
results['mod_depth'] = m
results['freq_carrier'] = fc
results['freq_output'] = fo
results['input_tc'] = tc
results['input_rg_on'] = rgon
results['input_rg_off'] = rgoff
results['tj_test'] = tjtest

dog = pd.DataFrame.from_dict(results)
dog.to_csv('input_list.csv')
