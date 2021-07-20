import sys
from enum import Enum


class LineType(Enum):
    EMPTY_LINE = 0
    COMMENT = 1
    LABEL = 2
    C_COMMAND = 3
    A_COMMAND = 4


class Parser:

    @staticmethod
    def remove_comment_if_exist(line):
        return line.split('//', maxsplit=1)[0].strip('\n\t ')

    @staticmethod
    def get_line_type(line):
        stripped_line = line.strip()

        if stripped_line == '':
            return LineType.EMPTY_LINE
        elif stripped_line[0] + stripped_line[1] == '//':
            return LineType.COMMENT
        elif stripped_line[0] == '(':
            return LineType.LABEL
        elif stripped_line[0] == '@':
            return LineType.A_COMMAND
        else:
            return LineType.C_COMMAND

    @staticmethod
    def get_label(line):
        # (LABEL)
        return line.split(')', maxsplit=1)[0].strip('(\n\t ')

    @staticmethod
    def parse_a_command(line):
        # @dummy
        return Parser.remove_comment_if_exist(line).strip('@')

    @staticmethod
    def parse_c_command(line):
        # dest = comp; jump

        dest = ''
        comp = ''
        jump = ''

        remained_line = Parser.remove_comment_if_exist(line)

        tokens = remained_line.split('=', maxsplit=1)
        if len(tokens) > 1:
            dest = tokens[0].strip('\n\t ')
            remained_line = tokens[1]

        tokens = remained_line.split(';', maxsplit=1)
        if len(tokens) > 1:
            jump = tokens[1].strip('\n\t ')

        comp = tokens[0].strip('\n\t ').replace(' ', '')

        return dest, comp, jump

    @staticmethod
    def translate_to_binary(number):
        return '{0:b}'.format(number)

    def __init__(self, file_directory):
        self.file_directory = file_directory
        self.current_line_index = 0
        with open(file_directory) as f:
            self.lines = f.readlines()

    def next_line(self):
        line = self.lines[self.current_line_index]
        self.current_line_index += 1
        return line

    def is_next_line_exist(self):
        return self.current_line_index < len(self.lines)

    def reset(self):
        self.current_line_index = 0


class Assembler:

    COMMAND_C_MSB = '1'
    COMMAND_A_MSB = '0'
    ADDRESS_MAX = 24576
    ADDRESS_MAX_LENGTH = 15

    symbol_table = {'R0': 0,
                    'R1': 1,
                    'R2': 2,
                    'R3': 3,
                    'R4': 4,
                    'R5': 5,
                    'R6': 6,
                    'R7': 7,
                    'R8': 8,
                    'R9': 9,
                    'R10': 10,
                    'R11': 11,
                    'R12': 12,
                    'R13': 13,
                    'R14': 14,
                    'R15': 15,
                    'SCREEN': 16384,
                    'KBD': 24576,
                    'SP': 0,
                    'LCL': 1,
                    'ARG': 2,
                    'THIS': 3,
                    'THAT': 4}

    COMP_TRANSLATE = {'0': '0101010',
                      '1': '0111111',
                      '-1': '0111010',
                      'D': '0001100',
                      'A': '0110000',
                      '!D': '0001101',
                      '!A': '0110001',
                      '-D': '0001111',
                      '-A': '0110011',
                      'D+1': '0011111',
                      'A+1': '0110111',
                      'D-1': '0001110',
                      'A-1': '0110010',
                      'D+A': '0000010',
                      'D-A': '0010011',
                      'A-D': '0000111',
                      'D&A': '0000000',
                      'D|A': '0010101',
                      'M': '1110000',
                      '!M': '1110001',
                      'M+1': '1110111',
                      'M-1': '1110010',
                      'D+M': '1000010',
                      'D-M': '1010011',
                      'M-D': '1000111',
                      'D&M': '1000000',
                      'D|M': '1010101'}

    DEST_TRANSLATE = {'': '000',
                      'M': '001',
                      'D': '010',
                      'MD': '011',
                      'A': '100',
                      'AM': '101',
                      'AD': '110',
                      'AMD': '111'}

    JUMP_TRANSLATE = {'': '000',
                      'JGT': '001',
                      'JEQ': '010',
                      'JGE': '011',
                      'JLT': '100',
                      'JNE': '101',
                      'JLE': '110',
                      'JMP': '111'}

    def __init__(self, file_directory):
        self.parser = Parser(file_directory)
        self.hack_file_directory = file_directory.rsplit('.', maxsplit=1)[0] + '.hack'
        self.current_free_register = 16

    def first_pass(self):
        significant_line_counter = 0
        while self.parser.is_next_line_exist():
            current_line = self.parser.next_line()
            line_type = Parser.get_line_type(current_line)
            if line_type == LineType.EMPTY_LINE or line_type == LineType.COMMENT:
                continue
            elif line_type == LineType.LABEL:
                label = Parser.get_label(current_line)
                Assembler.symbol_table[label] = significant_line_counter
            else:
                significant_line_counter += 1

    def second_pass(self):
        binary_code = ''
        while self.parser.is_next_line_exist():

            current_line = self.parser.next_line()
            line_type = Parser.get_line_type(current_line)
            translated_command = ''

            if line_type == LineType.EMPTY_LINE or line_type == LineType.COMMENT or line_type == LineType.LABEL:
                continue

            elif line_type == LineType.A_COMMAND:
                translated_command = self.translate_a_command(current_line)

            elif line_type == LineType.C_COMMAND:
                translated_command = self.translate_c_command(current_line)

            binary_code += translated_command + '\n'

        return binary_code.strip()

    def translate_a_command(self, line):
        main_part = Parser.parse_a_command(line)
        address = Assembler.symbol_table.get(main_part)
        if address is not None:
            address = int(address)
        elif main_part.isnumeric():
            address = int(main_part)
        else:
            Assembler.symbol_table[main_part] = self.current_free_register
            address = self.current_free_register
            self.current_free_register += 1
            assert(self.current_free_register <= Assembler.ADDRESS_MAX)

        binary_address = Parser.translate_to_binary(address)
        lacking_zero_bits = Assembler.ADDRESS_MAX_LENGTH - len(binary_address)

        if lacking_zero_bits != 0:
            binary_address = lacking_zero_bits * '0' + binary_address
        translated_command = Assembler.COMMAND_A_MSB + binary_address

        return translated_command

    def translate_c_command(self, line):
        dest, comp, jump = Parser.parse_c_command(line)

        assert(comp != '')
        comp_bin = Assembler.COMP_TRANSLATE.get(comp)
        assert(comp_bin is not None and len(comp_bin) == 7)

        dest_bin = Assembler.DEST_TRANSLATE.get(dest)
        assert(len(dest_bin) == 3)

        jump_bin = Assembler.JUMP_TRANSLATE.get(jump)
        assert(len(jump_bin) == 3)

        translated_command = Assembler.COMMAND_C_MSB + '11' + comp_bin + dest_bin + jump_bin
        return translated_command

    def assemble(self):
        self.first_pass()
        self.parser.reset()
        binary_code = self.second_pass()
        print(binary_code)

        hack_file = open(self.hack_file_directory, 'w')
        hack_file.write(binary_code)
        hack_file.close()


if __name__ == '__main__':

    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print("Usage: python assembler.py [file] "
              "file: file written in symbolic assembly Hack language"
              "which needed to be translated into binary Hack language")
        sys.exit(1)

    assembler = Assembler(arguments[0])
    assembler.assemble()
