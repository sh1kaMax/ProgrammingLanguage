import logging
from typing import ClassVar

from data_path import INSTRACTION_LIMIT
from exceptions import InvalidSignalError
from isa import Opcode
from signals import (
    JUMPS,
    PROG,
    AluLatch,
    ALUValues,
    ARLatch,
    BRLatch,
    DSLatch,
    Instraction,
    IOLatch,
    IRLatch,
    MCAdrLatch,
    MEMSignal,
    PCLatch,
    TosLatch,
)


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
    mc_adr = None
    datapath = None
    tick = None
    instraction_count = None
    signal_handlers: ClassVar[dict] = {}

    def __init__(self, datapath):
        self.mc_adr = 0
        self.datapath = datapath
        self.tick = 0
        self.instraction_count = 0
        self.signal_handlers = {
            ARLatch: [getattr(self.datapath, "address_register_latch"), 2],
            MEMSignal: [getattr(self.datapath, "memory_latch"), 2],
            MCAdrLatch: [getattr(self, "mc_adr_latch"), 2],
            IRLatch: [getattr(self.datapath, "mem_value_to_ir"), 1],
            ALUValues: [getattr(self.datapath, "alu_values_get"), 1],
            AluLatch: [getattr(self.datapath, "alu_latch"), 2],
            TosLatch: [getattr(self.datapath, "tos_latch"), 2],
            PCLatch: [getattr(self.datapath, "pc_latch"), 2],
            DSLatch: [getattr(self.datapath, "data_stack_latch"), 2],
            BRLatch: [getattr(self.datapath, "write_buffer_register"), 1],
            IOLatch: [getattr(self.datapath, "io_latch"), 2],
            JUMPS: [getattr(self.datapath, "jump"), 2],
            Instraction: [getattr(self, "inc_instraction_count"), 1],
        }

    def __repr__(self, signal):
        return (
            "TICK: {:4} PC: {:3} ADDR: {:3} mcADDR: {:2} SIGNAL: {:15} TOS: {:6} Z: {:1} N: {:1} V: {:1}\n" "DS: {}"
        ).format(
            str(self.tick),
            str(self.datapath.pc),
            str(self.datapath.address_register),
            str(self.mc_adr),
            str(signal),
            str(self.datapath.top_of_stack) if self.datapath.top_of_stack is not None else "0",
            str(self.datapath.alu.z_flag),
            str(self.datapath.alu.n_flag),
            str(self.datapath.alu.v_flag),
            self.datapath.data_stack.stack,
        )

    def inc_tick(self):
        self.tick += 1

    def inc_instraction_count(self):
        self.instraction_count += 1

    def execute_instraction(self, signals):
        for signal in signals:
            handler_name = self.signal_handlers.get(type(signal))
            if handler_name:
                if handler_name[1] == 2:
                    handler_name[0](signal)
                else:
                    handler_name[0]()
            else:
                if isinstance(signal, PROG):
                    raise StopIteration
                raise InvalidSignalError(signal)
            logging.debug("%s", self.__repr__(signal))
            self.inc_tick()

    def mc_adr_latch(self, signal):
        match signal:
            case MCAdrLatch.IR:
                self.mc_adr = opcode2microcode(self.datapath.instraction_register["opcode"])
            case MCAdrLatch.INC:
                self.mc_adr += 1
            case MCAdrLatch.ZERO:
                self.mc_adr = 0

    def run_machine(self):
        try:
            while self.instraction_count < INSTRACTION_LIMIT:
                self.execute_instraction(microcode[self.mc_adr])
        except StopIteration:
            pass
        except OSError:
            pass
        output = ""
        for stroka in "".join(self.datapath.output_buffer).split("\n"):
            output += f"{4 * '\t'}{stroka}\n"
        logging.debug("output_buffer: \n" + output[0:-1])
        return self.datapath.output_buffer, self.instraction_count, self.tick
