import sys

from ParserHelper import ParserHelper
from VMCommandType import VMCommandType
from VMParser import VMParser
from VMCodeWriter import VMCodeWriter


class VMTranslator:
    def __init__(self, file_directory):
        self.parser = VMParser(file_directory)
        self.code_writer = VMCodeWriter()
        self.code_writer.setFileName(file_directory)

    def translate(self):

        while self.parser.hasMoreCommands():

            self.parser.advance()
            if ParserHelper.is_comment_or_empty(self.parser.current_command):
                continue

            current_command_type = self.parser.getCurrentCommandType()

            if current_command_type == VMCommandType.C_ARITHMETIC:
                self.code_writer.writeArithmetic(self.parser.currentCommandArg0(), self.parser.current_command_index)

            elif current_command_type == VMCommandType.C_PUSH or current_command_type == VMCommandType.C_POP:
                self.code_writer.writePushPop(current_command_type, self.parser.currentCommandArg0(),
                                              self.parser.getCurrentCommandArg1(),
                                              self.parser.getCurrentCommandArg2())
            else:
                # TODO
                print(f'Command {self.parser.currentCommandArg0()} not implemented yet')
                sys.exit(1)

        self.code_writer.write_asm_file()


if __name__ == "__main__":

    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print("Usage: python VMTranslator.py [file] "
              "\nfile: some .vm file which needed to be translated into Hack assembly language")
        sys.exit(1)

    translator = VMTranslator(arguments[0])
    translator.translate()
    print(translator.code_writer.result)
