import sys
import typing as tp
from ASMLineType import ASMLineType
from ASMParser import ASMParser
from ASMConstant import ASMConstant


class Assembler:
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

    def __init__(self, file_directory: str):
        self._parser = ASMParser(file_directory)
        self._hack_file_directory = file_directory.rsplit('.', maxsplit=1)[0] + '.hack'
        self._current_free_register = 16

    def _first_pass(self) -> None:
        """
            Goes through the entire assembly program, line by line,
            and extends the Assembler.symbol_table without generating any code.

            This pass results in entering all the program’s labels along
            with their ROM addresses into the Assembler.symbol_table.
        """
        significant_line_counter: int = 0
        while self._parser.is_next_line_exist():
            current_line: str = self._parser.get_next_line()
            line_type: ASMLineType = ASMParser.get_line_type(current_line)

            if line_type in [ASMLineType.EMPTY_LINE, ASMLineType.COMMENT]:
                continue

            elif line_type == ASMLineType.LABEL:
                label = ASMParser.get_label(current_line)
                Assembler.symbol_table[label] = significant_line_counter

            else:
                significant_line_counter += 1

    def _second_pass(self) -> str:
        """
            Goes through entire assembly program again after _first_pass
            and translates every A-command and C-command in binary code
        :return: resulting binary code of .asm program
        """
        binary_code: str = ''
        while self._parser.is_next_line_exist():

            current_line: str = self._parser.get_next_line()
            line_type: ASMLineType = ASMParser.get_line_type(current_line)
            translated_command: str = ''

            if line_type in [ASMLineType.EMPTY_LINE, ASMLineType.COMMENT, ASMLineType.LABEL]:
                continue

            elif line_type == ASMLineType.A_COMMAND:
                translated_command = self._translate_a_command(current_line)

            elif line_type == ASMLineType.C_COMMAND:
                translated_command = self._translate_c_command(current_line)

            binary_code += translated_command + '\n'

        return binary_code.strip()

    def _translate_a_command(self, line: str) -> str:
        """
        Translates A-command, which has following structure:
            @value
        where value is either a non-negative decimal number
        or a symbol referring to such number

        :param line: "@value"
        :return: binary code of the A-command
        """

        a_cmd_value: str = ASMParser.parse_a_command(line)
        address: tp.Union[int, None] = Assembler.symbol_table.get(a_cmd_value)

        if address is not None:
            address = int(address)
        elif a_cmd_value.isnumeric():
            address = int(a_cmd_value)
        else:
            Assembler.symbol_table[a_cmd_value] = self._current_free_register
            address = self._current_free_register
            self._current_free_register += 1
            assert(self._current_free_register <= ASMConstant.ADDRESS_MAX)

        binary_address: str = ASMParser.translate_to_binary(address)
        lacking_zero_bits: int = ASMConstant.ADDRESS_MAX_LENGTH - len(binary_address)

        if lacking_zero_bits != 0:
            binary_address = lacking_zero_bits * '0' + binary_address
        translated_command: str = ASMConstant.COMMAND_A_MSB + binary_address

        return translated_command

    def _translate_c_command(self, line: str) -> str:
        dest, comp, jump = ASMParser.parse_c_command(line)

        assert(comp != '')
        comp_bin: str = ASMConstant.COMP_TRANSLATE.get(comp)
        assert(comp_bin is not None and len(comp_bin) == 7)

        dest_bin: str = ASMConstant.DEST_TRANSLATE.get(dest)
        assert(len(dest_bin) == 3)

        jump_bin: str = ASMConstant.JUMP_TRANSLATE.get(jump)
        assert(len(jump_bin) == 3)

        translated_command: str = ASMConstant.COMMAND_C_MSB + ASMConstant.C_COMMAND_PREFIX + comp_bin + dest_bin + jump_bin
        return translated_command

    def assemble(self) -> None:
        self._first_pass()
        self._parser.reset_current_line_index()
        binary_code = self._second_pass()
        print(binary_code)

        with open(self._hack_file_directory, 'w') as hack_file:
            hack_file.write(binary_code)


if __name__ == '__main__':

    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print("Usage: python Assembler.py [file] "
              "file: file written in symbolic assembly Hack language"
              "which needed to be translated into binary Hack language")
        sys.exit(1)

    assembler = Assembler(arguments[0])
    assembler.assemble()
