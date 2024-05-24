from isa import Opcode
from signals import *
from data_path import INSTRACTION_LIMIT
from exceptions import InvalidSignalError


def opcode2microcode(opcode):
    return {
        Opcode.SUM: 2,
        Opcode.SUB: 4,
        Opcode.MUL: 6,
        Opcode.DIV: 8,
        Opcode.MOD: 10,
        Opcode.DUP: 12,
        Opcode.DROP: 14,
        Opcode.SWAP: 16,
        Opcode.EQ: 19,
        Opcode.MORE: 21,
        Opcode.LESS: 23,
        Opcode.PUSH: 25,
        Opcode.ADDR_ON_TOP: 27,
        Opcode.SAVE_VAR: 29,
        Opcode.VAR_ON_TOP: 32,
        Opcode.JZS: 35,
        Opcode.JMP: 38,
        Opcode.PRINT: 41,
        Opcode.READ: 44,
        Opcode.EMIT: 46,
        Opcode.HALT: 49,
        Opcode.NOT_EQ: 50,
    }.get(opcode)


microcode = [
    # Fetch next instraction - 0
    [ARLatch.PC, MemorySignal.MemRead, MCAdrLatch.INC],
    [IRLatch.MEM, MCAdrLatch.IR],
    # SUM - 2
    [ValueToALULatch.GetValues, AluLatch.SUM, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, MCAdrLatch.ZERO],
    # SUB - 4
    [ValueToALULatch.GetValues, AluLatch.SUB, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, MCAdrLatch.ZERO],
    # MUL - 6
    [ValueToALULatch.GetValues, AluLatch.MUL, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, MCAdrLatch.ZERO],
    # DIV - 8
    [ValueToALULatch.GetValues, AluLatch.DIV, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, MCAdrLatch.ZERO],
    # MOD - 10
    [ValueToALULatch.GetValues, AluLatch.MOD, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, MCAdrLatch.ZERO],
    # DUP - 12
    [DataStackSignals.Push, MCAdrLatch.INC],
    [PCLatch.INC, MCAdrLatch.ZERO],
    # DROP - 14
    [DataStackSignals.Pop, MCAdrLatch.INC],
    [PCLatch.INC, MCAdrLatch.ZERO],
    # SWAP - 16
    [BRLatch.DS, MCAdrLatch.INC],
    [DataStackSignals.Push, TosLatch.BufferRegister, MCAdrLatch.INC],
    [PCLatch.INC, MCAdrLatch.ZERO],
    # EQ - 19
    [ValueToALULatch.GetValues, AluLatch.EQ, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, MCAdrLatch.ZERO],
    # MORE - 21
    [ValueToALULatch.GetValues, AluLatch.MORE, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, MCAdrLatch.ZERO],
    # LESS - 23
    [ValueToALULatch.GetValues, AluLatch.LESS, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, MCAdrLatch.ZERO],
    # PUSH - 25
    [DataStackSignals.Push, TosLatch.IR, MCAdrLatch.INC],
    [PCLatch.INC, MCAdrLatch.ZERO],
    # ADR_ON_TOP - 27
    [DataStackSignals.Push, TosLatch.IR, MCAdrLatch.INC],
    [PCLatch.INC, MCAdrLatch.ZERO],
    # SAVE_VAR - 29
    [ARLatch.TOS, BRLatch.DS, TosLatch.BufferRegister, MemorySignal.TOS, MCAdrLatch.INC],
    [MemorySignal.MemWrite, BRLatch.DS, TosLatch.BufferRegister, MCAdrLatch.INC],
    [PCLatch.INC, MCAdrLatch.ZERO],
    # VAR_ON_TOP - 32
    [ARLatch.TOS, MemorySignal.MemRead, MCAdrLatch.INC],
    [IRLatch.MEM, TosLatch.IR, MCAdrLatch.INC],
    [PCLatch.INC, MCAdrLatch.ZERO],
    # JZS - 35
    [DataStackSignals.Push, TosLatch.IR, JUMPS.JZS, MCAdrLatch.INC],
    [DataStackSignals.Pop, BRLatch.DS, TosLatch.BufferRegister, MCAdrLatch.INC],
    [PCLatch.INC, MCAdrLatch.ZERO],
    # JMP - 38
    [DataStackSignals.Push, TosLatch.IR, JUMPS.JMP, MCAdrLatch.INC],
    [BRLatch.DS, TosLatch.BufferRegister, MCAdrLatch.INC],
    [PCLatch.INC, MCAdrLatch.ZERO],
    # PRINT - 41
    [IOLatch.PRINT, MCAdrLatch.INC],
    [BRLatch.DS, TosLatch.BufferRegister, MCAdrLatch.INC],
    [PCLatch.INC, MCAdrLatch.ZERO],
    # READ - 44
    [DataStackSignals.Push, MCAdrLatch.INC],
    [IOLatch.READ, PCLatch.INC, MCAdrLatch.ZERO],
    # EMIT - 46
    [IOLatch.EMIT, MCAdrLatch.INC],
    [BRLatch.DS, TosLatch.BufferRegister, MCAdrLatch.INC],
    [PCLatch.INC, MCAdrLatch.ZERO],
    # HALT - 49
    [PROG.HALT],
    # NOT_EQ - 50
    [ValueToALULatch.GetValues, AluLatch.NOT_EQ, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, MCAdrLatch.ZERO],
]


class ControlUnit:
    mcAdr = None
    mcR = None
    datapath = None
    tick = None

    def __init__(self, datapath):
        self.mcAdr = 0
        self.mcR = []
        self.datapath = datapath
        self.tick = 0

    def inc_tick(self):
        self.tick += 1

    def execute_instraction(self, signals):
        for signal in signals:
            if isinstance(signal, ARLatch):
                self.datapath.address_register_latch(signal)
            elif isinstance(signal, MemorySignal):
                self.datapath.memory_latch(signal)
            elif isinstance(signal, MCAdrLatch):
                self.mcAdr_latch(signal)
            elif isinstance(signal, IRLatch):
                self.datapath.mem_value_to_ir()
            elif isinstance(signal, ValueToALULatch):
                self.datapath.alu_values_get()
            elif isinstance(signal, AluLatch):
                self.datapath.alu_latch(signal)
            elif isinstance(signal, TosLatch):
                self.datapath.tos_latch(signal)
            elif isinstance(signal, PCLatch):
                self.datapath.pc_latch(signal)
            elif isinstance(signal, DataStackSignals):
                self.datapath.data_stack_latch(signal)
            elif isinstance(signal, BRLatch):
                self.datapath.write_buffer_register()
            elif isinstance(signal, IOLatch):
                self.datapath.io_latch(signal)
            elif isinstance(signal, JUMPS):
                self.datapath.jump(signal)
            elif isinstance(signal, PROG):
                raise StopIteration
            else:
                raise InvalidSignalError(signal)

    def mcAdr_latch(self, signal):
        match signal:
            case MCAdrLatch.IR:
                self.mcAdr = opcode2microcode(self.datapath.instraction_register['opcode'])
            case MCAdrLatch.INC:
                self.mcAdr += 1
            case MCAdrLatch.ZERO:
                self.mcAdr = 0

    def run_machine(self):
        instraction_counter = 0
        try:
            while instraction_counter < INSTRACTION_LIMIT:
                self.execute_instraction(microcode[self.mcAdr])
                instraction_counter += 1
        except StopIteration:
            pass
        except IOError:
            pass

        print("output_buffer:", repr("".join(self.datapath.output_buffer)))
