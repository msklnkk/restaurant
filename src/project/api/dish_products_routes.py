from fastapi import APIRouter, HTTPException, status

from project.schemas.user import DishProductsCreate, DishProductsSchema
from project.core.exceptions import DishProductNotFound, DishProductAlreadyExists
from project.api.depends import database, dishProducts_repo


dish_products_router = APIRouter()


@dish_products_router.get("/all_dish_products", response_model=list[DishProductsSchema], status_code=status.HTTP_200_OK)
async def get_all_dish_products() -> list[DishProductsSchema]:
    async with database.session() as session:
        all_dish_products = await dishProducts_repo.get_all_dish_products(session=session)
        await session.commit()
    return all_dish_products


@dish_products_router.get("/dish_product/{dish_id}/{product_id}", response_model=DishProductsSchema, status_code=status.HTTP_200_OK)
async def get_dish_product(
    dish_id: int,
    product_id: int,
) -> DishProductsSchema:
    try:
        async with database.session() as session:
            dish_product = await dishProducts_repo.get_dish_product(
                session=session,
                dish_id=dish_id,
                product_id=product_id
            )
            await session.commit()
    except DishProductNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return dish_product


@dish_products_router.get("/dish/{dish_id}/products", response_model=list[DishProductsSchema], status_code=status.HTTP_200_OK)
async def get_products_for_dish(
    dish_id: int,
) -> list[DishProductsSchema]:
    async with database.session() as session:
        products = await dishProducts_repo.get_products_for_dish(
            session=session,
            dish_id=dish_id
        )
        await session.commit()
    return products


@dish_products_router.post("/add_dish_product", response_model=DishProductsSchema, status_code=status.HTTP_201_CREATED)
async def add_dish_product(
    dish_product_dto: DishProductsCreate,
) -> DishProductsSchema:
    try:
        async with database.session() as session:
            new_dish_product = await dishProducts_repo.create_dish_product(
                session=session,
                dish_product=dish_product_dto
            )
            await session.commit()
    except DishProductAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_dish_product


@dish_products_router.put(
    "/update_dish_product/{dish_id}/{product_id}",
    response_model=DishProductsSchema,
    status_code=status.HTTP_200_OK,
)
async def update_dish_product(
    dish_id: int,
    product_id: int,
    dish_product_dto: DishProductsCreate,
) -> DishProductsSchema:
    try:
        async with database.session() as session:
            updated_dish_product = await dishProducts_repo.update_dish_product(
                session=session,
                dish_id=dish_id,
                product_id=product_id,
                dish_product=dish_product_dto,
            )
            await session.commit()
    except DishProductNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_dish_product


@dish_products_router.delete("/delete_dish_product/{dish_id}/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish_product(
    dish_id: int,
    product_id: int,
) -> None:
    try:
        async with database.session() as session:
            await dishProducts_repo.delete_dish_product(
                session=session,
                dish_id=dish_id,
                product_id=product_id
            )
            await session.commit()
    except DishProductNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@dish_products_router.delete("/dish/{dish_id}/products", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_products_for_dish(
    dish_id: int,
) -> None:
    async with database.session() as session:
        await dishProducts_repo.delete_all_products_for_dish(
            session=session,
            dish_id=dish_id
        )
        await session.commit()