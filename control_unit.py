from isa import Opcode
import logging
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
    [ARLatch.PC, MEMSignal.READ, MCAdrLatch.INC],
    [IRLatch.MEM, Instraction.INC, MCAdrLatch.IR],
    # SUM - 2
    [ALUValues.VAR, AluLatch.SUM, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # SUB - 4
    [ALUValues.VAR, AluLatch.SUB, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # MUL - 6
    [ALUValues.VAR, AluLatch.MUL, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # DIV - 8
    [ALUValues.VAR, AluLatch.DIV, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # MOD - 10
    [ALUValues.VAR, AluLatch.MOD, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # DUP - 12
    [DSLatch.Push, MCAdrLatch.INC],
    [PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # DROP - 14
    [DSLatch.Pop, MCAdrLatch.INC],
    [PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # SWAP - 16
    [BRLatch.DS, MCAdrLatch.INC],
    [DSLatch.Push, TosLatch.BR, MCAdrLatch.INC],
    [PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # EQ - 19
    [ALUValues.VAR, AluLatch.EQ, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # MORE - 21
    [ALUValues.VAR, AluLatch.MORE, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # LESS - 23
    [ALUValues.VAR, AluLatch.LESS, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # PUSH - 25
    [DSLatch.Push, TosLatch.IR, MCAdrLatch.INC],
    [PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # ADR_ON_TOP - 27
    [DSLatch.Push, TosLatch.IR_VAR, MCAdrLatch.INC],
    [PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # SAVE_VAR - 29
    [ARLatch.TOS, BRLatch.DS, TosLatch.BR, MEMSignal.TOS, MCAdrLatch.INC],
    [MEMSignal.WRITE, BRLatch.DS, TosLatch.BR, MCAdrLatch.INC],
    [PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # VAR_ON_TOP - 32
    [ARLatch.TOS, MEMSignal.READ, MCAdrLatch.INC],
    [IRLatch.MEM, TosLatch.IR, MCAdrLatch.INC],
    [PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # JZS - 35
    [DSLatch.Push, TosLatch.IR, JUMPS.JZS, MCAdrLatch.INC],
    [DSLatch.Pop, BRLatch.DS, TosLatch.BR, MCAdrLatch.INC],
    [PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # JMP - 38
    [DSLatch.Push, TosLatch.IR, JUMPS.JMP, MCAdrLatch.INC],
    [BRLatch.DS, TosLatch.BR, MCAdrLatch.INC],
    [PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # PRINT - 41
    [IOLatch.PRINT, MCAdrLatch.INC],
    [BRLatch.DS, TosLatch.BR, MCAdrLatch.INC],
    [PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # READ - 44
    [DSLatch.Push, MCAdrLatch.INC],
    [IOLatch.READ, Instraction.INC, PCLatch.INC, MCAdrLatch.ZERO],
    # EMIT - 46
    [IOLatch.EMIT, MCAdrLatch.INC],
    [BRLatch.DS, TosLatch.BR, MCAdrLatch.INC],
    [PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
    # HALT - 49
    [Instraction.INC, PROG.HALT],
    # NOT_EQ - 50
    [ALUValues.VAR, AluLatch.NOT_EQ, MCAdrLatch.INC],
    [TosLatch.ALU, PCLatch.INC, Instraction.INC, MCAdrLatch.ZERO],
]


class ControlUnit:
    mcAdr = None
    datapath = None
    tick = None
    instraction_count = None

    def __init__(self, datapath):
        self.mcAdr = 0
        self.datapath = datapath
        self.tick = 0
        self.instraction_count = 0

    def __repr__(self, signal):
        state_repr = ("TICK: {:4} PC: {:3} ADDR: {:3} mcADDR: {:2} SIGNAL: {:15} TOS: {:6} Z: {:1} N: {:1} V: {:1}\n"
                      "DS: {}").format(
            str(self.tick),
            str(self.datapath.pc),
            str(self.datapath.address_register),
            str(self.mcAdr),
            str(signal),
            str(self.datapath.top_of_stack) if self.datapath.top_of_stack is not None else '0',
            str(self.datapath.alu.z_flag),
            str(self.datapath.alu.n_flag),
            str(self.datapath.alu.v_flag),
            self.datapath.data_stack.stack
        )
        return state_repr

    def inc_tick(self):
        self.tick += 1


    def execute_instraction(self, signals):
        for signal in signals:
            if isinstance(signal, ARLatch):
                self.datapath.address_register_latch(signal)
            elif isinstance(signal, MEMSignal):
                self.datapath.memory_latch(signal)
            elif isinstance(signal, MCAdrLatch):
                self.mcAdr_latch(signal)
            elif isinstance(signal, IRLatch):
                self.datapath.mem_value_to_ir()
            elif isinstance(signal, ALUValues):
                self.datapath.alu_values_get()
            elif isinstance(signal, AluLatch):
                self.datapath.alu_latch(signal)
            elif isinstance(signal, TosLatch):
                self.datapath.tos_latch(signal)
            elif isinstance(signal, PCLatch):
                self.datapath.pc_latch(signal)
            elif isinstance(signal, DSLatch):
                self.datapath.data_stack_latch(signal)
            elif isinstance(signal, BRLatch):
                self.datapath.write_buffer_register()
            elif isinstance(signal, IOLatch):
                self.datapath.io_latch(signal)
            elif isinstance(signal, JUMPS):
                self.datapath.jump(signal)
            elif isinstance(signal, Instraction):
                self.instraction_count += 1
            elif isinstance(signal, PROG):
                raise StopIteration
            else:
                raise InvalidSignalError(signal)
            logging.debug("%s", self.__repr__(signal))
            self.inc_tick()

    def mcAdr_latch(self, signal):
        match signal:
            case MCAdrLatch.IR:
                self.mcAdr = opcode2microcode(self.datapath.instraction_register['opcode'])
            case MCAdrLatch.INC:
                self.mcAdr += 1
            case MCAdrLatch.ZERO:
                self.mcAdr = 0

    def run_machine(self):
        try:
            while self.instraction_count < INSTRACTION_LIMIT:
                self.execute_instraction(microcode[self.mcAdr])
        except StopIteration:
            pass
        except IOError:
            pass
        output = ""
        for stroka in ''.join(self.datapath.output_buffer).split("\n"):
            output += f'{4 * '\t'}{stroka}\n'
        logging.debug("output_buffer: \n" + output[0:-1])
        return self.datapath.output_buffer, self.instraction_count, self.tick
