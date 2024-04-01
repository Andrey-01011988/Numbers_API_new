def right_month(month: str) -> bool:
    """
    Проверяет правильно ли ввел месяц пользователь

    :param month: номер месяца
    """
    if 0 < int(month) < 13:
        return True


def right_day(month: str, day: str) -> bool:
    """
    Проверяет соответствие введенного числа месяцу указанному ранее

    :param month: месяц указанный ранее

    :param day: введенный день
    """
    if int(month) in (1, 3, 5, 7, 8, 10, 12) and 0 < int(day) < 32:
        return True
    elif int(month) in (4, 6, 9, 11) and 0 < int(day) < 31:
        return True
    elif int(month) == 2 and 0 < int(day) < 30:
        return True
