import re
from fastapi import HTTPException

from PPgroup5.pythonBackEnd.database.database import session, User


def is_telephone_number(telephone: str):
    """
    Проверяет, является ли строка телефонным номером.

    Parameters:
    - telephone (str): Строка для проверки.

    Returns:
    - dict: Результат проверки со следующими ключами:
      - "result" (bool): Результат проверки (True - номер телефона, False - не номер телефона).
      - "telephone" (str): Проверенная строка.
      - "details" (str or None): Дополнительные детали о неудачной проверке (если есть).
    """
    if len(telephone) != 11:
        if not (len(telephone) == 12 and telephone.startswith("+")):
            return {"result": False,
                    "telephone": telephone,
                    "details": "length of telephone number"}
        telephone = telephone[1:]
    if not telephone.isdigit():
        return {"result": False,
                "telephone": telephone,
                "details": "telephone number not from digits"}
    return {"result": True,
            "telephone": telephone,
            "details": None}


def error_telephone_userexists():
    """
    Вызывает HTTPException со статусом 409 и сообщением об ошибке для существующего телефонного номера.
    """
    raise HTTPException(status_code=409, detail={
        "status": "error",
        "data": None,
        "details": "such telephone is already exists"
    })


def error_email_userexists():
    """
    Вызывает HTTPException со статусом 409 и сообщением об ошибке для существующего адреса эл. почты.
    """
    raise HTTPException(status_code=409, detail={
        "status": "error",
        "data": None,
        "details": "such email is already exists"
    })


def error_login_udentified():
    """
    Вызывает HTTPException со статусом 409 и сообщением об ошибке для нераспознанного логина.
    """
    raise HTTPException(status_code=409, detail={
        "status": "error",
        "data": None,
        "details": "unidentified login"
    })


def nothing():
    """
    Функция-заглушка, ничего не делает.
    """
    pass


def is_valid_email(email):
    """
    Проверяет, является ли строка email адресом.

    Parameters:
    - email (str): Строка для проверки.

    Returns:
    - bool: True, если строка является валидным email адресом, иначе False.
    """
    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    if not re.match(pattern, email):
        return False
    return True


def is_login(login, func_login_telephone=nothing(), func_login_email=nothing(), func_login_udentified=nothing()):
    """
    Проверяет логин пользователя (телефонный номер или email) и вызывает соответствующую функцию обработки ошибки.

    Parameters:
    - login (str): Логин пользователя (телефонный номер или email).
    - func_login_telephone (function): Функция для обработки ошибки существующего телефонного номера.
    - func_login_email (function): Функция для обработки ошибки существующего email.
    - func_login_udentified (function): Функция для обработки ошибки нераспознанного логина.

    Returns:
    - tuple: Кортеж из телефонного номера, email и объекта пользователя (если найден).
    """
    if is_telephone_number(login)["result"]:
        user = session.query(User).filter(User.telephone_number == login).first()
        if user:
            func_login_telephone()
        telephone_number = is_telephone_number(login)["telephone"]
        email = None
    else:
        if is_valid_email(login):
            user = session.query(User).filter(User.email == login).first()
            if user:
                func_login_email()
            telephone_number = None
            email = login
        else:
            func_login_udentified()
    return telephone_number, email, user
