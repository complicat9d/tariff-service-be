import orjson as json
from typing import Optional, List
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from db.session import session_dep
from kafka.conf import kafka_client
from utils.db.tariff import (
    create_tariff,
    update_tariff,
    delete_tariff,
    get_tariff,
    get_tariffs,
)
from utils.auth import user_dep
from utils.log import logger
from schemas.exc import InvalidJSONException, TariffNotFoundException
from schemas.tariff import (
    TariffSchema,
    TariffDeleteSchema,
    TariffUpdateSchema,
    TariffCreateSchema,
    InsuranceCalculationSchema,
)

tariff_router = APIRouter(tags=["Tariff"])


@tariff_router.post("", response_model=TariffSchema)
async def _create_tariff(
    request: TariffCreateSchema, session: session_dep, user: user_dep
):
    try:
        await create_tariff(session, request)
    except IntegrityError:
        logger.warning(
            "Tariff entity with date {} and cargo_type {} was not created, as it is already in the db".format(
                request.date, request.cargo_type
            )
        )
    await kafka_client.send_log(
        user_id=user.id,
        action=f"create_tariff",
        cargo_type=request.cargo_type,
        date=request.date,
    )
    return await get_tariff(session, request.date, request.cargo_type)


@tariff_router.put("", response_model=TariffSchema)
async def _update_tariff(
    request: TariffUpdateSchema, session: session_dep, user: user_dep
):
    await update_tariff(session, request)
    await kafka_client.send_log(
        user_id=user.id,
        action=f"update_tariff",
        cargo_type=request.cargo_type,
        date=request.date,
    )
    return await get_tariff(session, request.date, request.cargo_type)


@tariff_router.delete("", status_code=status.HTTP_200_OK)
async def _delete_tariff(
    request: TariffDeleteSchema, session: session_dep, user: user_dep
):
    await delete_tariff(session, request)
    await kafka_client.send_log(
        user_id=user.id,
        action=f"delete_tariff",
        cargo_type=request.cargo_type,
        date=request.date,
    )


@tariff_router.post("/calculate", status_code=status.HTTP_200_OK)
async def calculate(
    request: InsuranceCalculationSchema, session: session_dep, user: user_dep
):
    tariff = await get_tariff(session, request.date, request.cargo_type)
    if tariff:
        await kafka_client.send_log(
            user_id=user.id,
            action=f"calc_cost",
            cargo_type=request.cargo_type,
            date=request.date,
        )
        return JSONResponse({"insurance_cost": (request.value * tariff.rate)})
    else:
        raise TariffNotFoundException


@tariff_router.get("", response_model=Optional[List[TariffSchema]])
async def get_all_tariffs(
    session: session_dep, user: user_dep, page: int = 0, per_page: int = 10
):
    await kafka_client.send_log(user_id=user.id, action=f"get_tariffs")
    return await get_tariffs(session, page, per_page)


@tariff_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_tariffs(
    session: session_dep, user: user_dep, file: UploadFile = File(...)
):
    contents = await file.read()

    try:
        data = json.loads(contents)
        for date, info in data.items():
            request = TariffSchema(date=date, **info)
            try:
                await create_tariff(session, request)
            except IntegrityError:
                logger.warning(
                    "Tariff entity with date {} and cargo_type {} was not created, as it is already in the db".format(
                        request.date, request.cargo_type
                    )
                )
            await kafka_client.send_log(
                user_id=user.id,
                action=f"create_tariff",
                cargo_type=request.cargo_type,
                date=request.date,
            )

    except json.JSONDecodeError:
        raise InvalidJSONException
