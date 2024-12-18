from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import ProductCreate, ProductSchema, ClientSchema
from project.core.exceptions import ProductNotFound, ProductAlreadyExists
from project.api.depends import database, product_repo, check_for_admin_access, get_current_client

product_router = APIRouter()



@product_router.get(
    "/all_products",
    response_model=list[ProductSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_all_products() -> list[ProductSchema]:
    async with database.session() as session:
        all_products = await product_repo.get_all_products(session=session)

    return all_products


@product_router.get(
    "/product/{product_id}",
    response_model=ProductSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_product_by_id(
    product_id: int,
) -> ProductSchema:
    try:
        async with database.session() as session:
            product = await product_repo.get_product_by_id(session=session, product_id=product_id)
    except ProductNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return product


@product_router.post("/add_product", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def add_product(
    product_dto: ProductCreate,
current_client: ClientSchema = Depends(get_current_client),
) -> ProductSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            new_product = await product_repo.create_product(session=session, product=product_dto)
    except ProductAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_product


@product_router.put(
    "/update_product/{product_id}",
    response_model=ProductSchema,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product_id: int,
    product_dto: ProductCreate,
current_client: ClientSchema = Depends(get_current_client),
) -> ProductSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            updated_product = await product_repo.update_product(
                session=session,
                product_id=product_id,
                product=product_dto,
            )
    except ProductNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_product


@product_router.delete("/delete_product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
current_client: ClientSchema = Depends(get_current_client),
) -> None:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            product = await product_repo.delete_product(session=session, product_id=product_id)
    except ProductNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return product
