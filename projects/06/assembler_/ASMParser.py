import typing as tp
from ASMLineType import ASMLineType

class ASMParser:

    @staticmethod
    def remove_comment_if_exist(line: str) -> str:
        return line.split('//', maxsplit=1)[0].strip('\n\t ')

    @staticmethod
    def get_line_type(line: str) -> ASMLineType:
        stripped_line: str = line.strip()

        if stripped_line == '':
            return ASMLineType.EMPTY_LINE
        elif stripped_line[0:2] == '//':
            return ASMLineType.COMMENT
        elif stripped_line[0] == '(':
            return ASMLineType.LABEL
        elif stripped_line[0] == '@':
            return ASMLineType.A_COMMAND
        else:
            return ASMLineType.C_COMMAND

    @staticmethod
    def translate_to_binary(number: int) -> str:
        return '{0:b}'.format(number)

    @staticmethod
    def get_label(line: str) -> str:
        """
        Gets label name from a string.
        :param line: "(LABEL)"
        :return: "LABEL"
        """
        return line.split(')', maxsplit=1)[0].strip('(\n\t ')

    @staticmethod
    def parse_a_command(line: str):
        """
        Parses A-command (gets the address after "@" symbol)
        :param line: "@2679"
        :return: "2679"
        """
        # @dummy
        return ASMParser.remove_comment_if_exist(line).strip('@')

    @staticmethod
    def parse_c_command(line: str) -> tp.Tuple[str, str, str]:
        """
        Parses C-command on dest, comp and jump tokens and returns them.
        :rtype: object
        :param line: "dest = comp; jump"
        :return: ("dest", "comp", "jump")
        """
        dest: str = ''
        comp: str = ''
        jump: str = ''

        remained_line: str = ASMParser.remove_comment_if_exist(line)

        tokens: tp.List[str] = remained_line.split('=', maxsplit=1)
        if len(tokens) > 1:
            dest = tokens[0].strip('\n\t ')
            remained_line = tokens[1]

        tokens: tp.List[str] = remained_line.split(';', maxsplit=1)
        if len(tokens) > 1:
            jump = tokens[1].strip('\n\t ')

        comp = tokens[0].strip('\n\t ').replace(' ', '')

        return dest, comp, jump

    def __init__(self, file_directory: str):
        self._file_directory = file_directory
        self._current_line_index = 0
        with open(file_directory) as f:
            self._lines = f.readlines()

    def get_next_line(self) -> str:
        line: str = self._lines[self._current_line_index]
        self._current_line_index += 1
        return line

    def is_next_line_exist(self) -> bool:
        return self._current_line_index < len(self._lines)

    def reset_current_line_index(self) -> None:
        self._current_line_index = 0
