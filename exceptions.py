class InvalidInputError(Exception):
    def __init__(self, line_number, word_number, word):
        super().__init__(f"Error: invalid input [{line_number, word_number, word}]")


class NestedProcedureCreationError(Exception):
    def __init__(self, line_number, word_number, word):
        super().__init__(f"Error: cannot make new procedure in another procedure [{line_number, word_number, word}]")


class EndingProcedureError(Exception):
    def __init__(self, line_number, word_number, word):
        super().__init__(f"Error: cannot end the procedure [{line_number, word_number, word}]")


class StartedProcedureInBranchError(Exception):
    def __init__(self, line_number, word_number, word):
        super().__init__(f"Error: cannot start making procedure in branch [{line_number, word_number, word}]")


class StartedProcedureInLoopError(Exception):
    def __init__(self, line_number, word_number, word):
        super().__init__(f"Error: cannot start making procedure in loop [{line_number, word_number, word}]")


class EndingProcedureBeforeClosingBranchError(Exception):
    def __init__(self, line_number, word_number, word):
        super().__init__(
            f"Error: you need to close a branch before ending procedure " f"[{line_number, word_number, word}]"
        )


class EndingProcedureBeforeClosingLoopError(Exception):
    def __init__(self, line_number, word_number, word):
        super().__init__(f"Error: you need to close a loop before ending procedure [{line_number, word_number, word}]")


class BranchesNotBalancedError(Exception):
    def __init__(self):
        super().__init__("Error: not balanced count of 'if' and 'endif'")


class LoopNotBalancedError(Exception):
    def __init__(self):
        super().__init__("Error: not balanced count of 'begin' and 'until'")


class WrongTranslatorArgumentsError(Exception):
    def __init__(self):
        super().__init__("Error: wrong number of arguments (translator.py <input_file> <output_file>)")


class WrongMachineArgumentsError(Exception):
    def __init__(self):
        super().__init__("Error: wrong number of arguments (machine.py <machine_code_file> <input_file> <log_file>")


class StackOverflowError(Exception):
    def __init__(self, max_size):
        super().__init__(f"Error: stack is overflowed (max_size is {max_size})")


class StackUnderflowError(Exception):
    def __init__(self):
        super().__init__("Error: stack is underflow")


class InvalidSignalError(Exception):
    def __init__(self, signal):
        super().__init__(f"Error: signal {signal} does not exist")


class NewBufferInProcedureError(Exception):
    def __init__(self):
        super().__init__(f"Error: cannot make new buffer in procedure")
