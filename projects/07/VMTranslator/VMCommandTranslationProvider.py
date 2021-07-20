import os

from VMCommandType import VMCommandType
from ParserHelper import ParserHelper


class VMCommandTranslationProvider:

    def __init__(self, main_directory):
        assert os.path.isdir(main_directory)
        self.main_directory = main_directory
        self.cache = {}

    def get_command_translation(self, command_type: VMCommandType, command_name, arg1='') -> str:

        _hash = command_type.value + command_name + arg1
        command_translation = self.cache.get(_hash)

        if command_translation is None:

            file_directory = self.get_source_directory(command_type, command_name, arg1)
            with open(file_directory, 'r') as reader:
                file_content = reader.readlines()

            significant_content = []
            for line in file_content:
                if ParserHelper.is_comment_or_empty(line):
                    continue
                significant_content.append(ParserHelper.remove_content_of_curly_brackets(
                        ParserHelper.normalize(line)))

            command_translation = '\n'.join(significant_content) + '\n'
            self.cache[_hash] = command_translation
            reader.close()

        return command_translation

    def get_source_directory(self, command_type: VMCommandType, command_name: str, arg1: str) -> str:

        file_directory = self.main_directory

        if command_type == VMCommandType.C_ARITHMETIC:
            file_directory += os.sep + command_type.value + os.sep + command_name

        elif command_type == VMCommandType.C_PUSH or command_type == VMCommandType.C_POP:
            file_directory += os.sep + command_type.value
            if arg1 in ['local', 'argument', 'this', 'that']:
                file_directory += os.sep + f'{command_name}_local_argument_this_that'

            elif arg1 in ['constant', 'temp', 'static', 'pointer']:
                file_directory += os.sep + f'{command_name}_{arg1}'

            else:
                raise Exception(f'Arg1 {arg1} is not supported')
        else:
            # TODO
            raise Exception(f'Command {command_name} is not implemented yet')

        return file_directory + '.txt'
