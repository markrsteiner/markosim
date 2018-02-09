import sim_tools
import cProfile

file_values = sim_tools.module_file_reader()

input_file_values = sim_tools.input_file_reader()
file_values = sim_tools.file_value_checker(file_values)
# m_sim_results = sim_tools.m_sim_runner(file_values, input_file_values)
cProfile.run("sim_tools.mark_sim_runner(file_values, input_file_values)")

#     mark_sim_results = sim_tools.mark_sim_runner(file_values, input_file_values)
#     sim_tools.output_file_writer(mark_sim_results)
#
# sim_tools.module_file_updated_writer(file_values)
