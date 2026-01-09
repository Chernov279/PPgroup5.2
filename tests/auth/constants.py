REGISTER_PATH = "/auth/register"
LOGIN_PATH = "/auth/login"
OAUTH2_PATH = "/auth/oauth2"
REFRESH_PATH = "/auth/refresh"
LOGOUT_PATH = "/auth/logout"
LOGOUT_ALL_PATH = "/auth/logout-all"

VALID_REGISTER_USER = {
    "email": "valid@example.com",
    "password": "Password123!",
    "name": "ValidUser",
}

SAME_EMAIL_VALID_REGISTER_USER = {
    "email": "valid@example.com",
    "password": "SOMething987!",
    "name": "Good_guy19",
}

INVALID_EMAIL_REGISTER_USER = {
    "email": "not-an-email@.",
    "password": "Password123!",
    "name": "Test_User",
}

WEAK_PASSWORD_REGISTER_USER = {
    "email": "weakpass@example.com",
    "password": "weak",
    "name": "Test_User",
}

OPTIONAL_FIELDS_VALID_REGISTER_USER = {
    "email": "fulluser@example.com",
    "password": "Password123!",
    "name": "Test",
    "surname": "User",
    "patronymic": "Patronymic",
}

VALID_LOGIN_USER = {
    "email": "valid@example.com",
    "password": "Password123!",
}

WRONG_PASSWORD_LOGIN_USER = {
    "email": "valid@example.com",
    "password": "WrongPassword123!",
}

VALID_LOGIN_OATH2_USER = {
    "username": "valid@example.com",
    "password": "Password123!",
}

REFRESH_TOKEN_KEY = "refresh_token"
REFRESH_TOKEN_SCHEMA = {
    REFRESH_TOKEN_KEY: None
}

INVALID_REFRESH_USER = {
    REFRESH_TOKEN_KEY: "invalid_token"
}