import re

from fastapi.responses import JSONResponse

from src.token.token_utils import create_refresh_token, create_access_token, set_refresh_token_cookie


def is_valid_email(email: str) -> bool:
    """
    Проверка формата email.
    """
    email_regex = r"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)"
    return re.match(email_regex, email) is not None


def is_valid_username(username: str) -> bool:
    """Проверяет, что никнейм состоит только из букв, цифр и имеет длину от 3 до 20 символов."""
    if not isinstance(username, str):
        return False
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return bool(re.match(pattern, username)) and len(set(username)) > 2


def is_strong_password(password: str) -> tuple[bool, str]:
    """
    Проверка сложности пароля:
    - Минимальная длина 8 символов.
    - Наличие хотя бы одной заглавной буквы.
    - Наличие хотя бы одной цифры.
    - Наличие хотя бы одного специального символа.
    """
    password_invalids = {
        0: "your password length must be at least 8",
        1: "your password must contain at least 1 capital latin letter",
        2: "your password must contain at least 1 digit",
        3: "your password must contain at least 1 special character",
        4: "your password has too few repeated characters",
    }

    if len(password) < 8:
        return False, password_invalids[0]

    # Проверка на наличие хотя бы одной заглавной буквы
    if not re.search(r'[A-Z]', password):
        return False, password_invalids[1]

    # Проверка на наличие хотя бы одной цифры
    if not re.search(r'\d', password):
        return False, password_invalids[2]

    # Проверка на наличие хотя бы одного специального символа
    if not re.search(r'[\W_]', password):
        return False, password_invalids[3]

    # Проверка на большое количество повторяющихся символов
    if len(set(password)) < 6:
        return False, password_invalids[4]
    return True, ""


def is_valid_create_user_data(
        user_in,
        check_email: bool = True,
        check_name: bool = True,
        check_password: bool = True
) -> tuple[bool, str]:
    if check_email:
        if not is_valid_email(user_in.email):
            return False, "invalid email"

    if check_name:
        if not is_valid_username(user_in.name):
            return False, "invalid username"

    if check_password:
        is_valid_password = is_strong_password(user_in.password)
        if not is_valid_password[0]:
            return is_valid_password
    return True, ""


def success_login_user(
        user_id
) -> JSONResponse:
    refresh_token = create_refresh_token(user_id)
    access_token = create_access_token(user_id)
    response = JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer",
    })
    set_refresh_token_cookie(response, refresh_token)
    return response
