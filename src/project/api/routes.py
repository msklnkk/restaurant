from fastapi import APIRouter, HTTPException, status

from project.schemas.user import ClientBase, ClientCreate, Client
from project.schemas.healthcheck import HealthCheckSchema
from project.core.exceptions import UserNotFound, UserAlreadyExists
from project.api.depends import database, user_repo


router = APIRouter()


@router.get("/healthcheck", response_model=HealthCheckSchema, status_code=status.HTTP_200_OK)
async def check_health() -> HealthCheckSchema:
    async with database.session() as session:
        db_is_ok = await user_repo.check_connection(session=session)

    return HealthCheckSchema(
        db_is_ok=db_is_ok,
    )


@router.get("/all_users", response_model=list[Client], status_code=status.HTTP_200_OK)
async def get_all_users() -> list[Client]:
    async with database.session() as session:
        all_users = await user_repo.get_all_users(session=session)

    return all_users


@router.get("/user/{user_id}", response_model=Client, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int,
) -> Client:
    try:
        async with database.session() as session:
            user = await user_repo.get_user_by_id(session=session, user_id=user_id)
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return user


@router.post("/add_user", response_model=Client, status_code=status.HTTP_201_CREATED)
async def add_user(
    user_dto: ClientCreate,
) -> Client:
    try:
        async with database.session() as session:
            new_user = await user_repo.create_user(session=session, user=user_dto)
    except UserAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_user


@router.put(
    "/update_user/{user_id}",
    response_model=Client,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    user_dto: ClientCreate,
) -> Client:
    try:
        async with database.session() as session:
            updated_user = await user_repo.update_user(
                session=session,
                user_id=user_id,
                user=user_dto,
            )
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_user


@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
) -> None:
    try:
        async with database.session() as session:
            user = await user_repo.delete_user(session=session, user_id=user_id)
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return user
