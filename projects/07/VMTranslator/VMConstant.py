
IMPLEMENTATION_DIRECTORY = 'HackImplementation'


class VMCmd:
    C_ADD = 'add'
    C_AND = 'and'
    C_EQ = 'eq'
    C_GT = 'gt'
    C_LT = 'lt'
    C_NEG = 'neg'
    C_NOT = 'not'
    C_OR = 'or'
    C_SUB = 'sub'
    C_PUSH = 'push'
    C_POP = 'pop'
    C_LABEL = 'label'
    C_GOTO = 'goto'
    C_IF = 'if-goto'
    C_FUNCTION = 'function'
    C_RETURN = 'return'
    C_CALL = 'call'
    C_INIT = 'init'


class VMSegment:
    S_CONSTANT = 'constant'
    S_LOCAL = 'local'
    S_ARGUMENT = 'argument'
    S_THIS = 'this'
    S_THAT = 'that'
    S_STATIC = 'static'
    S_TEMP = 'temp'
    S_POINTER = 'pointer'


ARITHMETIC_COMMANDS = [VMCmd.C_ADD, VMCmd.C_AND, VMCmd.C_EQ, VMCmd.C_GT,
                       VMCmd.C_LT, VMCmd.C_NEG, VMCmd.C_NOT, VMCmd.C_OR, VMCmd.C_SUB]

BRANCHING_COMMANDS = [VMCmd.C_LABEL, VMCmd.C_IF, VMCmd.C_GOTO]

FUNCTION_COMMANDS = [VMCmd.C_CALL, VMCmd.C_FUNCTION, VMCmd.C_RETURN]

TEMP_LOCATION_IN_RAM = 5

SEGMENT_TRANSLATION = {'local': 'LCL',
                       'argument': 'ARG',
                       'this': 'THIS',
                       'that': 'THAT'}
