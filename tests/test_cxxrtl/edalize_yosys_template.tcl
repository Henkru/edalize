yosys -import
source edalize_yosys_procs.tcl
load_plugins
yosys -import

verilog_defaults -push

set_defines
set_incdirs
read_files
set_params

verilog_defaults -pop

synth $top

write_cxxrtl -header test_cxxrtl_cxxrtl_0.cpp
