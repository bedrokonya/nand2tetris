import ParserHelper


class VMParser:

    def __init__(self, filename):

        self.filename = filename
        self.current_command_index = -1
        self.current_command = None
        self.current_arg0 = None
        self.current_arg1 = None
        self.current_arg2 = None

        with open(filename) as f:
            self.commands = f.readlines()

    def hasMoreCommands(self):
        return self.current_command_index < len(self.commands) - 1

    def advance(self):
        self.current_command_index += 1
        self.current_command = ParserHelper.normalize(self.commands[self.current_command_index])

        tokens = self.current_command.split(' ')
        self.current_arg0 = tokens[0]
        self.current_arg1 = tokens[1] if len(tokens) > 1 else ''
        self.current_arg2 = tokens[2] if len(tokens) > 2 else ''

    def getCurrentCommandArg0(self):
        return self.current_arg0

    def getCurrentCommandArg1(self):
        return self.current_arg1

    def getCurrentCommandArg2(self):
        return self.current_arg2
