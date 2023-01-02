# Copyright edalize contributors
# Licensed under the 2-Clause BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-2-Clause

import logging

from edalize.tools.edatool import Edatool
from edalize.utils import EdaCommands

logger = logging.getLogger(__name__)


class Ccompiler(Edatool):
    description = "Compile C/C++ files"

    TOOL_OPTIONS = {
        "cc": {
            "type": "str",
            "desc": "The used compiler",
            "list": False,
        },
        "cc_flags": {
            "type": "str",
            "desc": "Compiler flags",
            "list": True,
        },
        "cc_extra_flags": {
            "type": "str",
            "desc": "Additional compiler flags",
            "list": True,
        },
        "output_name": {
            "type": "str",
            "desc": "The output binary name",
            "list": False,
        },
    }

    def configure(self, edam):
        super().configure(edam)
        unused_files = []
        source_files = []
        header_files = []
        for f in self.files:
            if f.get("file_type") in ["cSource", "cppSource"]:
                if f.get("is_include_file"):
                    header_files.append(f.get("name"))
                else:
                    source_files.append(f.get("name"))
            else:
                unused_files.append(f)

        if not source_files:
            raise RuntimeError("No input file(s) specified for compiler")

        output_name = self.tool_options.get("output_name", "cxxrtl_binary")
        self.edam["files"] = unused_files
        self.edam["files"].append({"name": output_name, "file_type": "binary"})

        # Compiler configuration
        cc = self.tool_options.get("cc", "clang++")
        cc_flags = self.tool_options.get("cc_flags", [])
        cc_extra_flags = self.tool_options.get("cc_extra_flags", [])

        target = output_name
        command = [cc] + cc_flags + cc_extra_flags + ["-o", target]
        command += source_files

        depends = source_files + header_files
        commands = EdaCommands()
        commands.add(command, [target], depends)
        self.commands = commands.commands
