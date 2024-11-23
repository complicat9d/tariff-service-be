import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from db.models import Base
from db.session import db_url
from config import settings


def test_check_db():
    if (
        settings.DATABASE_HOST not in ("localhost", "127.0.0.1", "db`")
        or "amazonaws" in settings.DATABASE_HOST
    ):
        print(db_url)
        raise Exception("Use local database only!")


@pytest.fixture
async def engine():
    test_check_db()

    e = create_async_engine(db_url, echo=False, max_overflow=25)

    try:
        async with e.begin() as con:
            await Base.metadata.create_all(con)

        yield e
    finally:
        async with e.begin() as con:
            Base.metadata.drop_all(con)
            # alembic_version should be dropped as well, as the next time we do alembic upgrade head
            # it won't do any changes
            await con.execute(text("DROP TABLE IF EXISTS alembic_version"))


@pytest.fixture
async def dbsession(engine) -> AsyncSession:
    with AsyncSession(bind=engine) as session, session.begin():
        yield session
