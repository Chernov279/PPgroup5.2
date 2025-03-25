# import pytest
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.main import app
#
#
# @pytest.fixture
# async def test_db_session() -> AsyncSession:
#     """Создает сессию для тестов"""
#     async with TestSessionLocal() as session:
#         yield session
#
#
# @pytest.fixture
# async def async_client():
#     """Фикстура для HTTP клиента"""
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         yield client
#
#
# @pytest.mark.asyncio
# async def test_get_all_users(async_client):
#     response = await async_client.get("/users/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)  # Проверяем, что возвращается список
#
#
# @pytest.mark.asyncio
# async def test_get_user_me(async_client):
#     response = await async_client.get("/users/me", headers={"Authorization": "Bearer testtoken"})
#     assert response.status_code in [200, 401]  # Если нет токена - 401, иначе 200
#
#
# @pytest.mark.asyncio
# async def test_get_user_by_id(async_client):
#     response = await async_client.get("/users/1")  # Проверяем, что юзер с id=1 существует
#     assert response.status_code in [200, 404]  # Если юзер есть - 200, иначе - 404
#
#
# @pytest.mark.asyncio
# async def test_update_user(async_client):
#     update_data = {"name": "Updated Name"}
#     response = await async_client.put("/users/", json=update_data)
#     assert response.status_code in [200, 404]  # Если юзер есть - 200, иначе - 404
#
#
# @pytest.mark.asyncio
# async def test_delete_user(async_client):
#     response = await async_client.delete("/users/")
#     assert response.status_code in [200, 404]  # Если юзер есть - 200, иначе - 404