import datetime

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

import db.models as m
from schemas.exc import TariffNotFoundException, TariffAlreadyExistsException
from schemas.tariff import (
    TariffCreateSchema,
    TariffUpdateSchema,
    TariffSchema,
    TariffDeleteSchema,
)


async def get_tariffs(session: AsyncSession, page: int, per_page: int):
    q = sa.select(m.Tariff.__table__).offset(page * per_page).limit(per_page)
    entities = (await session.execute(q)).mappings().all()

    if entities:
        return [TariffSchema(**entity) for entity in entities]


async def get_tariff(session: AsyncSession, date: datetime.date, cargo_type: str):
    q = sa.select(m.Tariff.__table__).filter(
        sa.and_(m.Tariff.cargo_type == cargo_type, m.Tariff.date == date)
    )
    entity = (await session.execute(q)).mappings().first()

    if entity:
        return TariffSchema(**entity)


async def create_tariff(session: AsyncSession, request: TariffCreateSchema):
    q = sa.select(m.Tariff.cargo_type).filter(
        sa.and_(
            m.Tariff.cargo_type == request.cargo_type, m.Tariff.date == request.date
        )
    )
    exists = (await session.execute(q)).scalar()

    if exists:
        raise TariffAlreadyExistsException

    q = sa.insert(m.Tariff).values(
        {
            m.Tariff.cargo_type: request.cargo_type,
            m.Tariff.date: request.date,
            m.Tariff.rate: request.rate,
        }
    )
    await session.execute(q)


async def update_tariff(session: AsyncSession, request: TariffUpdateSchema):
    q = sa.select(m.Tariff.cargo_type).filter(
        sa.and_(
            m.Tariff.cargo_type == request.cargo_type, m.Tariff.date == request.date
        )
    )

    exists = (await session.execute(q)).scalar_one_or_none()
    if not exists:
        raise TariffNotFoundException

    q = (
        sa.update(m.Tariff)
        .filter(
            sa.and_(
                m.Tariff.cargo_type == request.cargo_type, m.Tariff.date == request.date
            )
        )
        .values(rate=request.new_rate)
    )
    await session.execute(q)


async def delete_tariff(session: AsyncSession, request: TariffDeleteSchema):
    q = sa.select(m.Tariff.cargo_type).filter(
        sa.and_(
            m.Tariff.cargo_type == request.cargo_type, m.Tariff.date == request.date
        )
    )

    exists = (await session.execute(q)).scalar_one_or_none()
    if not exists:
        raise TariffNotFoundException

    q = sa.delete(m.Tariff).filter(
        sa.and_(
            m.Tariff.cargo_type == request.cargo_type, m.Tariff.date == request.date
        )
    )
    await session.execute(q)
