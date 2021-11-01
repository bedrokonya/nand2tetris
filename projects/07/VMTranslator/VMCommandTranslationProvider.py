import os
import typing as tp

import ParserHelper
from VMConstant import VMCmd, VMSegment, ARITHMETIC_COMMANDS, BRANCHING_COMMANDS, FUNCTION_COMMANDS


class VMCommandTranslationProvider:
    """
    For every VM command gets its template assembly code from 'main_directory'.
    """

    def __init__(self, main_directory: str):
        assert os.path.isdir(main_directory)
        self._main_directory = main_directory
        self._cache_commands = {}

    def get_command_translation(self, command_name: str, arg1: str = '') -> str:

        cmd_hash: str = command_name + arg1
        command_translation: tp.Optional[str] = self._cache_commands.get(cmd_hash)

        if command_translation is None:

            file_directory: str = self._get_source_directory(command_name, arg1)
            with open(file_directory, 'r') as reader:
                file_content: tp.List[str] = reader.readlines()
                significant_content: tp.List[str] = []
                for line in file_content:
                    if ParserHelper.is_comment_or_empty(line):
                        continue
                    significant_content.append(ParserHelper.remove_content_of_curly_brackets(ParserHelper.normalize(line)))

                command_translation: str = os.linesep.join(significant_content) + os.linesep
                self._cache_commands[cmd_hash] = command_translation

        return command_translation

    def _get_source_directory(self, command_name: str, arg1: str = '') -> str:
        """
        By 'command_name' and 'arg1' gets exact directory inside 'main_directory' with .asm code for appropriate command.
        """
        file_directory: str = self._main_directory

        if command_name in ARITHMETIC_COMMANDS:
            file_directory += os.sep + 'arithmetic' + os.sep + command_name

        elif command_name in [VMCmd.C_PUSH, VMCmd.C_POP]:
            file_directory += os.sep + command_name
            if arg1 in [VMSegment.S_LOCAL, VMSegment.S_ARGUMENT, VMSegment.S_THIS, VMSegment.S_THAT]:
                file_directory += os.sep + f'{command_name}_local_argument_this_that'
            elif arg1 in [VMSegment.S_CONSTANT, VMSegment.S_TEMP, VMSegment.S_STATIC, VMSegment.S_POINTER]:
                file_directory += os.sep + f'{command_name}_{arg1}'

        elif command_name in BRANCHING_COMMANDS:
            file_directory += os.sep + 'branching' + os.sep + command_name

        elif command_name in FUNCTION_COMMANDS:
            file_directory += os.sep + 'function' + os.sep + command_name

        elif command_name == VMCmd.C_INIT:
            file_directory += os.sep + command_name

        else:
            raise Exception(f'Command {command_name} is not implemented')

        return file_directory + '.txt'
