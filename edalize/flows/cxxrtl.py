# Copyright edalize contributors
# Licensed under the 2-Clause BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-2-Clause

import os.path
from importlib import import_module
import subprocess

from edalize.flows.edaflow import Edaflow


class Cxxrtl(Edaflow):
    """Open source toolchain for Lattice iCE40 FPGAs. Uses yosys for synthesis and nextpnr for Place & Route"""

    argtypes = ["vlogdefine", "vlogparam"]

    FLOW_DEFINED_TOOL_OPTIONS = {
        "yosys": {"output_format": "cxxrtl", "output_name": ""},
        "ccompiler": {"cc_flags": "", "output_name": ""},
    }

    FLOW_OPTIONS = {
        "frontends": {
            "type": "str",
            "desc": "Tools to run before yosys (e.g. sv2v)",
            "list": True,
        },
    }

    @classmethod
    def get_flow_options(cls):
        return cls.FLOW_OPTIONS.copy()

    @classmethod
    def get_tool_options(cls, flow_options):
        flow = flow_options.get("frontends", [])
        flow += ["yosys", "ccompiler"]
        return cls.get_filtered_tool_options(flow, cls.FLOW_DEFINED_TOOL_OPTIONS)

    def configure_flow(self, flow_options):
        name = self.edam["name"]

        self.yosys_output = "{}.cpp".format(name)
        yosys_include = "{}/include".format(
            subprocess.Popen(
                ["yosys-config", "--datdir"], stdout=subprocess.PIPE, env=os.environ
            )
            .communicate()[0]
            .strip()
            .decode()
        )

        flow = [
            (
                "yosys",
                ["ccompiler"],
                {
                    "output_format": "cxxrtl",
                    "output_name": self.yosys_output,
                    "yosys_write_options": ["-header"],
                },
            ),
            (
                "ccompiler",
                [],
                {
                    "cc_flags": [
                        "-g",
                        "-O3",
                        "-std=c++14",
                        "-I",
                        ".",
                        "-I",
                        yosys_include,
                    ],
                    "output_name": name,
                },
            ),
        ]

        # Add the generated cpp files from yosys
        self.edam["files"].append({"name": self.yosys_output, "file_type": "cppSource"})
        self.edam["files"].append(
            {
                "name": "{}.h".format(name),
                "file_type": "cppSource",
                "is_include_file": True,
            }
        )

        # Add any user-specified frontends to the flow
        next_tool = "yosys"

        for frontend in reversed(flow_options.get("frontends", [])):
            flow[0:0] = [(frontend, [next_tool], {})]
            next_tool = frontend

        self.commands.set_default_target(name)

        return flow

    def run(self, args):
        cmd = os.path.join(self.work_root, self.edam["name"])
        self._run_tool(cmd)
