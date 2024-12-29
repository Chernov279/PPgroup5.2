from src.services.token_service import TokenService


def get_token_service() -> TokenService:
    return TokenService()
