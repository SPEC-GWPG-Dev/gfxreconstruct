#!/usr/bin/env python3
#
# Copyright (c) 2021 LunarG, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import sys
from base_generator import *
from dx12_base_generator import *
from base_struct_decoders_header_generator import *


class Dx12StructDecodersHeaderGenerator(
        Dx12BaseGenerator, BaseStructDecodersHeaderGenerator):
    """Generates C++ functions responsible for decoding Dx12 API calls."""

    def __init__(self, source_dict, dx12_prefix_strings,
                 err_file=sys.stderr,
                 warn_file=sys.stderr,
                 diag_file=sys.stdout):
        Dx12BaseGenerator.__init__(
            self, source_dict, dx12_prefix_strings,
            err_file, warn_file, diag_file)
        self.check_blacklist = True

    def beginFile(self, gen_opts):
        """Methond override."""
        BaseGenerator.beginFile(self, gen_opts)

        self.write_include()
        write('GFXRECON_BEGIN_NAMESPACE(gfxrecon)', file=self.outFile)
        write('GFXRECON_BEGIN_NAMESPACE(decode)', file=self.outFile)
        self.newline()

    def generate_feature(self):
        """Methond override."""
        code = ''
        struct_list = self.source_dict['struct_list']
        for name in struct_list:
            code += 'struct Decoded_{};\n'.format(name)
        code += 'struct Decoded_LARGE_INTEGER;\n'.format(name)
        write(code, file=self.outFile)

        Dx12BaseGenerator.generate_feature(self)
        BaseStructDecodersHeaderGenerator.generate_feature(self)

    def write_include(self):
        """Methond override."""
        code = ''
        header_dict = self.source_dict['header_dict']
        for k, v in header_dict.items():
            code += '#include <{}>\n'.format(k)

        code += ("\n"
                 "#include \"decode/handle_pointer_decoder.h\"\n"
                 "#include \"decode/string_array_decoder.h\"\n"
                 "#include \"decode/string_decoder.h\"\n"
                 "#include \"decode/struct_pointer_decoder.h\"\n"
                 "\n")
        write(code, file=self.outFile)

    def endFile(self):
        """Methond override."""
        self.newline()
        write('GFXRECON_END_NAMESPACE(decode)', file=self.outFile)
        write('GFXRECON_END_NAMESPACE(gfxrecon)', file=self.outFile)

        # Finish processing in superclass
        BaseGenerator.endFile(self)