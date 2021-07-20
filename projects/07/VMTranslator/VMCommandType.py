from enum import Enum


class VMCommandType(Enum):
    C_ARITHMETIC = 'arithmetic'
    C_PUSH = 'push'
    C_POP = 'pop'
    C_LABEL = 'label'
    C_GOTO = 'goto'
    C_IF = 'if'
    C_FUNCTION = 'function'
    C_RETURN = 'return'
    C_CALL = 'call'
