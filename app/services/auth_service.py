from sqlalchemy.orm import Session

from app.schemas.auth import UserLoginRequest, UserLoginResponse

class AuthService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def login(self, payload; UserLoginRequest):
        