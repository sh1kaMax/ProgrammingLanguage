from enum import Enum


class StackSignals(Enum):
    DSPush = 0
    DSPop = 1
    RSPush = 2
    RSPop = 3


class ARLatch(Enum):
    IR = 0
    TOS = 1
    INC = 2


class TosLatch(Enum):
    MEM = 0
    IR = 1
    BufferRegister = 2
    ALU = 3


class DataStackToALULatch(Enum):
    DataStack = 0
    Zero = 1


class AluLatch(Enum):
    SUM = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MOD = 4


class MemorySignal(Enum):
    MemRead = 0
    MemWrite = 1