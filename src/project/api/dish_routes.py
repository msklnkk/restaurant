from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import DishCreate, DishSchema, ClientSchema
from project.core.exceptions import DishNotFound, DishAlreadyExists
from project.api.depends import database, dish_repo, check_for_admin_access, get_current_client

dish_router = APIRouter()


@dish_router.get("/all_dishes", response_model=list[DishSchema], status_code=status.HTTP_200_OK)
async def get_all_dishes() -> list[DishSchema]:
    async with database.session() as session:
        all_dishes = await dish_repo.get_all_dishes(session=session)
        await session.commit()
    return all_dishes


@dish_router.get(
    "/dish/{dish_id}",
    response_model=DishSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_dish_by_id(
    dish_id: int,
) -> DishSchema:
    try:
        async with database.session() as session:
            dish = await dish_repo.get_dish_by_id(session=session, dish_id=dish_id)
            await session.commit()
    except DishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return dish


@dish_router.get("/dishes/type/{dish_type}", response_model=list[DishSchema], status_code=status.HTTP_200_OK)
async def get_dishes_by_type(
    dish_type: str,
) -> list[DishSchema]:
    async with database.session() as session:
        dishes = await dish_repo.get_dishes_by_type(session=session, dish_type=dish_type)
        await session.commit()
    return dishes


@dish_router.get("/dishes/search", response_model=list[DishSchema], status_code=status.HTTP_200_OK)
async def search_dishes_by_name(
    name: str,
) -> list[DishSchema]:
    async with database.session() as session:
        dishes = await dish_repo.search_dishes_by_name(session=session, name=name)
        await session.commit()
    return dishes


@dish_router.post("/add_dish", response_model=DishSchema, status_code=status.HTTP_201_CREATED)
async def add_dish(
    dish_dto: DishCreate,
    current_client: ClientSchema = Depends(get_current_client),
) -> DishSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            new_dish = await dish_repo.create_dish(session=session, dish=dish_dto)
            await session.commit()
    except DishAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_dish


@dish_router.put(
    "/update_dish/{dish_id}",
    response_model=DishSchema,
    status_code=status.HTTP_200_OK,
)
async def update_dish(
    dish_id: int,
    dish_dto: DishCreate,
    current_client: ClientSchema = Depends(get_current_client),
) -> DishSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            updated_dish = await dish_repo.update_dish(
                session=session,
                dish_id=dish_id,
                dish=dish_dto,
            )
            await session.commit()
    except DishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_dish


@dish_router.delete("/delete_dish/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(
    dish_id: int,
    current_client: ClientSchema = Depends(get_current_client),
) -> None:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            await dish_repo.delete_dish(session=session, dish_id=dish_id)
            await session.commit()
    except DishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
