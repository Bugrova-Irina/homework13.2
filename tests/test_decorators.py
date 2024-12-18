import os

import pytest

from src.decorators import log


def test_log() -> None:
    @log("../logs/my_log.txt")
    def my_function(a: int, b: int) -> int:
        return a + b

    assert my_function(1, 2) == 3


def test_filename_decorator() -> None:
    @log("../logs/my_log.doc")
    def my_function(a: int, b: int) -> int:
        return a + b

    with pytest.raises(NameError, match="Файл с неверным расширением"):
        my_function(1, 2)


def test_no_filename(capsys: pytest.CaptureFixture[str]) -> None:
    # @wraps(test_no_filename)
    @log()
    def my_function(a: int, b: int) -> int:

        return a + b

    "Function my_function started"
    my_function(1, 2)
    "Function my_function finished"
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Function my_function started\n3\nmy_function ok\nFunction my_function finished\n"
    )


def test_bad_function() -> None:
    @log("../logs/my_log.txt")
    def my_function(a: int, b: int) -> float:

        return a / b

    try:
        my_function(5, 0)

    except ZeroDivisionError:
        os.makedirs(os.path.dirname("../logs/my_log.txt"), exist_ok=True)
        with open("../logs/my_log.txt", "a", encoding="utf-8") as file:
            file.write("my_function error: division by zero. Inputs: (5, 0), {}")
