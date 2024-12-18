from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import DrinkSchema, DrinkCreate, ClientSchema
from project.core.exceptions import DrinkNotFound, DrinkAlreadyExists
from project.api.depends import database, drink_repo, check_for_admin_access, get_current_client


drink_router = APIRouter()



@drink_router.get("/all_drinks", response_model=list[DrinkSchema], status_code=status.HTTP_200_OK)
async def get_all_drinks() -> list[DrinkSchema]:
    async with database.session() as session:
        all_drinks = await drink_repo.get_all_drinks(session=session)
    return all_drinks


@drink_router.get(
    "/drink/{drink_id}",
    response_model=DrinkSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_drink_by_id(
    drink_id: int,
) -> DrinkSchema:
    try:
        async with database.session() as session:
            drink = await drink_repo.get_drink_by_id(session=session, drink_id=drink_id)
    except DrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return drink


@drink_router.post("/add_drink", response_model=DrinkSchema, status_code=status.HTTP_201_CREATED)
async def add_drink(
    drink_dto: DrinkCreate,
    current_client: ClientSchema = Depends(get_current_client),
) -> DrinkSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            new_drink = await drink_repo.create_drink(session=session, drink=drink_dto)
            await session.commit()
    except DrinkAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_drink


@drink_router.put(
    "/update_drink/{drink_id}",
    response_model=DrinkSchema,
    status_code=status.HTTP_200_OK,
)
async def update_drink(
    drink_id: int,
    drink_dto: DrinkCreate,
    current_client: ClientSchema = Depends(get_current_client),
) -> DrinkSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            updated_drink = await drink_repo.update_drink(
                session=session,
                drink_id=drink_id,
                drink=drink_dto,
            )
            await session.commit()
    except DrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_drink


@drink_router.delete("/delete_drink/{drink_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drink(
    drink_id: int,
    current_client: ClientSchema = Depends(get_current_client),
) -> None:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            await drink_repo.delete_drink(session=session, drink_id=drink_id)
            await session.commit()
    except DrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
