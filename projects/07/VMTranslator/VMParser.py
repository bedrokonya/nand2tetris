from ParserHelper import ParserHelper
from VMCommandType import VMCommandType


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
        self.current_command = ParserHelper.normalize(self.commands[self.current_command_index])

    def currentCommandArg0(self):
        return self.current_command.split(' ')[0]

    def getCurrentCommandArg1(self):
        return self.current_command.split(' ')[1]

    def getCurrentCommandArg2(self):
        return self.current_command.split(' ')[2]

    def getCurrentCommandType(self):
        command_name = self.currentCommandArg0()
        if command_name in ['add', 'and', 'eq', 'gt', 'lt', 'neg', 'not', 'or', 'sub']:
            return VMCommandType.C_ARITHMETIC
        elif command_name == 'push':
            return VMCommandType.C_PUSH
        elif command_name == 'pop':
            return VMCommandType.C_POP
        else:
            # TODO
            raise Exception(f'Command {command_name} not implemented yet')
