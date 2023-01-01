from .edalize_common import make_edalize_test


def test_yosys(make_edalize_test):
    output_names = {
        "default_output_name": {
            "arch": "ice40",
        },
        "custom_output_name": {"arch": "ice40", "output_name": "test.json"},
    }

    for test_name, tool_options in output_names.items():
        tf = make_edalize_test(
            "yosys",
            param_types=["vlogdefine", "vlogparam"],
            tool_options=tool_options,
            ref_dir=test_name,
        )

        tf.backend.configure()
        tf.compare_files(["Makefile"])


def test_yosys_no_arch(make_edalize_test):
    # When the arch tool_options is not set
    # the synth proc should be empty
    tf = make_edalize_test(
        "yosys",
        param_types=["vlogdefine", "vlogparam"],
        tool_options={},
        ref_dir="no_arch",
    )

    tf.backend.configure()
    tf.compare_files(["edalize_yosys_procs.tcl"])

    # Ensure the synth command is generated when
    # the arch is specified
    tf = make_edalize_test(
        "yosys",
        param_types=["vlogdefine", "vlogparam"],
        tool_options={"arch": "ice40"},
    )

    tf.backend.configure()
    tf.compare_files(["edalize_yosys_procs.tcl"])
