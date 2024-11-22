import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from typing import overload, Optional

import db.models as m
from utils.hash import hasher
from schemas.user import UserSchema, UserCreateSchema


async def create_user(request: UserCreateSchema, session: AsyncSession) -> int:
    q = (
        sa.insert(m.User)
        .values(
            {
                m.User.username: request.username,
                m.User.password: hasher.get_password_hash(request.password),
            }
        )
        .returning(m.User.id)
    )

    user_id = (await session.execute(q)).scalar()

    return user_id


@overload
async def get_user(user_id: int, session: AsyncSession) -> Optional[UserSchema]: ...


@overload
async def get_user(username: str, session: AsyncSession) -> Optional[UserSchema]: ...


async def get_user(
    session: AsyncSession, username: Optional[str] = None, user_id: Optional[int] = None
) -> Optional[UserSchema]:
    if user_id is not None:
        q = sa.select(m.User.__table__).where(m.User.id == user_id)
    elif username is not None:
        q = sa.select(m.User.__table__).where(m.User.username == username)
    else:
        return None

    entity = (await session.execute(q)).mappings().first()

    if entity:
        return UserSchema(**entity)
