from httpx import Response


def assert_status_code(response: Response, expected_code: int):
    actual_code = response.status_code
    assert actual_code == expected_code, \
    f'Ожидался статус код "{expected_code}", но получен {actual_code}. Тело ответа {response.text}'

def assert_json_has_key(response: Response, key: str):
    response_json = response.json()
    assert key in response_json, \
    f'Ключ "{key}" отсутствует в JSON - ответе'

def assert_detail_has_key_word(response: Response, key: str):
    response_detail = response.json().get("detail", None)
    assert response_detail is not None, \
    f'Ключ "detail" отсутствует в JSON - ответе'
    assert key in response_detail.lower(), \
    f'Ключ "{key}" отсутствует в JSON - ответе'