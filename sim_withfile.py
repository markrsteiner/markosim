import sim_tools

file_values = sim_tools.module_file_reader()
input_file_values = sim_tools.input_file_reader()
sim_tools.file_value_checker(file_values)

m_sim_results = sim_tools.m_sim_runner(file_values, input_file_values)
sim_tools.output_file_writer(m_sim_results)

run_mine = True

if run_mine:
    mark_sim_results = sim_tools.mark_sim_runner(file_values, input_file_values)
    sim_tools.output_file_writer(mark_sim_results)

sim_tools.module_file_updated_writer(file_values)
