from fastapi import APIRouter, HTTPException, status
from datetime import date
from decimal import Decimal

from project.schemas.user import ClientCreate, ClientSchema, DrinkSchema, DrinkCreate, PriceSchema, PriceCreate
from project.schemas.user import ProductCreate, ProductSchema, StaffCreate, StaffSchema, SupplierCreate, SupplierSchema
from project.schemas.user import TableCreate, TableSchema, DeliveryCreate, DeliverySchema, DishProductsCreate, DishProductsSchema
from project.schemas.user import DishCreate, DishSchema, OrderCreate, OrderSchema, ProductInDeliveryCreate, ProductInDeliverySchema
from project.schemas.user import ShelfLifeCreate, ShelfLifeSchema, OrderedDrinkCreate, OrderedDrinkSchema, OrderedDishCreate, OrderedDishSchema

from project.schemas.healthcheck import HealthCheckSchema

from project.core.exceptions import UserNotFound, UserAlreadyExists, DrinkNotFound, DrinkAlreadyExists, ProductNotFound, ProductAlreadyExists
from project.core.exceptions import StaffNotFound, StaffAlreadyExists, SupplierNotFound, SupplierAlreadyExists, OrderNotFound, OrderAlreadyExists
from project.core.exceptions import TableNotFound, TableAlreadyExists, DeliveryNotFound, DeliveryAlreadyExists
from project.core.exceptions import PriceNotFound, PriceAlreadyExists, DishProductNotFound, DishProductAlreadyExists, DishNotFound, DishAlreadyExists
from project.core.exceptions import ProductInDeliveryNotFound, ProductInDeliveryAlreadyExists, ShelfLifeNotFound, ShelfLifeAlreadyExists
from project.core.exceptions import OrderedDishNotFound, OrderedDishAlreadyExists, OrderedDrinkNotFound, OrderedDrinkAlreadyExists

from project.api.depends import database, user_repo, drink_repo, price_repo, product_repo, staff_repo, supplier_repo, table_repo
from project.api.depends import delivery_repo, dishProducts_repo, dish_repo, order_repo, productInDelivery_repo, shelfLife_repo
from project.api.depends import orderedDish_repo, orderedDrink_repo




router = APIRouter()


@router.get("/healthcheck", response_model=HealthCheckSchema, status_code=status.HTTP_200_OK)
async def check_health() -> HealthCheckSchema:
    async with database.session() as session:
        db_is_ok = await user_repo.check_connection(session=session)

    return HealthCheckSchema(
        db_is_ok=db_is_ok,
    )

# Client
@router.get("/all_users", response_model=list[ClientSchema], status_code=status.HTTP_200_OK)
async def get_all_users() -> list[ClientSchema]:
    async with database.session() as session:
        all_users = await user_repo.get_all_users(session=session)

    return all_users


@router.get("/user/{user_id}", response_model=ClientSchema, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int,
) -> ClientSchema:
    try:
        async with database.session() as session:
            user = await user_repo.get_user_by_id(session=session, user_id=user_id)
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return user


@router.post("/add_user", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
async def add_user(
    user_dto: ClientCreate,
) -> ClientSchema:
    try:
        async with database.session() as session:
            new_user = await user_repo.create_user(session=session, user=user_dto)
    except UserAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_user


@router.put(
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



# Drink
@router.get("/all_drinks", response_model=list[DrinkSchema], status_code=status.HTTP_200_OK)
async def get_all_drinks() -> list[DrinkSchema]:
    async with database.session() as session:
        all_drinks = await drink_repo.get_all_drinks(session=session)
    return all_drinks


@router.get("/drink/{drink_id}", response_model=DrinkSchema, status_code=status.HTTP_200_OK)
async def get_drink_by_id(
    drink_id: int,
) -> DrinkSchema:
    try:
        async with database.session() as session:
            drink = await drink_repo.get_drink_by_id(session=session, drink_id=drink_id)
    except DrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return drink


@router.post("/add_drink", response_model=DrinkSchema, status_code=status.HTTP_201_CREATED)
async def add_drink(
    drink_dto: DrinkCreate,
) -> DrinkSchema:
    try:
        async with database.session() as session:
            new_drink = await drink_repo.create_drink(session=session, drink=drink_dto)
            await session.commit()
    except DrinkAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_drink


@router.put(
    "/update_drink/{drink_id}",
    response_model=DrinkSchema,
    status_code=status.HTTP_200_OK,
)
async def update_drink(
    drink_id: int,
    drink_dto: DrinkCreate,
) -> DrinkSchema:
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


@router.delete("/delete_drink/{drink_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drink(
    drink_id: int,
) -> None:
    try:
        async with database.session() as session:
            await drink_repo.delete_drink(session=session, drink_id=drink_id)
            await session.commit()
    except DrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)



# Price
@router.get("/all_prices", response_model=list[PriceSchema], status_code=status.HTTP_200_OK)
async def get_all_prices() -> list[PriceSchema]:
    async with database.session() as session:
        all_prices = await price_repo.get_all_prices(session=session)
    return all_prices


@router.get("/price/{dish_id}", response_model=PriceSchema, status_code=status.HTTP_200_OK)
async def get_price_by_dish_id(
    dish_id: int,
) -> PriceSchema:
    try:
        async with database.session() as session:
            price = await price_repo.get_price_by_dish_id(session=session, dish_id=dish_id)
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return price


@router.post("/add_price/{dish_id}", response_model=PriceSchema, status_code=status.HTTP_201_CREATED)
async def add_price(
    dish_id: int,
    price_dto: PriceCreate,
) -> PriceSchema:
    try:
        async with database.session() as session:
            new_price = await price_repo.create_price(
                session=session,
                price=price_dto,
                dish_id=dish_id
            )
            await session.commit()
    except PriceAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_price


@router.put(
    "/update_price/{dish_id}",
    response_model=PriceSchema,
    status_code=status.HTTP_200_OK,
)
async def update_price(
    dish_id: int,
    price_dto: PriceCreate,
) -> PriceSchema:
    try:
        async with database.session() as session:
            updated_price = await price_repo.update_price(
                session=session,
                dish_id=dish_id,
                price=price_dto,
            )
            await session.commit()
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_price


@router.delete("/delete_price/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_price(
    dish_id: int,
) -> None:
    try:
        async with database.session() as session:
            await price_repo.delete_price(session=session, dish_id=dish_id)
            await session.commit()
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)



# Product

@router.get("/all_products", response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
async def get_all_products() -> list[ProductSchema]:
    async with database.session() as session:
        all_products = await product_repo.get_all_products(session=session)

    return all_products


@router.get("/product/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product_by_id(
    product_id: int,
) -> ProductSchema:
    try:
        async with database.session() as session:
            product = await product_repo.get_product_by_id(session=session, product_id=product_id)
    except ProductNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return product


@router.post("/add_product", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def add_product(
    product_dto: ProductCreate,
) -> ProductSchema:
    try:
        async with database.session() as session:
            new_product = await product_repo.create_product(session=session, product=product_dto)
    except ProductAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_product


@router.put(
    "/update_product/{product_id}",
    response_model=ProductSchema,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product_id: int,
    product_dto: ProductCreate,
) -> ProductSchema:
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


@router.delete("/delete_product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
) -> None:
    try:
        async with database.session() as session:
            product = await product_repo.delete_product(session=session, product_id=product_id)
    except ProductNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return product



# Staff

@router.get("/all_staff", response_model=list[StaffSchema], status_code=status.HTTP_200_OK)
async def get_all_staff() -> list[StaffSchema]:
    async with database.session() as session:
        all_staff = await staff_repo.get_all_staff(session=session)

    return all_staff


@router.get("/staff/{staff_id}", response_model=StaffSchema, status_code=status.HTTP_200_OK)
async def get_staff_by_id(
    staff_id: int,
) -> StaffSchema:
    try:
        async with database.session() as session:
            staff = await staff_repo.get_staff_by_id(session=session, staff_id=staff_id)
    except StaffNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return staff


@router.post("/add_staff", response_model=StaffSchema, status_code=status.HTTP_201_CREATED)
async def add_staff(
    staff_dto: StaffCreate,
) -> StaffSchema:
    try:
        async with database.session() as session:
            new_staff = await staff_repo.create_staff(session=session, staff=staff_dto)
    except StaffAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_staff


@router.put(
    "/update_staff/{staff_id}",
    response_model=StaffSchema,
    status_code=status.HTTP_200_OK,
)
async def update_staff(
    staff_id: int,
    staff_dto: StaffCreate,
) -> StaffSchema:
    try:
        async with database.session() as session:
            updated_staff = await staff_repo.update_staff(
                session=session,
                staff_id=staff_id,
                staff=staff_dto,
            )
    except StaffNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_staff


@router.delete("/delete_staff/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(
    staff_id: int,
) -> None:
    try:
        async with database.session() as session:
            staff = await staff_repo.delete_staff(session=session, staff_id=staff_id)
    except StaffNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return staff




# Supplier

@router.get("/all_suppliers", response_model=list[SupplierSchema], status_code=status.HTTP_200_OK)
async def get_all_suppliers() -> list[SupplierSchema]:
    async with database.session() as session:
        all_suppliers = await supplier_repo.get_all_suppliers(session=session)

    return all_suppliers


@router.get("/supplier/{supplier_id}", response_model=SupplierSchema, status_code=status.HTTP_200_OK)
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


@router.post("/add_supplier", response_model=SupplierSchema, status_code=status.HTTP_201_CREATED)
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


@router.put(
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


@router.delete("/delete_supplier/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
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



# Table

@router.get("/all_tables", response_model=list[TableSchema], status_code=status.HTTP_200_OK)
async def get_all_tables() -> list[TableSchema]:
    async with database.session() as session:
        all_tables = await table_repo.get_all_tables(session=session)

    return all_tables


@router.get("/table/{table_id}", response_model=TableSchema, status_code=status.HTTP_200_OK)
async def get_table_by_id(
    table_id: int,
) -> TableSchema:
    try:
        async with database.session() as session:
            table = await table_repo.get_table_by_id(session=session, table_id=table_id)
    except TableNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return table


@router.post("/add_table", response_model=TableSchema, status_code=status.HTTP_201_CREATED)
async def add_table(
    table_dto: TableCreate,
) -> TableSchema:
    try:
        async with database.session() as session:
            new_table = await table_repo.create_table(session=session, table=table_dto)
    except TableAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_table


@router.put(
    "/update_table/{table_id}",
    response_model=TableSchema,
    status_code=status.HTTP_200_OK,
)
async def update_table(
    table_id: int,
    table_dto: TableCreate,
) -> TableSchema:
    try:
        async with database.session() as session:
            updated_table = await table_repo.update_table(
                session=session,
                table_id=table_id,
                table=table_dto,
            )
    except TableNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_table


@router.delete("/delete_table/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    table_id: int,
) -> None:
    try:
        async with database.session() as session:
            table = await table_repo.delete_table(session=session, table_id=table_id)
    except TableNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return table



# Delivery

@router.get("/all_deliveries", response_model=list[DeliverySchema], status_code=status.HTTP_200_OK)
async def get_all_deliveries() -> list[DeliverySchema]:
    async with database.session() as session:
        all_deliveries = await delivery_repo.get_all_deliveries(session=session)

    return all_deliveries


@router.get("/delivery/{delivery_id}", response_model=DeliverySchema, status_code=status.HTTP_200_OK)
async def get_delivery_by_id(
    delivery_id: int,
) -> DeliverySchema:
    try:
        async with database.session() as session:
            delivery = await delivery_repo.get_delivery_by_id(
                session=session,
                delivery_id=delivery_id
            )
    except DeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return delivery


@router.get("/deliveries_by_date/{delivery_date}", response_model=list[DeliverySchema], status_code=status.HTTP_200_OK)
async def get_deliveries_by_date(
    delivery_date: date,
) -> list[DeliverySchema]:
    async with database.session() as session:
        deliveries = await delivery_repo.get_deliveries_by_date(
            session=session,
            delivery_date=delivery_date
        )

    return deliveries


@router.post("/add_delivery", response_model=DeliverySchema, status_code=status.HTTP_201_CREATED)
async def add_delivery(
    delivery_dto: DeliveryCreate,
) -> DeliverySchema:
    try:
        async with database.session() as session:
            new_delivery = await delivery_repo.create_delivery(
                session=session,
                delivery=delivery_dto
            )
    except DeliveryAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_delivery


@router.put(
    "/update_delivery/{delivery_id}",
    response_model=DeliverySchema,
    status_code=status.HTTP_200_OK,
)
async def update_delivery(
    delivery_id: int,
    delivery_dto: DeliveryCreate,
) -> DeliverySchema:
    try:
        async with database.session() as session:
            updated_delivery = await delivery_repo.update_delivery(
                session=session,
                delivery_id=delivery_id,
                delivery=delivery_dto,
            )
    except DeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_delivery


@router.delete("/delete_delivery/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_delivery(
    delivery_id: int,
) -> None:
    try:
        async with database.session() as session:
            delivery = await delivery_repo.delete_delivery(
                session=session,
                delivery_id=delivery_id
            )
    except DeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return delivery



# DishProducts

@router.get("/all_dish_products", response_model=list[DishProductsSchema], status_code=status.HTTP_200_OK)
async def get_all_dish_products() -> list[DishProductsSchema]:
    async with database.session() as session:
        all_dish_products = await dishProducts_repo.get_all_dish_products(session=session)
        await session.commit()
    return all_dish_products


@router.get("/dish_product/{dish_id}/{product_id}", response_model=DishProductsSchema, status_code=status.HTTP_200_OK)
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


@router.get("/dish/{dish_id}/products", response_model=list[DishProductsSchema], status_code=status.HTTP_200_OK)
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


@router.post("/add_dish_product", response_model=DishProductsSchema, status_code=status.HTTP_201_CREATED)
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


@router.put(
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


@router.delete("/delete_dish_product/{dish_id}/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.delete("/dish/{dish_id}/products", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_products_for_dish(
    dish_id: int,
) -> None:
    async with database.session() as session:
        await dishProducts_repo.delete_all_products_for_dish(
            session=session,
            dish_id=dish_id
        )
        await session.commit()


# Dish

@router.get("/all_dishes", response_model=list[DishSchema], status_code=status.HTTP_200_OK)
async def get_all_dishes() -> list[DishSchema]:
    async with database.session() as session:
        all_dishes = await dish_repo.get_all_dishes(session=session)
        await session.commit()
    return all_dishes


@router.get("/dish/{dish_id}", response_model=DishSchema, status_code=status.HTTP_200_OK)
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


@router.get("/dishes/type/{dish_type}", response_model=list[DishSchema], status_code=status.HTTP_200_OK)
async def get_dishes_by_type(
    dish_type: str,
) -> list[DishSchema]:
    async with database.session() as session:
        dishes = await dish_repo.get_dishes_by_type(session=session, dish_type=dish_type)
        await session.commit()
    return dishes


@router.get("/dishes/search", response_model=list[DishSchema], status_code=status.HTTP_200_OK)
async def search_dishes_by_name(
    name: str,
) -> list[DishSchema]:
    async with database.session() as session:
        dishes = await dish_repo.search_dishes_by_name(session=session, name=name)
        await session.commit()
    return dishes


@router.post("/add_dish", response_model=DishSchema, status_code=status.HTTP_201_CREATED)
async def add_dish(
    dish_dto: DishCreate,
) -> DishSchema:
    try:
        async with database.session() as session:
            new_dish = await dish_repo.create_dish(session=session, dish=dish_dto)
            await session.commit()
    except DishAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_dish


@router.put(
    "/update_dish/{dish_id}",
    response_model=DishSchema,
    status_code=status.HTTP_200_OK,
)
async def update_dish(
    dish_id: int,
    dish_dto: DishCreate,
) -> DishSchema:
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


@router.delete("/delete_dish/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(
    dish_id: int,
) -> None:
    try:
        async with database.session() as session:
            await dish_repo.delete_dish(session=session, dish_id=dish_id)
            await session.commit()
    except DishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


# Order
@router.get("/all_orders", response_model=list[OrderSchema], status_code=status.HTTP_200_OK)
async def get_all_orders() -> list[OrderSchema]:
    async with database.session() as session:
        all_orders = await order_repo.get_all_orders(session=session)

    return all_orders


@router.get("/order/{order_id}", response_model=OrderSchema, status_code=status.HTTP_200_OK)
async def get_order_by_id(
    order_id: int,
) -> OrderSchema:
    try:
        async with database.session() as session:
            order = await order_repo.get_order_by_id(session=session, order_id=order_id)
    except OrderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return order


@router.get("/orders/date/{order_date}", response_model=list[OrderSchema], status_code=status.HTTP_200_OK)
async def get_orders_by_date(
    order_date: date,
) -> list[OrderSchema]:
    async with database.session() as session:
        orders = await order_repo.get_orders_by_date(session=session, order_date=order_date)

    return orders


@router.get("/orders/status/{status}", response_model=list[OrderSchema], status_code=status.HTTP_200_OK)
async def get_orders_by_status(
    status: str,
) -> list[OrderSchema]:
    async with database.session() as session:
        orders = await order_repo.get_orders_by_status(session=session, status=status)

    return orders


@router.get("/orders/client/{client_id}", response_model=list[OrderSchema], status_code=status.HTTP_200_OK)
async def get_orders_by_client(
    client_id: int,
) -> list[OrderSchema]:
    async with database.session() as session:
        orders = await order_repo.get_orders_by_client(session=session, client_id=client_id)

    return orders


@router.get("/orders/staff/{staff_id}", response_model=list[OrderSchema], status_code=status.HTTP_200_OK)
async def get_orders_by_staff(
    staff_id: int,
) -> list[OrderSchema]:
    async with database.session() as session:
        orders = await order_repo.get_orders_by_staff(session=session, staff_id=staff_id)

    return orders


@router.post("/add_order", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
async def add_order(
    order_dto: OrderCreate,
) -> OrderSchema:
    try:
        async with database.session() as session:
            new_order = await order_repo.create_order(session=session, order=order_dto)
    except OrderAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_order


@router.put(
    "/update_order/{order_id}",
    response_model=OrderSchema,
    status_code=status.HTTP_200_OK,
)
async def update_order(
    order_id: int,
    order_dto: OrderCreate,
) -> OrderSchema:
    try:
        async with database.session() as session:
            updated_order = await order_repo.update_order(
                session=session,
                order_id=order_id,
                order=order_dto,
            )
    except OrderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_order


@router.patch(
    "/order/{order_id}/status",
    response_model=OrderSchema,
    status_code=status.HTTP_200_OK,
)
async def update_order_status(
    order_id: int,
    status: str,
) -> OrderSchema:
    try:
        async with database.session() as session:
            updated_order = await order_repo.update_order_status(
                session=session,
                order_id=order_id,
                status=status,
            )
    except OrderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_order


@router.delete("/delete_order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
) -> None:
    try:
        async with database.session() as session:
            await order_repo.delete_order(session=session, order_id=order_id)
    except OrderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)




# ProductInDelivery
@router.get("/all", response_model=list[ProductInDeliverySchema], status_code=status.HTTP_200_OK)
async def get_all_products_in_deliveries() -> list[ProductInDeliverySchema]:
    async with database.session() as session:
        all_products = await productInDelivery_repo.get_all_products_in_deliveries(session=session)

    return all_products


@router.get("/product/{product_id}/delivery/{delivery_id}", response_model=ProductInDeliverySchema, status_code=status.HTTP_200_OK)
async def get_product_in_delivery(
    product_id: int,
    delivery_id: int,
) -> ProductInDeliverySchema:
    try:
        async with database.session() as session:
            product = await productInDelivery_repo.get_product_in_delivery(
                session=session,
                product_id=product_id,
                delivery_id=delivery_id
            )
    except ProductInDeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return product


@router.get("/delivery/{delivery_id}", response_model=list[ProductInDeliverySchema], status_code=status.HTTP_200_OK)
async def get_products_by_delivery(
    delivery_id: int,
) -> list[ProductInDeliverySchema]:
    async with database.session() as session:
        products = await productInDelivery_repo.get_products_by_delivery(
            session=session,
            delivery_id=delivery_id
        )

    return products


@router.post("/add", response_model=ProductInDeliverySchema, status_code=status.HTTP_201_CREATED)
async def add_product_in_delivery(
    product_dto: ProductInDeliveryCreate,
) -> ProductInDeliverySchema:
    try:
        async with database.session() as session:
            new_product = await productInDelivery_repo.create_product_in_delivery(
                session=session,
                product=product_dto
            )
    except ProductInDeliveryAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_product


@router.put(
    "/update/product/{product_id}/delivery/{delivery_id}",
    response_model=ProductInDeliverySchema,
    status_code=status.HTTP_200_OK,
)
async def update_product_in_delivery(
    product_id: int,
    delivery_id: int,
    product_dto: ProductInDeliveryCreate,
) -> ProductInDeliverySchema:
    try:
        async with database.session() as session:
            updated_product = await productInDelivery_repo.update_product_in_delivery(
                session=session,
                product_id=product_id,
                delivery_id=delivery_id,
                product=product_dto,
            )
    except ProductInDeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_product


@router.delete("/delete/product/{product_id}/delivery/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_in_delivery(
    product_id: int,
    delivery_id: int,
) -> None:
    try:
        async with database.session() as session:
            await productInDelivery_repo.delete_product_in_delivery(
                session=session,
                product_id=product_id,
                delivery_id=delivery_id
            )
    except ProductInDeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@router.get("/delivery/{delivery_id}/total_cost", response_model=Decimal, status_code=status.HTTP_200_OK)
async def get_total_cost_by_delivery(
        delivery_id: int,
) -> Decimal:
    async with database.session() as session:
        total_cost = await productInDelivery_repo.get_total_cost_by_delivery(
            session=session,
            delivery_id=delivery_id
        )

    return total_cost


@router.delete("/delivery/{delivery_id}/delete_all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_products_in_delivery(
        delivery_id: int,
) -> None:
    async with database.session() as session:
        await productInDelivery_repo.delete_all_products_in_delivery(
            session=session,
            delivery_id=delivery_id
        )




# ShelfLife
@router.get("/all", response_model=list[ShelfLifeSchema], status_code=status.HTTP_200_OK)
async def get_all_shelf_lives() -> list[ShelfLifeSchema]:
    async with database.session() as session:
        all_shelf_lives = await shelfLife_repo.get_all_shelf_lives(session=session)

    return all_shelf_lives


@router.get("/shelf/{shelf_id}/delivery/{delivery_id}", response_model=ShelfLifeSchema, status_code=status.HTTP_200_OK)
async def get_shelf_life(
    shelf_id: int,
    delivery_id: int,
) -> ShelfLifeSchema:
    try:
        async with database.session() as session:
            shelf_life = await shelfLife_repo.get_shelf_life(
                session=session,
                shelf_id=shelf_id,
                delivery_id=delivery_id
            )
    except ShelfLifeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return shelf_life


@router.get("/delivery/{delivery_id}", response_model=list[ShelfLifeSchema], status_code=status.HTTP_200_OK)
async def get_shelf_lives_by_delivery(
    delivery_id: int,
) -> list[ShelfLifeSchema]:
    async with database.session() as session:
        shelf_lives = await shelfLife_repo.get_shelf_lives_by_delivery(
            session=session,
            delivery_id=delivery_id
        )

    return shelf_lives


@router.post("/add", response_model=ShelfLifeSchema, status_code=status.HTTP_201_CREATED)
async def add_shelf_life(
    shelf_life_dto: ShelfLifeCreate,
) -> ShelfLifeSchema:
    try:
        async with database.session() as session:
            new_shelf_life = await shelfLife_repo.create_shelf_life(
                session=session,
                shelf_life=shelf_life_dto
            )
    except ShelfLifeAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_shelf_life


@router.put(
    "/update/shelf/{shelf_id}/delivery/{delivery_id}",
    response_model=ShelfLifeSchema,
    status_code=status.HTTP_200_OK,
)
async def update_shelf_life(
    shelf_id: int,
    delivery_id: int,
    shelf_life_dto: ShelfLifeCreate,
) -> ShelfLifeSchema:
    try:
        async with database.session() as session:
            updated_shelf_life = await shelfLife_repo.update_shelf_life(
                session=session,
                shelf_id=shelf_id,
                delivery_id=delivery_id,
                shelf_life=shelf_life_dto,
            )
    except ShelfLifeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_shelf_life


@router.delete("/delete/shelf/{shelf_id}/delivery/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shelf_life(
    shelf_id: int,
    delivery_id: int,
) -> None:
    try:
        async with database.session() as session:
            await shelfLife_repo.delete_shelf_life(
                session=session,
                shelf_id=shelf_id,
                delivery_id=delivery_id
            )
    except ShelfLifeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@router.get("/expired", response_model=list[ShelfLifeSchema], status_code=status.HTTP_200_OK)
async def get_expired_shelf_lives(
        current_date: date | None = None
) -> list[ShelfLifeSchema]:
    async with database.session() as session:
        expired_items = await shelfLife_repo.get_expired_shelf_lives(
            session=session,
            current_date=current_date
        )

    return expired_items


@router.delete("/delivery/{delivery_id}/delete_all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shelf_lives_by_delivery(
        delivery_id: int,
) -> None:
    async with database.session() as session:
        await shelfLife_repo.delete_shelf_lives_by_delivery(
            session=session,
            delivery_id=delivery_id
        )



# OrderedDish
@router.get("/all", response_model=list[OrderedDishSchema], status_code=status.HTTP_200_OK)
async def get_all_ordered_dishes() -> list[OrderedDishSchema]:
    async with database.session() as session:
        all_ordered_dishes = await orderedDish_repo.get_all_ordered_dishes(session=session)

    return all_ordered_dishes


@router.get("/order/{order_id}/dish/{dish_id}", response_model=OrderedDishSchema, status_code=status.HTTP_200_OK)
async def get_ordered_dish(
    order_id: int,
    dish_id: int,
) -> OrderedDishSchema:
    try:
        async with database.session() as session:
            ordered_dish = await orderedDish_repo.get_ordered_dish(
                session=session,
                order_id=order_id,
                dish_id=dish_id
            )
    except OrderedDishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return ordered_dish


@router.get("/order/{order_id}", response_model=list[OrderedDishSchema], status_code=status.HTTP_200_OK)
async def get_dishes_by_order(
    order_id: int,
) -> list[OrderedDishSchema]:
    async with database.session() as session:
        ordered_dishes = await orderedDish_repo.get_dishes_by_order(
            session=session,
            order_id=order_id
        )

    return ordered_dishes


@router.post("/add", response_model=OrderedDishSchema, status_code=status.HTTP_201_CREATED)
async def add_ordered_dish(
    ordered_dish_dto: OrderedDishCreate,
) -> OrderedDishSchema:
    try:
        async with database.session() as session:
            new_ordered_dish = await orderedDish_repo.create_ordered_dish(
                session=session,
                ordered_dish=ordered_dish_dto
            )
    except OrderedDishAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_ordered_dish


@router.put(
    "/update/order/{order_id}/dish/{dish_id}",
    response_model=OrderedDishSchema,
    status_code=status.HTTP_200_OK,
)
async def update_ordered_dish(
    order_id: int,
    dish_id: int,
    ordered_dish_dto: OrderedDishCreate,
) -> OrderedDishSchema:
    try:
        async with database.session() as session:
            updated_ordered_dish = await orderedDish_repo.update_ordered_dish(
                session=session,
                order_id=order_id,
                dish_id=dish_id,
                ordered_dish=ordered_dish_dto,
            )
    except OrderedDishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_ordered_dish


@router.delete("/delete/order/{order_id}/dish/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ordered_dish(
    order_id: int,
    dish_id: int,
) -> None:
    try:
        async with database.session() as session:
            await orderedDish_repo.delete_ordered_dish(
                session=session,
                order_id=order_id,
                dish_id=dish_id
            )
    except OrderedDishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@router.put(
    "/update_count/order/{order_id}/dish/{dish_id}",
    response_model=OrderedDishSchema,
    status_code=status.HTTP_200_OK,
)
async def update_dish_count(
    order_id: int,
    dish_id: int,
    count: int,
) -> OrderedDishSchema:
    try:
        async with database.session() as session:
            updated_ordered_dish = await orderedDish_repo.update_dish_count(
                session=session,
                order_id=order_id,
                dish_id=dish_id,
                count=count
            )
    except OrderedDishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_ordered_dish


@router.delete("/order/{order_id}/delete_all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dishes_from_order(
    order_id: int,
) -> None:
    async with database.session() as session:
        await orderedDish_repo.delete_dishes_from_order(
            session=session,
            order_id=order_id
        )



# OrderedDrink

@router.get("/ordered_drinks", response_model=list[OrderedDrinkSchema], status_code=status.HTTP_200_OK)
async def get_all_ordered_drinks() -> list[OrderedDrinkSchema]:
    async with database.session() as session:
        ordered_drinks = await orderedDrink_repo.get_all_ordered_drinks(session=session)

    return ordered_drinks


@router.get("/ordered_drink/order/{order_id}/drink/{drink_id}", response_model=OrderedDrinkSchema,
            status_code=status.HTTP_200_OK)
async def get_ordered_drink(
        order_id: int,
        drink_id: int,
) -> OrderedDrinkSchema:
    try:
        async with database.session() as session:
            ordered_drink = await orderedDrink_repo.get_ordered_drink(
                session=session,
                order_id=order_id,
                drink_id=drink_id
            )
    except OrderedDrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return ordered_drink


@router.get("/ordered_drinks/order/{order_id}", response_model=list[OrderedDrinkSchema], status_code=status.HTTP_200_OK)
async def get_drinks_by_order(
        order_id: int,
) -> list[OrderedDrinkSchema]:
    async with database.session() as session:
        ordered_drinks = await orderedDrink_repo.get_drinks_by_order(
            session=session,
            order_id=order_id
        )

    return ordered_drinks


@router.post("/ordered_drink", response_model=OrderedDrinkSchema, status_code=status.HTTP_201_CREATED)
async def create_ordered_drink(
        ordered_drink_dto: OrderedDrinkCreate,
) -> OrderedDrinkSchema:
    try:
        async with database.session() as session:
            new_ordered_drink = await orderedDrink_repo.create_ordered_drink(
                session=session,
                ordered_drink=ordered_drink_dto
            )
    except OrderedDrinkAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_ordered_drink


@router.put(
    "/ordered_drink/order/{order_id}/drink/{drink_id}",
    response_model=OrderedDrinkSchema,
    status_code=status.HTTP_200_OK,
)
async def update_ordered_drink(
        order_id: int,
        drink_id: int,
        ordered_drink_dto: OrderedDrinkCreate,
) -> OrderedDrinkSchema:
    try:
        async with database.session() as session:
            updated_ordered_drink = await orderedDrink_repo.update_ordered_drink(
                session=session,
                order_id=order_id,
                drink_id=drink_id,
                ordered_drink=ordered_drink_dto
            )
    except OrderedDrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_ordered_drink


@router.delete("/ordered_drink/order/{order_id}/drink/{drink_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ordered_drink(
        order_id: int,
        drink_id: int,
) -> None:
    try:
        async with database.session() as session:
            await orderedDrink_repo.delete_ordered_drink(
                session=session,
                order_id=order_id,
                drink_id=drink_id
            )
    except OrderedDrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)



@router.put(
    "/ordered_drink/order/{order_id}/drink/{drink_id}/count",
    response_model=OrderedDrinkSchema,
    status_code=status.HTTP_200_OK,
)
async def update_drink_count(
    order_id: int,
    drink_id: int,
    count: int,
) -> OrderedDrinkSchema:
    try:
        async with database.session() as session:
            updated_ordered_drink = await orderedDrink_repo.update_drink_count(
                session=session,
                order_id=order_id,
                drink_id=drink_id,
                count=count
            )
    except OrderedDrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_ordered_drink


@router.delete("/ordered_drinks/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drinks_from_order(
    order_id: int,
) -> None:
    async with database.session() as session:
        await orderedDrink_repo.delete_drinks_from_order(
            session=session,
            order_id=order_id
        )
