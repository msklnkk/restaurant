from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
from jose import jwt
from project.core.config import settings
from project.core.exceptions import UserNotFound
from project.schemas.auth import Token
from project.api.depends import database, client_repo
from project.resource.auth import verify_password
from project.schemas.user import ClientCreate, ClientSchema
from project.core.exceptions import UserAlreadyExists
from project.resource.auth import get_password_hash
import logging

auth_router = APIRouter()
logger = logging.getLogger(__name__)


@auth_router.post(
    "/register",
    response_model=ClientSchema,
    status_code=status.HTTP_201_CREATED,
    description="Регистрация нового клиента"
)
async def register_client(
        user_dto: ClientCreate,
) -> ClientSchema:
    """
    Регистрация нового клиента в системе.
    """
    logger.debug(f"Попытка регистрации нового клиента: {user_dto.mail}")
    try:
        async with database.session() as session:
            async with session.begin():
                # Устанавливаем значения по умолчанию для нового клиента
                user_dto.is_admin = False  # не админ
                user_dto.discount_percentage = 0  # начальная скидка 0%

                # Хешируем пароль перед сохранением
                user_dto.password = get_password_hash(password=user_dto.password)

                # Создаем нового пользователя
                new_user = await client_repo.create_user(
                    session=session,
                    user=user_dto
                )

                logger.info(f"Успешно зарегистрирован новый клиент с ID: {new_user.clientid}")
                return new_user

    except UserAlreadyExists as error:
        logger.warning(f"Попытка регистрации с существующей почтой: {user_dto.mail}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой почтой уже существует"
        )
    except Exception as e:
        logger.error(f"Неожиданная ошибка при регистрации: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера при регистрации"
        )


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    try:
        async with database.session() as session:
            user = await client_repo.get_user_by_mail(session=session, mail=form_data.username)
        if not verify_password(plain_password=form_data.password, hashed_password=user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": user.mail}
    to_encode = token_data.copy()
    if access_token_expires:
        expire = datetime.now(timezone.utc) + access_token_expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(
        claims=to_encode,
        key=settings.SECRET_AUTH_KEY.get_secret_value(),
        algorithm=settings.AUTH_ALGORITHM,
    )
    return Token(access_token=access_token, token_type="bearer")