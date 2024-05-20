import json
from enum import Enum
from collections import namedtuple


class Opcode(str, Enum):
    SUM = "sum"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    MOD = "mod"

    DUP = "dup"
    DROP = "drop"
    SWAP = "swap"

    EQ = "eq"
    MORE = "more"
    LESS = "less"

    PRINT = "print"
    READ = "read"
    PUSH = "push"
    INPUT = "input"
    SET_ADR = "set_addr"
    SAVE_VAR = "save_var"
    VAR_ON_TOP = "var_on_top"

    JF = "jF"
    JMP = "jmp"
    HALT = "halt"

    def __str__(self):
        return str(self.value)


class Term(namedtuple("Term", "line word symbol")):
    """Описание символов из текста программы в виде (строка номер_в_строке символ)"""


def write_code(filename, code):
    with open(filename, "w", encoding="utf-8") as file:
        buffer = []
        for instruction in code:
            buffer.append(json.dumps(instruction))
        file.write("[" + ",\n".join(buffer) + "]")


def read_code(filename):
    with open(filename, encoding="utf-8") as file:
        code = json.loads(file.read())\

    for instraction in code:
        instraction["opcode"] = Opcode(instraction["opcode"])

        if "term" in instraction:
            instraction["term"] = Term(instraction["term"][0], instraction["term"][1], instraction["term"][2])
    return code
