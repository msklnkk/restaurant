from fastapi import APIRouter, HTTPException, status

from project.schemas.user import SupplierCreate, SupplierSchema
from project.core.exceptions import SupplierNotFound, SupplierAlreadyExists
from project.api.depends import database, supplier_repo

supplier_router = APIRouter()



@supplier_router.get("/all_suppliers", response_model=list[SupplierSchema], status_code=status.HTTP_200_OK)
async def get_all_suppliers() -> list[SupplierSchema]:
    async with database.session() as session:
        all_suppliers = await supplier_repo.get_all_suppliers(session=session)

    return all_suppliers


@supplier_router.get("/supplier/{supplier_id}", response_model=SupplierSchema, status_code=status.HTTP_200_OK)
async def get_supplier_by_id(
    supplier_id: int,
) -> SupplierSchema:
    try:
        async with database.session() as session:
            supplier = await supplier_repo.get_supplier_by_id(
                session=session,
                supplier_id=supplier_id
            )
    except SupplierNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return supplier


@supplier_router.post("/add_supplier", response_model=SupplierSchema, status_code=status.HTTP_201_CREATED)
async def add_supplier(
    supplier_dto: SupplierCreate,
) -> SupplierSchema:
    try:
        async with database.session() as session:
            new_supplier = await supplier_repo.create_supplier(
                session=session,
                supplier=supplier_dto
            )
    except SupplierAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_supplier


@supplier_router.put(
    "/update_supplier/{supplier_id}",
    response_model=SupplierSchema,
    status_code=status.HTTP_200_OK,
)
async def update_supplier(
    supplier_id: int,
    supplier_dto: SupplierCreate,
) -> SupplierSchema:
    try:
        async with database.session() as session:
            updated_supplier = await supplier_repo.update_supplier(
                session=session,
                supplier_id=supplier_id,
                supplier=supplier_dto,
            )
    except SupplierNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_supplier


@supplier_router.delete("/delete_supplier/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(
    supplier_id: int,
) -> None:
    try:
        async with database.session() as session:
            supplier = await supplier_repo.delete_supplier(
                session=session,
                supplier_id=supplier_id
            )
    except SupplierNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return supplier