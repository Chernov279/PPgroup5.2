from fastapi import APIRouter

auth = APIRouter(prefix="/auth", tags=["/auth", "/login"])

routes = [
    auth,
          ]