from app.repositories.users import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.db.models import User

class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def register(self, email: str, password: str) -> User:
        existing_user = await self._user_repo.get_by_email(email)
        if existing_user:
            raise ConflictError("Пользователь с таким email уже существует")

        hashed_password = get_password_hash(password)

        return await self._user_repo.create(email=email, password_hash=hashed_password)

    async def login(self, email: str, password: str) -> str:
        user = await self._user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError("Неверный email или пароль")

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Неверный email или пароль")

        token = create_access_token(subject=user.id, role=user.role)
        return token

    async def get_profile(self, user_id: int) -> User:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")
        return user
