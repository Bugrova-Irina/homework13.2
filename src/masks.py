import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(
    "..//homework_13.2/logs/masks.log", "w", encoding="utf-8"
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(number: str) -> str:
    """Принимает на вход номер карты и возвращает ее маску"""
    logger.info("Введен номер карты")
    if number.isdigit() and len(number) == 16:
        logger.info("Создана маска номера карты")
        logger.info("Приложение закончило работу.")
        return f"{number[0:4]} {number[4:6]}** **** {number[12:]}"
    else:
        logger.error("Введен некорректный номер карты")
        logger.info("Приложение закончило работу.")
        raise ValueError("Введен некорректный номер карты")


def get_mask_account(account: str) -> str:
    """Принимает на вход номер счета и возвращает его маску"""
    logger.info("Введен номер счета.")
    list_of_numbers_account = ["**"]

    if account.isdigit() and len(account) == 20:
        list_of_numbers_account.append(account[-4:])
        mask_account = "".join(list_of_numbers_account)
        logger.info("Создана маска номера счета")
        logger.info("Приложение закончило работу.")
        return mask_account

    else:
        logger.error("Введен некорректный номер счета")
        logger.info("Приложение закончило работу.")
        raise ValueError("Введен некорректный номер счета")


if __name__ == "__main__":
    get_mask_account("73654108430135874305")
    # get_mask_card_number('7000792289606361')
