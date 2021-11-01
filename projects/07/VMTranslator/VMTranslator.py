import sys
import os

import OSPathHelper
import ParserHelper
from VMParser import VMParser
from VMCodeWriter import VMCodeWriter


class VMTranslator:
    def __init__(self, vm_file_directory):

        # calculating the name os the resulting .asm file
        # and finding the .vm files which needed to be translated
        self._files_to_process = []
        self._is_bootstrap_needed = False

        if os.path.isfile(vm_file_directory):
            self._asm_file_name = OSPathHelper.remove_extension(vm_file_directory)
            if OSPathHelper.get_extension(vm_file_directory) == 'vm':
                self._files_to_process.append(vm_file_directory)

        elif os.path.isdir(vm_file_directory):
            self.is_bootstrap_needed = True
            basename = vm_file_directory.rsplit(os.sep, maxsplit=1)[-1]
            self._asm_file_name = vm_file_directory + os.sep + basename

            for filename in os.listdir(vm_file_directory):
                if OSPathHelper.get_extension(filename) == 'vm':
                    self._files_to_process.append(vm_file_directory + os.sep + filename)

        if len(self._files_to_process) == 0:
            print(f'Nothing to translate in the passed directory: {vm_file_directory}')
            sys.exit(1)

        self._asm_file_name += '.asm'
        print(f'Resulting .asm file name: {self._asm_file_name}')

        self._code_writer = VMCodeWriter(self._asm_file_name, self._is_bootstrap_needed)
        self._parser = None

    def translate(self):

        for filename in self._files_to_process:
            self._parser = VMParser(filename)
            self._code_writer.set_file_name(filename)

            while self._parser.has_more_commands():

                self._parser.advance()
                if ParserHelper.is_comment_or_empty(self._parser.current_command):
                    continue

                self._code_writer.write_command(self._parser.get_current_command_arg0(),
                                               self._parser.get_current_command_arg1(),
                                               self._parser.get_current_command_arg2())

        self._code_writer.write_asm_file()
        print(self._code_writer.result)


if __name__ == "__main__":

    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print("Usage: python VMTranslator.py [file.vm] | [local_directory] "
              "\nfile: some .vm file which needed to be translated into Hack assembly language"
              "\nlocal_directory: directory containing multiple .vm files")
        sys.exit(1)

    translator = VMTranslator(arguments[0])
    translator.translate()