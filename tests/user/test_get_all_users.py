import pytest
from httpx import AsyncClient
from typing import List

from tests.assertions import assert_status_code, assert_detail_has_key_word
from tests.user.constants import GET_ALL_PATH, INVALID_LIMIT, INVALID_OFFSET


@pytest.mark.asyncio
async def test_get_all_success(client: AsyncClient, create_user):
    """Проверяет успешный возврат всех пользователей из БД"""

    users: List[dict] = []
    for i in range(3):
        user = await create_user()
        users.append(user)

    response = await client.get(GET_ALL_PATH)
    assert_status_code(response, 200)

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

    user_ids = {user["id"] for user in data}
    for user in users:
        assert user["id"] in user_ids


@pytest.mark.asyncio
async def test_get_all_empty(client: AsyncClient):
    """Проверяет возврат пустого списка когда нет пользователей"""
    response = await client.get(GET_ALL_PATH)
    assert_status_code(response, 200)

    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_all_limit_success(client: AsyncClient, create_user):
    """Проверяет успешный возврат всех пользователей из БД с успешным применением лимита"""
    LIMIT = 2

    # Создаем больше пользователей, чем лимит
    for i in range(5):
        await create_user()

    response = await client.get(f"{GET_ALL_PATH}?limit={LIMIT}")
    assert_status_code(response, 200)

    data = response.json()
    assert len(data) == LIMIT


@pytest.mark.asyncio
async def test_get_all_offset_success(client: AsyncClient, create_user):
    """Проверяет успешный возврат всех пользователей из БД с успешным применением offset"""
    OFFSET = 1

    # Создаем пользователей и запоминаем их в правильном порядке
    created_users = []
    for i in range(3):
        user = await create_user()
        created_users.append(user)

    all_response = await client.get(GET_ALL_PATH)
    all_users = all_response.json()

    response = await client.get(f"{GET_ALL_PATH}?offset={OFFSET}")
    assert_status_code(response, 200)

    data = response.json()

    # Проверяем, что со смещением получаем подмножество
    assert len(data) == len(all_users) - OFFSET

    # Проверяем, что первый пользователь из all_users[OFFSET] равен data[0]
    if len(all_users) > OFFSET and len(data) > 0:
        assert all_users[OFFSET]["id"] == data[0]["id"]


@pytest.mark.asyncio
async def test_get_all_limit_and_offset_success(client: AsyncClient, create_user):
    """Проверяет комбинацию limit и offset"""
    LIMIT = 2
    OFFSET = 1

    for i in range(5):
        await create_user()

    response = await client.get(f"{GET_ALL_PATH}?limit={LIMIT}&offset={OFFSET}")
    assert_status_code(response, 200)

    data = response.json()
    assert len(data) == LIMIT


@pytest.mark.asyncio
async def test_get_all_invalid_limit(client: AsyncClient):
    """Проверяет валидацию неверного limit"""
    response = await client.get(f"{GET_ALL_PATH}?limit={INVALID_LIMIT}")
    assert_status_code(response, 422)
    assert_detail_has_key_word(response, "limit")


@pytest.mark.asyncio
async def test_get_all_invalid_offset(client: AsyncClient):
    """Проверяет валидацию неверного offset"""
    response = await client.get(f"{GET_ALL_PATH}?offset={INVALID_OFFSET}")
    assert_status_code(response, 422)
    assert_detail_has_key_word(response, "offset")


@pytest.mark.asyncio
async def test_get_all_negative_limit(client: AsyncClient):
    """Проверяет отрицательный limit"""
    response = await client.get(f"{GET_ALL_PATH}?limit=-1")
    assert_status_code(response, 422)


@pytest.mark.asyncio
async def test_get_all_negative_offset(client: AsyncClient):
    """Проверяет отрицательный offset"""
    response = await client.get(f"{GET_ALL_PATH}?offset=-1")
    assert_status_code(response, 422)


# @pytest.mark.asyncio
# async def test_get_all_with_order_by(client: AsyncClient, create_user):
#     """Проверяет сортировку пользователей"""
#     # Создаем пользователей с разными именами
#     await create_user(name="Charlie")
#     await create_user(name="Alice")
#     await create_user(name="Bob")
#
#     # Сортировка по имени по возрастанию
#     response = await client.get(f"{GET_ALL_PATH}?order_by=name&order=asc")
#     assert_status_code(response, 200)
#
#     data = response.json()
#     if len(data) >= 3:
#         # Проверяем порядок
#         names = [user["name"] for user in data[:3]]
#         assert names == sorted(names)
