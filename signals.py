from enum import Enum


class DataStackSignals(Enum):
    Push = 0
    Pop = 1


class ARLatch(Enum):
    PC = 0
    TOS = 1


class IRLatch(Enum):
    MEM = 0


class PCLatch(Enum):
    IR = 0
    INC = 1


class TosLatch(Enum):
    MEM = 0
    IR = 1
    BufferRegister = 2
    ALU = 3


class ValueToALULatch(Enum):
    GetValues = 0


class AluLatch(Enum):
    SUM = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MOD = 4
    NOT_EQ = 5
    EQ = 6
    MORE = 7
    LESS = 8


class MemorySignal(Enum):
    MemRead = 0
    MemWrite = 1
    TOS = 2


class MCAdrLatch(Enum):
    IR = 0
    INC = 1
    ZERO = 2


class BRLatch(Enum):
    DS = 0


class checkFlag(Enum):
    z = 0
    n = 1
    v = 2


class JUMPS(Enum):
    JMP = 0
    JZS = 1


class IOLatch(Enum):
    PRINT = 0
    READ = 1
    EMIT = 2


class PROG(Enum):
    HALT = 0
