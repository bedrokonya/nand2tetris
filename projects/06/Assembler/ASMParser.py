from ASMLineType import ASMLineType


class ASMParser:

    @staticmethod
    def remove_comment_if_exist(line):
        return line.split('//', maxsplit=1)[0].strip('\n\t ')

    @staticmethod
    def get_line_type(line):
        stripped_line = line.strip()

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
    def get_label(line):
        # (LABEL)
        return line.split(')', maxsplit=1)[0].strip('(\n\t ')

    @staticmethod
    def parse_a_command(line):
        # @dummy
        return ASMParser.remove_comment_if_exist(line).strip('@')

    @staticmethod
    def parse_c_command(line):
        # dest = comp; jump

        dest = ''
        comp = ''
        jump = ''

        remained_line = ASMParser.remove_comment_if_exist(line)

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
        self._file_directory = file_directory
        self._current_line_index = 0
        with open(file_directory) as f:
            self._lines = f.readlines()

    def next_line(self):
        line = self._lines[self._current_line_index]
        self.current_line_index += 1
        return line

    def is_next_line_exist(self):
        return self._current_line_index < len(self._lines)

    def reset(self):
        self._current_line_index = 0
