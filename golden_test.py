import contextlib
import io
import logging
import os
import tempfile

import machine
import pytest
import translator


@pytest.mark.golden_test("golden/*.yml")
def test_program(golden, caplog):
    caplog.set_level(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s]  %(message)s")

    caplog.handler.setFormatter(formatter)
    with tempfile.TemporaryDirectory() as tmpdirname:
        code = os.path.join(tmpdirname, "code")
        inputs = os.path.join(tmpdirname, "inputs")
        target = os.path.join(tmpdirname, "target")
        with open(code, "w", encoding="utf-8") as f:
            f.write(golden["in_source"])
        with open(inputs, "w", encoding="utf-8") as f:
            f.write(golden["in_stdin"])

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator.main(code, target)
            print("============================================================")
            machine.main(target, inputs)

        with open(target, encoding="utf-8") as f:
            machine_code = f.read()

        assert machine_code == golden.out["out_code"]
        assert stdout.getvalue()[:-1] == golden.out["out_stdout"]
        assert caplog.text[:-1] == golden.out["out_log"]
