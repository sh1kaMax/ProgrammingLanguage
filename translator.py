import sys

from isa import Opcode, Term, write_code


commands = {
    "+",
    "-",
    "*",
    "/",
    "mod",
    "dup",
    "drop",
    "swap",
    "begin",
    "until",
    "=",
    ">",
    "<",
    ".",
    "exit",
    "!",
    "@",
    "#",
    "if",
    "else",
    "endif"
}


def is_number(maybe_number):
    try:
        int(maybe_number)
        return True
    except ValueError:
        return False


def symbol2opcode(symbol):
    return {
        "+": Opcode.SUM.value,
        "-": Opcode.SUB.value,
        "*": Opcode.MUL.value,
        "/": Opcode.DIV.value,
        "mod": Opcode.MOD.value,
        "dup": Opcode.DUP.value,
        "drop": Opcode.DROP.value,
        "swap": Opcode.SWAP.value,
        "=": Opcode.EQ.value,
        ">": Opcode.MORE.value,
        "<": Opcode.LESS.value,
        ".": Opcode.PRINT.value,
        "exit": Opcode.HALT.value,
        "!": Opcode.VAR.value,
        "@": Opcode.VAR_ON_TOP.value,
        "#": Opcode.READ.value
    }.get(symbol)


def text2terms(text):
    terms = []
    for number, line in enumerate(text.split("\n"), 1):
        words = line.split(" ")
        if len(words) == 1 and words[0] in commands:
            terms.append(Term(number, line))
        if len(words) == 1 and is_number(words[0]):
            terms.append((Term(number, line)))
        if len(words) == 2:
            if words[0] == 'variable' or words[1] in commands:
                terms.append(Term(number, line))
    return terms


def translate(text):
    terms = text2terms(text)
    machine_code = []
    jmp_stack = []
    else_flag = False
    count = 0
    for term in terms:
        words = term.symbol.split(" ")
        if len(words) == 1:
            if words[0] == "if":
                machine_code.append(None)
                jmp_stack.append(count)
            elif words[0] == "else":
                if_index = jmp_stack.pop()
                machine_code[if_index] = ({"index": if_index, "opcode": Opcode.JF.value, "arg": count + 1, "term": terms[if_index]})
                machine_code.append(None)
                jmp_stack.append(count)
                else_flag = True
            elif words[0] == "endif":
                if_index = jmp_stack.pop()
                count -= 1
                if else_flag:
                    machine_code[if_index] = ({"index": if_index, "opcode": Opcode.JMP.value, "arg": count + 1, "tern": terms[if_index]})
                else:
                    machine_code[if_index] = ({"index": if_index, "opcode": Opcode.JF.value, "arg": count + 1, "term": terms[if_index]})
            elif words[0] == "begin":
                jmp_stack.append(count)
                count -= 1
            elif words[0] == "until":
                jmp_index = jmp_stack.pop()
                machine_code.append({"index": count, "opcode": Opcode.JF.value, "arg": jmp_index, "term": terms[count]})
            elif is_number(words[0]):
                machine_code.append({"index": count, "opcode": Opcode.PUSH.value, "arg": words[0], "term": term})
            else:
                machine_code.append({"index": count, "opcode": symbol2opcode(words[0]), "term": term})
        else:
            print("Hi")
        count += 1
    return machine_code


if __name__ == "__main__":
    test = ("begin\n"
            "#\n"
            "dup\n"
            "0\n"
            "=\n"
            "if\n"
            ".\n"
            "else\n"
            "#\n"
            "endif\n"
            ".\n"
            "until"
            )
    # assert len(sys.argv) == 3, "Error: should be 3 arguments translator.py <input> <output>"
    code = translate(test)
    for i in code:
        print(i)
