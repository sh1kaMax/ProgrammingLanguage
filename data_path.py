from data_stack import Stack
from signals import *
from alu import ALU
STACK_SIZE = 64


class DataPath:
    data_stack = None
    top_of_stack = None
    alu = None
    instraction_register = None
    buffer_register = None
    address_register = None
    memory = None

    def __init__(self, code):
        self.data_stack = Stack(STACK_SIZE)
        self.alu = ALU()
        self.instraction_register: map = {}
        self.buffer_register = 0
        self.memory = []

    def push_value(self, value):
        self.data_stack.push(value)

    def pop_value(self):
        return self.data_stack.pop()

    def read_memory(self):
        self.instraction_register = self.memory[self.address_register]

    def write_memory(self):
        self.memory[self.address_register] = self.data_stack.top_of_stack

    def write_buffer_register(self):
        self.buffer_register = self.pop_value()

    def tos_latch(self, signal):
        match signal:
            case TosLatch.ALU:
                self.top_of_stack = self.alu.value
            case TosLatch.BufferRegister:
                self.top_of_stack = self.buffer_register
            case TosLatch.MEM:
                self.top_of_stack = self.memory[self.address_register]
            case TosLatch.IR:
                self.top_of_stack = self.instraction_register["arg"]

    def second_variable_latch(self, signal):
        match signal:
            case DataStackToALULatch.DataStack:
                self.alu.second_value = self.pop_value()
            case DataStackToALULatch.Zero:
                self.alu.second_value = 0

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

    def address_instraction_latch(self, signal):
        match signal:
            case ARLatch.IR:
                self.address_register = self.instraction_register["arg"]
            case ARLatch.INC:
                self.address_register += 1
            case ARLatch.TOS:
                self.address_register = self.top_of_stack

