from fastapi import APIRouter

from app.auth.views.token import AuthTokenView
from app.auth.views.v1.user_view import UserView

auth_router = APIRouter(
    prefix="",
    responses={404: {"description": "Not found"}},
)


auth_router.add_api_route("/auth-token", AuthTokenView.auth_token, methods=["POST"])
auth_router.add_api_route(
    "/refresh-token", AuthTokenView.refresh_token, methods=["POST"]
)

user_router = APIRouter(
    prefix="",
    responses={404: {"description": "Not found"}},
)
user_router.add_api_route("/me", UserView.me, methods=["GET"])
user_router.add_api_route("/users", UserView.create, methods=["POST"])
