import typing as tp

import ParserHelper


class VMParser:
    """
    Handles the parsing of a single .vm file.
    It reads VM commands, parses them, and provides convenient access to their components.
    In addition, it removes all white spaces and comments.
    """

    def __init__(self, filename: str):

        self._filename = filename
        self._current_command_index = -1
        self._current_arg0 = None
        self._current_arg1 = None
        self._current_arg2 = None

        self.current_command = None

        with open(filename) as f:
            self._commands = f.readlines()

    def has_more_commands(self) -> bool:
        """
        Checks if there are more commands in the input.

        :return: bool
        """
        return self._current_command_index < len(self._commands) - 1

    def advance(self) -> None:
        """
        Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is True.
        """
        self._current_command_index += 1
        self.current_command = ParserHelper.normalize(self._commands[self._current_command_index])

        tokens: tp.List[str] = self.current_command.split(' ')
        self._current_arg0 = tokens[0]
        self._current_arg1 = tokens[1] if len(tokens) > 1 else ''
        self._current_arg2 = tokens[2] if len(tokens) > 2 else ''

    def get_current_command_arg0(self) -> str:
        """
        :return: str, the name of the current command
        """
        return self._current_arg0

    def get_current_command_arg1(self) -> str:
        """
        Should NOT be called if the current command is in ARITHMETIC_COMMANDS or if current command is C_RETURN

        :return: str, the first argument of the current command
        """
        return self._current_arg1

    def get_current_command_arg2(self) -> str:
        """
        Should be called only if the current command is C_PUSH, C_POP, C_FUNCTION, C_CALL
        :return: str, the second argument of the current command
        """
        return self._current_arg2
