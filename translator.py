import sys

from isa import Opcode, Term, write_code
from exceptions import *

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

loop_branch_commands = {
    "if",
    "else",
    "endif",
    "begin",
    "until"
}

variable_names = []

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
        "!": Opcode.SAVE_VAR.value,
        "@": Opcode.VAR_ON_TOP.value,
        "#": Opcode.READ.value
    }.get(symbol)


def text2terms(text):
    terms = []
    procedures = {}
    is_procedure = False
    is_procedure_name = False
    branch_counter = 0
    loop_counter = 0
    procedure_name = ""
    for line_number, line in enumerate(text.split("\n"), 1):
        line_words = line.strip().split(" ")
        for word_number, word in enumerate(line.strip().split(" "), 1):
            if is_procedure_name:
                procedure_name = str(word)
                procedures[procedure_name] = []
                is_procedure_name = False
            elif is_number(word) or word in commands:
                if is_procedure:
                    procedures[procedure_name].append(Term(line_number, word_number, word))
                else:
                    terms.append(Term(line_number, word_number, word))
            elif word == ":":
                if branch_counter == 0 and loop_counter == 0:
                    if not is_procedure:
                        is_procedure = True
                        is_procedure_name = True
                    else:
                        raise NestedProcedureCreationError(line_number, word_number, word)
                else:
                    if branch_counter == 0:
                        raise StartedProcedureInBranchError(line_number, word_number, word)
                    if loop_counter == 0:
                        raise StartedProcedureInLoopError(line_number, word_number, word)
            elif word == ";":
                if branch_counter == 0 and loop_counter == 0:
                    if is_procedure:
                        is_procedure = False
                    else:
                        raise EndingProcedureError(line_number, word_number, word)
                else:
                    if branch_counter == 0:
                        raise EndingProcedureBeforeClosingBranchError(line_number, word_number, word)
                    if loop_counter == 0:
                        raise EndingProcedureBeforeClosingLoopError(line_number, word_number, word)
            elif word in procedures.keys():
                for procedure_term in procedures[word]:
                    terms.append(procedure_term)
            else:
                if line_words[word_number] == '!' or line_words[word_number] == '@':
                    if word not in variable_names:
                        variable_names.append(word)
                    if is_procedure:
                        procedures[procedure_name].append(Term(line_number, word_number, word))
                    else:
                        terms.append(Term(line_number, word_number, word))
                else:
                    raise InvalidInputError(line_number, word_number, word)

            if word == "if":
                branch_counter -= 1
            if word == "endif":
                branch_counter += 1
            if word == "begin":
                loop_counter -= 1
            if word == "until":
                loop_counter += 1
    if branch_counter < 0:
        raise BranchesNotBalancedError
    if loop_counter < 0:
        raise LoopNotBalancedError
    return terms


def translate(text):
    terms = text2terms(text)
    machine_code = []
    jmp_stack = []
    else_flag = False
    count = 0
    for term in terms:
        words = term.symbol.split(" ")
        if words[0] == "if":
            machine_code.append(None)
            jmp_stack.append(count)
        elif words[0] == "else":
            if_index = jmp_stack.pop()
            machine_code[if_index] = {"index": if_index, "opcode": Opcode.JF.value, "arg": count + 1, "term": terms[if_index]}
            machine_code.append(None)
            jmp_stack.append(count)
            else_flag = True
        elif words[0] == "endif":
            if_index = jmp_stack.pop()
            count -= 1
            if else_flag:
                machine_code[if_index] = {"index": if_index, "opcode": Opcode.JMP.value, "arg": count + 1, "tern": terms[if_index]}
            else:
                machine_code[if_index] = {"index": if_index, "opcode": Opcode.JF.value, "arg": count + 1, "term": terms[if_index]}
        elif words[0] == "begin":
            jmp_stack.append(count)
            count -= 1
        elif words[0] == "until":
            jmp_index = jmp_stack.pop()
            machine_code.append({"index": count, "opcode": Opcode.JF.value, "arg": jmp_index, "term": terms[count]})
        elif is_number(words[0]):
            machine_code.append({"index": count, "opcode": Opcode.PUSH.value, "arg": words[0], "term": term})
        elif words[0] in variable_names:
            machine_code.append({"index": count, "opcode": Opcode.SET_ADR.value, "arg": words[0], "term": term})
        else:
            machine_code.append({"index": count, "opcode": symbol2opcode(words[0]), "term": term})
        count += 1
    return machine_code


def main(source, target):
    with open(source, encoding="utf-8") as file:
        source = file.read()

    code = translate(source)

    write_code(target, code)
    print(f'Translated successfully. Source LoC: {len(source.split("\n"))} Code instruction: {len(code)}')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise WrongTranslatorArgumentsError
    _, input_file, output_file = sys.argv
    main(input_file, output_file)
