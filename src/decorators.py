import os
from functools import wraps
from typing import Any


def log(filename: str = "") -> Any:
    """Декоратор, логирующий состояние функции в файл либо в консоль"""

    def logging(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = f"Function {func.__name__} started"

            if filename == "":
                print(start)
                print(func(*args, **kwargs))
                print(f"{func.__name__} ok")
                print(f"Function {func.__name__} finished")

            elif not filename.endswith(".txt"):
                raise NameError("Файл с неверным расширением")

            else:
                try:
                    result = func(*args, **kwargs)
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(
                            f"{start}\n{func.__name__} ok\n{result}\nFunction {func} finished\n"
                        )

                    return result
                except ZeroDivisionError as e:
                    print(f"Error: {e}")
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(
                            f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}\n"
                        )

        return wrapper

    return logging


@log("../homework_13.2/logs/my_log.txt")
def my_function(x: int, y: int) -> float:

    return x / y


my_function(1, 0)

# Ожидаемый вывод в лог-файл mylog.txt при успешном выполнении:
# my_function ok
# Ожидаемый вывод при ошибке:
# my_function error: тип ошибки. Inputs: (1, 2), {}
# Где тип ошибки заменяется на текст ошибки.
