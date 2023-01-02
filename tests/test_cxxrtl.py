import os
import edalize
import pytest
from .edalize_common import make_edalize_test, compare_files, tests_dir, FILES


@pytest.fixture
def test_cxxrtl(tmpdir):
    test_name = "cxxrtl"
    os.environ["PATH"] = (
        os.path.join(tests_dir, "mock_commands") + ":" + os.environ["PATH"]
    )
    tool = "cxxrtl"
    name = "test_cxxrtl_{}_0".format(test_name)
    work_root = str(tmpdir)

    edam = {"name": name, "flow_options": {}, "files": FILES}

    tf = edalize.get_flow(tool)(edam=edam, work_root=work_root)
    tf.configure()

    config_file_list = [
        "Makefile",
        "edalize_yosys_template.tcl",
        "edalize_yosys_procs.tcl",
    ]
    ref_dir = os.path.join(tests_dir, "test_" + tool)
    compare_files(ref_dir, work_root, config_file_list)
