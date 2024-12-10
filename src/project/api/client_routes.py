from fastapi import APIRouter, HTTPException, status

from project.schemas.user import ClientCreate, ClientSchema
from project.core.exceptions import UserNotFound, UserAlreadyExists
from project.api.depends import database, client_repo

client_router = APIRouter()


@client_router.get("/all_users", response_model=list[ClientSchema], status_code=status.HTTP_200_OK)
async def get_all_users() -> list[ClientSchema]:
    async with database.session() as session:
        all_users = await client_repo.get_all_users(session=session)

    return all_users


@client_router.get("/user/{user_id}", response_model=ClientSchema, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int,
) -> ClientSchema:
    try:
        async with database.session() as session:
            user = await client_repo.get_user_by_id(session=session, user_id=user_id)
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return user


@client_router.post("/add_user", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
async def add_user(
    user_dto: ClientCreate,
) -> ClientSchema:
    try:
        async with database.session() as session:
            new_user = await client_repo.create_user(session=session, user=user_dto)
    except UserAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_user


@client_router.put(
    "/update_user/{user_id}",
    response_model=ClientSchema,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    user_dto: ClientCreate,
) -> ClientSchema:
    try:
        async with database.session() as session:
            updated_user = await client_repo.update_user(
                session=session,
                user_id=user_id,
                user=user_dto,
            )
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_user


@client_router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
) -> None:
    try:
        async with database.session() as session:
            user = await client_repo.delete_user(session=session, user_id=user_id)
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return user