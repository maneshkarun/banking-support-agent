from fastapi import APIRouter, Depends

from app.schemas.auth import UserLoginRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def user_login(request: UserLoginRequest, service: Depends())