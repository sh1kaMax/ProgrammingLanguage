import sys
from data_path import DataPath
from control_unit import ControlUnit
from exceptions import *
from isa import *


def main(code_file, input_file):
    code = read_code(code_file)
    with open(input_file, encoding="utf-8") as file:
        inputs = file.read().strip()
        input_token = []
        for char in inputs:
            input_token.append(char)

    data_path = DataPath(code, input_token)
    control_unit = ControlUnit(data_path)
    control_unit.run_machine()


if __name__ == "__main__":
    code_input = "./programs/test_machine_code"
    input_file_name = "./programs/cat_input"

    main(code_input, input_file_name)
