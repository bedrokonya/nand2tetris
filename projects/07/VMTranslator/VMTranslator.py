import sys
import os

import OsPathHelper
import ParserHelper
from VMParser import VMParser
from VMCodeWriter import VMCodeWriter


class VMTranslator:
    def __init__(self, vm_file_directory):

        # calculating the name os the resulting .asm file
        # and finding the files which needed to be translated
        self.files_to_process = []
        self.is_bootstrap_needed = False

        if os.path.isfile(vm_file_directory):

            self.asm_file_name = OsPathHelper.removeExtension(vm_file_directory)
            if OsPathHelper.getExtension(vm_file_directory) == 'vm':
                self.files_to_process.append(vm_file_directory)

        elif os.path.isdir(vm_file_directory):
            self.is_bootstrap_needed = True
            basename = vm_file_directory.rsplit(os.sep, maxsplit=1)[-1]
            self.asm_file_name = vm_file_directory + os.sep + basename

            for filename in os.listdir(vm_file_directory):
                if OsPathHelper.getExtension(filename) == 'vm':
                    self.files_to_process.append(vm_file_directory + os.sep + filename)

        if len(self.files_to_process) == 0:
            print(f'Nothing to translate in the passed directory: {vm_file_directory}')
            sys.exit(1)

        self.asm_file_name += '.asm'
        print(f'Resulting .asm file name: {self.asm_file_name}')

        self.code_writer = VMCodeWriter(self.asm_file_name, self.is_bootstrap_needed)
        self.parser = None

    def translate(self):

        for filename in self.files_to_process:
            self.parser = VMParser(filename)
            self.code_writer.setFileName(filename)

            while self.parser.hasMoreCommands():

                self.parser.advance()
                if ParserHelper.is_comment_or_empty(self.parser.current_command):
                    continue

                self.code_writer.writeCommand(self.parser.getCurrentCommandArg0(),
                                              self.parser.getCurrentCommandArg1(),
                                              self.parser.getCurrentCommandArg2())

        self.code_writer.writeAsmFile()


if __name__ == "__main__":

    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print("Usage: python VMTranslator.py [file] "
              "\nfile: some .vm file which needed to be translated into Hack assembly language")
        sys.exit(1)

    translator = VMTranslator(arguments[0])
    translator.translate()
    print(translator.code_writer.result)
