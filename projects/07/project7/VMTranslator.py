import sys
import ParserHelper
import os
from enum import Enum


TEMP_LOCATION_IN_RAM = 5

ARITHMETIC_COMMANDS_TRANSLATION = {'add': (lambda x: '@SP\nA=M-1\nD=M\nA=A-1\nM=D+M\n@SP\nM=M-1\n'),
                                   'sub': (lambda x: '@SP\nA=M-1\nD=M\nA=A-1\nM=M-D\n@SP\nM=M-1\n'),
                                   'eq': (lambda x: f'@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@EQ{x}\nD;JEQ\n@0\nD=A\n@EQWRITERESULT{x}\n0;JMP\n(EQ{x})\nD=-1\n(EQWRITERESULT{x})\n@SP\nA=M-1\nA=A-1\nM=D\n@SP\nM=M-1\n'),
                                   'gt': (lambda x: f'@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@GT{x}\nD;JGT\n@0\nD=A\n@GTWRITERESULT{x}\n0;JMP\n(GT{x})\nD=-1\n(GTWRITERESULT{x})\n@SP\nA=M-1\nA=A-1\nM=D\n@SP\nM=M-1\n'),
                                   'lt': (lambda x: f'@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@LT{x}\nD;JLT\n@0\nD=A\n@LTWRITERESULT{x}\n0;JMP\n(LT{x})\nD=-1\n(LTWRITERESULT{x})\n@SP\nA=M-1\nA=A-1\nM=D\n@SP\nM=M-1\n'),
                                   'and': (lambda x: '@SP\nA=M-1\nD=M\nA=A-1\nM=D&M\n@SP\nM=M-1\n'),
                                   'or': (lambda x: '@SP\nA=M-1\nD=M\nA=A-1\nM=D|M\n@SP\nM=M-1\n'),
                                   'neg': (lambda x: '@SP\nA=M-1\nM=-M\n'),
                                   'not': (lambda x: '@SP\nA=M-1\nM=!M\n')}

ARG1_TRANSLATION = {'local': 'LCL',
                    'argument': 'ARG',
                    'this': 'THIS',
                    'that': 'THAT'}

PUSH_ARG1_EQUALS_LOCAL_ARGUMENT_THIS_THAT = '@{}\nD=A\n@{}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
POP_ARG1_EQUALS_LOCAL_ARGUMENT_THIS_THAT = '@{}\nD=A\n@{}\nD=M+D\n@addr\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@addr\nA=M\nM=D\n'

PUSH_POP_COMMANDS_TRANSLATION = {'push constant': (lambda constant: f'@{constant}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'),
                                 'push local': (lambda segment, i: PUSH_ARG1_EQUALS_LOCAL_ARGUMENT_THIS_THAT.format(i, segment)),
                                 'push argument': (lambda segment, i: PUSH_ARG1_EQUALS_LOCAL_ARGUMENT_THIS_THAT.format(i, segment)),
                                 'push this': (lambda segment, i: PUSH_ARG1_EQUALS_LOCAL_ARGUMENT_THIS_THAT.format(i, segment)),
                                 'push that': (lambda segment, i: PUSH_ARG1_EQUALS_LOCAL_ARGUMENT_THIS_THAT.format(i, segment)),
                                 'push temp': (lambda segment_addr, i: f'@{i}\nD=A\n@{segment_addr}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'),
                                 'push static': (lambda filename, i: f'@{filename}.{i}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'),
                                 'push pointer': (lambda segment: f'@{segment}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'),
                                 'pop local': (lambda segment, i: POP_ARG1_EQUALS_LOCAL_ARGUMENT_THIS_THAT.format(i, segment)),
                                 'pop argument': (lambda segment, i: POP_ARG1_EQUALS_LOCAL_ARGUMENT_THIS_THAT.format(i, segment)),
                                 'pop this': (lambda segment, i: POP_ARG1_EQUALS_LOCAL_ARGUMENT_THIS_THAT.format(i, segment)),
                                 'pop that': (lambda segment, i: POP_ARG1_EQUALS_LOCAL_ARGUMENT_THIS_THAT.format(i, segment)),
                                 'pop static': (lambda filename, i: f'@SP\nA=M-1\nD=M\n@SP\nM=M-1\n@{filename}.{i}\nM=D\n'),
                                 'pop temp': (lambda segment_addr, i: f'@{i}\nD=A\n@{segment_addr}\nD=D+A\n@addr\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@addr\nA=M\nM=D\n'),
                                 'pop pointer': (lambda segment: f'@SP\nM=M-1\nA=M\nD=M\n@{segment}\nM=D\n')}

class VMCommandType(Enum):
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8


class VMTranslator:
    def __init__(self, file_directory):
        self.parser = VMParser(file_directory)
        self.code_writer = VMCodeWriter()
        self.code_writer.setFileName(file_directory)

    def translate(self):

        while self.parser.hasMoreCommands():

            self.parser.advance()
            if ParserHelper.ParserHelper.is_comment_or_empty(self.parser.current_command):
                continue

            current_command_type = self.parser.getCurrentCommandType()

            if current_command_type == VMCommandType.C_ARITHMETIC:
                self.code_writer.writeArithmetic(self.parser.currentCommandArg0(), self.parser.current_command_index)

            elif current_command_type == VMCommandType.C_PUSH or current_command_type == VMCommandType.C_POP:
                self.code_writer.writePushPop(self.parser.currentCommandArg0(), self.parser.getCurrentCommandArg1(),
                                              self.parser.getCurrentCommandArg2())
            else:
                # TODO
                print(f'Command {self.parser.currentCommandArg0()} not implemented yet')
                sys.exit(1)

        self.code_writer.write_asm_file()


class VMCodeWriter:

    def __init__(self):
        self.asm_file_name = None
        self.vm_file_name = None
        self.vm_file_name_without_dir = None
        self.result = ''

    def setFileName(self, vm_file_name):
        self.vm_file_name = vm_file_name
        self.vm_file_name_without_dir = os.path.basename(vm_file_name).rsplit('.', maxsplit=1)[0].strip()

        if self.asm_file_name is None:
            if os.path.isfile(vm_file_name):
                self.asm_file_name = vm_file_name.rsplit('.', maxsplit=1)[0].strip()
            else:
                if vm_file_name.find('/') != -1:
                    self.asm_file_name = vm_file_name + '/' + vm_file_name.rsplit('/', maxsplit=1)[1]
            self.asm_file_name += '.asm'
            print(f'Resulting .asm file name: {self.asm_file_name}')

    def writeArithmetic(self, command_name, current_command_index):
        self.result += ARITHMETIC_COMMANDS_TRANSLATION.get(command_name)(current_command_index)

    def writePushPop(self, command_name, segment, i):
        if segment == 'constant':
            translated_command = PUSH_POP_COMMANDS_TRANSLATION.get(command_name + ' ' + segment)(i)
        elif segment == 'local' or segment == 'argument' or segment == 'this' or segment == 'that':
            translated_command = PUSH_POP_COMMANDS_TRANSLATION.get(command_name + ' ' + segment)(ARG1_TRANSLATION.get(segment), i)
        elif segment == 'static':
            translated_command = PUSH_POP_COMMANDS_TRANSLATION.get(command_name + ' ' + segment)(self.vm_file_name_without_dir, i)
        elif segment == 'temp':
            translated_command = PUSH_POP_COMMANDS_TRANSLATION.get(command_name + ' ' + segment)(TEMP_LOCATION_IN_RAM, i)
        elif segment == 'pointer':
            new_segment = 'this' if int(i) == 0 else 'that'
            translated_command = PUSH_POP_COMMANDS_TRANSLATION.get(command_name + ' ' + segment)(ARG1_TRANSLATION.get(new_segment))
        else:
            print(f'Segment {segment} is not implemented yet')
            sys.exit(1)
        self.result += translated_command

    def write_asm_file(self):
        asm_file = open(self.asm_file_name, 'w')
        asm_file.write(self.result)
        asm_file.close()


class VMParser:

    def __init__(self, file_name):
        self.file_name = file_name
        self.current_command_index = -1
        self.current_command = None
        with open(file_name) as f:
            self.commands = f.readlines()

    def hasMoreCommands(self):
        return self.current_command_index < len(self.commands) - 1

    def advance(self):
        self.current_command_index += 1
        self.current_command = ParserHelper.ParserHelper.normalize_line(self.commands[self.current_command_index])

    def currentCommandArg0(self):
        return self.current_command.split(' ')[0]

    def getCurrentCommandArg1(self):
        return self.current_command.split(' ')[1]

    def getCurrentCommandArg2(self):
        return self.current_command.split(' ')[2]

    def getCurrentCommandType(self):
        command_name = self.currentCommandArg0()
        if ARITHMETIC_COMMANDS_TRANSLATION.get(command_name):
            return VMCommandType.C_ARITHMETIC
        elif command_name == 'push':
            return VMCommandType.C_PUSH
        elif command_name == 'pop':
            return VMCommandType.C_POP
        else:
            # TODO
            print(f'Command {command_name} not implemented yet')
            sys.exit(1)


if __name__ == "__main__":

    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print("Usage: python VMTranslator.py [file] "
              "file: some VM program which needed to be translated into Hack assembly language")
        sys.exit(1)

    translator = VMTranslator(arguments[0])
    translator.translate()
    print(translator.code_writer.result)
