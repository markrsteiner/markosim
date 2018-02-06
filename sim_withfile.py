from original_sim import m_sim_output_calc
from mark_sim import mark_sim_output_calc
import sim_tools

file_values = sim_tools.module_file_reader()

file_values["igbt_r1_per_r0_value"]
file_values["igbt_r2_per_j0_value"]
file_values["igbt_r2_per_j0_value"]
file_values["igbt_r4_per_r1_value"]
file_values["igbt_t1_per_j1_value"]
file_values["igbt_t2_per_t1_value"]
file_values["igbt_t3_value"]
file_values["igbt_t4_value"]
file_values["fwd_r1a_per_rd0_value"]
file_values["fwd_r2a_per_jd0_value"]
file_values["fwd_r3a_per_td0_value"]
file_values["fwd_r4a_per_rd1_value"]
file_values["fwd_t1a_per_jd1_value"]
file_values["fwd_t2a_per_td1_value"]
file_values["fwd_t3_value"]
file_values["fwd_t4_value"]
file_values["rth_tr_value"]
file_values["rth_di_value"]
file_values["rth_thermal_contact"]
file_values["vcc_value"]

# e_on_from_e_on_150 = sim_tools.esw_rg_fixer(e_sw_on_from_e_sw_on_150, ic_from_e_sw_on_150, e_on_from_e_on_150, 600)
# e_off_from_e_off_150 = sim_tools.esw_rg_fixer(e_sw_off_from_e_sw_off_150, ic_from_e_sw_off_150, e_off_from_e_off_150,
#                                               600)
# e_rr_from_e_rg_150 = sim_tools.esw_rg_fixer(e_rr_from_e_rr_150, ic_from_e_rr_150, e_rr_from_e_rg_150, 600)

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

# file_version test

m_sim_results = m_sim_output_calc(file_values["ic_from_vcesat_125"], file_values["vcesat_from_vcesat_125"],
                                  file_values["ic_from_vcesat_150"],
                                  file_values["vcesat_from_vcesat_150"],
                                  file_values["ie_from_vecsat_125"],
                                  file_values["vecsat_from_vecsat_125"],
                                  file_values["ie_from_vecsat_150"],
                                  file_values["vecsat_from_vecsat_150"],
                                  file_values["ic_from_e_sw_on_125"],
                                  file_values["e_sw_on_from_e_sw_on_125"],
                                  file_values["ic_from_e_sw_on_150"],
                                  file_values["e_sw_on_from_e_sw_on_150"],
                                  file_values["ic_from_e_sw_off_125"],
                                  file_values["e_sw_off_from_e_sw_off_125"],
                                  file_values["ic_from_e_sw_off_150"],
                                  file_values["e_sw_off_from_e_sw_off_150"],
                                  file_values["ic_from_e_rr_125"],
                                  file_values["e_rr_from_e_rr_125"],
                                  file_values["ic_from_e_rr_150"],
                                  file_values["e_rr_from_e_rr_150"],
                                  file_values["e_rg_from_e_on_125"],
                                  file_values["e_on_from_e_on_125"],
                                  file_values["e_rg_from_e_on_150"],
                                  file_values["e_on_from_e_on_150"],
                                  file_values["e_rg_from_e_off_125"],
                                  file_values["e_off_from_e_off_125"],
                                  file_values["e_rg_from_e_off_150"],
                                  file_values["e_off_from_e_off_150"],
                                  file_values["e_rg_from_e_rg_125"],
                                  file_values["e_rr_from_e_rg_125"],
                                  file_values["e_rg_from_e_rg_150"],
                                  file_values["e_rr_from_e_rg_150"],
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
run_mine = False

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
