import ParserHelper


class VMParser:

    def __init__(self, filename):

        self._filename = filename
        self._current_command_index = -1
        self._current_arg0 = None
        self._current_arg1 = None
        self._current_arg2 = None

        self.current_command = None

        with open(filename) as f:
            self._commands = f.readlines()

    def has_more_commands(self):
        return self._current_command_index < len(self._commands) - 1

    def advance(self):
        self._current_command_index += 1
        self.current_command = ParserHelper.normalize(self._commands[self._current_command_index])

        tokens = self.current_command.split(' ')
        self._current_arg0 = tokens[0]
        self._current_arg1 = tokens[1] if len(tokens) > 1 else ''
        self._current_arg2 = tokens[2] if len(tokens) > 2 else ''

    def get_current_command_arg0(self):
        return self._current_arg0

    def get_current_command_arg1(self):
        return self._current_arg1

    def get_current_command_arg2(self):
        return self._current_arg2
