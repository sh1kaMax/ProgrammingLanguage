import logging

from data_stack import Stack
from signals import *
from alu import ALU
STACK_SIZE = 64
SIZE_FOR_VARS = 150
INSTRACTION_LIMIT = 100000


class Memory:
    memory = None
    start_of_variables = None
    value = None

    def __init__(self, code, start_of_variables):
        self.start_of_variables = start_of_variables
        self.memory = [0] * (len(code) + 1)
        self.value = 0
        self.memory[0] = start_of_variables
        for number, instraction in enumerate(code, 1):
            self.memory[number] = instraction

    def read(self, adr):
        self.value = self.memory[adr]

    def write(self, adr):
        self.memory[adr] = self.value


class DataPath:
    data_stack = None
    top_of_stack = None
    alu = None
    instraction_register = None
    buffer_register = None
    address_register = None
    memory = None
    pc = None
    input_buffer = None
    output_buffer = None

    def __init__(self, code, input_token, start_of_variables):
        self.data_stack = Stack(STACK_SIZE)
        self.alu = ALU()
        self.instraction_register: map = {}
        self.buffer_register = 0
        self.memory = Memory(code, start_of_variables)
        self.pc = 1
        self.input_buffer = input_token
        self.output_buffer = []

    def push_value(self):
        self.data_stack.push(self.top_of_stack)

    def pop_value(self):
        return self.data_stack.pop()

    def write_buffer_register(self):
        self.buffer_register = self.pop_value()

    def mem_value_to_ir(self):
        if isinstance(self.memory.value, int):
            self.instraction_register = {"arg": self.memory.value}
        else:
            self.instraction_register = self.memory.value

    def tos_latch(self, signal):
        match signal:
            case TosLatch.ALU:
                self.top_of_stack = self.alu.value
            case TosLatch.BR:
                self.top_of_stack = self.buffer_register
            case TosLatch.MEM:
                self.top_of_stack = self.memory[self.address_register]
            case TosLatch.IR:
                self.top_of_stack = int(self.instraction_register["arg"])
            case TosLatch.IR_VAR:
                self.top_of_stack = int(self.instraction_register["arg"]) + self.memory.start_of_variables

    def pc_latch(self, signal):
        match signal:
            case PCLatch.IR:
                self.pc = self.instraction_register["arg"]
            case PCLatch.INC:
                self.pc += 1

    def alu_values_get(self):
        self.alu.first_value = self.top_of_stack
        self.alu.second_value = self.data_stack.pop()

    def alu_latch(self, signal):
        match signal:
            case AluLatch.SUM:
                self.alu.do_operation(0)
            case AluLatch.SUB:
                self.alu.do_operation(1)
            case AluLatch.MUL:
                self.alu.do_operation(2)
            case AluLatch.DIV:
                self.alu.do_operation(3)
            case AluLatch.MOD:
                self.alu.do_operation(4)
            case AluLatch.NOT_EQ:
                self.alu.do_operation(5)
            case AluLatch.EQ:
                self.alu.do_operation(6)
            case AluLatch.MORE:
                self.alu.do_operation(7)
            case AluLatch.LESS:
                self.alu.do_operation(8)

    def address_register_latch(self, signal):
        match signal:
            case ARLatch.PC:
                self.address_register = self.pc
            case ARLatch.TOS:
                self.address_register = self.top_of_stack

    def data_stack_latch(self, signal):
        match signal:
            case DSLatch.Push:
                self.push_value()
            case DSLatch.Pop:
                self.pop_value()

    def memory_latch(self, signal):
        match signal:
            case MEMSignal.READ:
                self.memory.read(self.address_register)
            case MEMSignal.WRITE:
                self.memory.write(self.address_register)
            case MEMSignal.TOS:
                self.memory.value = self.top_of_stack

    def io_latch(self, signal):
        match signal:
            case IOLatch.PRINT:
                self.output_buffer.append(str(self.top_of_stack))
                logging.debug("output: " + ''.join(self.output_buffer) + "<<" + str(self.top_of_stack))
            case IOLatch.READ:
                if len(self.input_buffer) == 0:
                    logging.warning("No input from user!")
                    raise IOError()
                self.top_of_stack = ord(self.input_buffer.pop(0))
                logging.debug("input: " + chr(self.top_of_stack))
            case IOLatch.EMIT:
                self.output_buffer.append(chr(self.top_of_stack))
                logging.debug("output: " + ''.join(self.output_buffer) + "<<" + chr(self.top_of_stack))

    def jump(self, signal):
        match signal:
            case JUMPS.JZS:
                if self.alu.z_flag == 1:
                    self.pc = self.top_of_stack
            case JUMPS.JMP:
                self.pc = self.top_of_stack
