from enum import Enum


class ASMLineType(Enum):
    EMPTY_LINE = 0
    COMMENT = 1
    LABEL = 2
    C_COMMAND = 3
    A_COMMAND = 4
