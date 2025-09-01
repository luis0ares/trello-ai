import asyncio
import pytest_asyncio
from alembic import command
from alembic.config import Config
from pathlib import Path
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession)
from testcontainers.postgres import PostgresContainer
from httpx import AsyncClient, ASGITransport

from app.main import app as main_app
from app.infrastructure.db.database import get_session


alembic_cfg = Config(f'{Path().absolute()}/alembic.ini')


@pytest_asyncio.fixture(scope="session")
async def db_container():
    container = PostgresContainer('postgres:14', driver='asyncpg')
    container.start()
    yield container
    container.stop()


@pytest_asyncio.fixture(scope='session')
async def async_session_maker(db_container):
    db_url = db_container.get_connection_url().replace(
        "postgresql://", "postgresql+asyncpg://"
    )
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    async_engine = create_async_engine(db_url, echo=False, future=True)

    async_session_maker = async_sessionmaker(
        async_engine, autoflush=False, expire_on_commit=False
    )
    yield async_session_maker
    await async_engine.dispose()


@pytest_asyncio.fixture(scope='function')
async def db_session(async_session_maker):
    """
    AsyncSession factory bound to the test engine.
    """
    loop = asyncio.get_event_loop()

    async with async_session_maker() as session:
        try:
            # create the DB schema
            await loop.run_in_executor(
                None, lambda: command.upgrade(alembic_cfg, "head"))
            # wait for tests to finish
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            # drop the DB schema
            await loop.run_in_executor(
                None, lambda: command.downgrade(alembic_cfg, "base"))
            # close the session
            await session.close()


@pytest_asyncio.fixture(scope='function')
async def async_client(db_session: AsyncSession):
    """
    Async HTTP client for the FastAPI app, using the test DB session.
    """
    # Dependency override to inject the test session
    async def override_get_session():
        yield db_session

    main_app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=main_app)
    async with AsyncClient(transport=transport, base_url="http://test/api") as ac:
        yield ac

    main_app.dependency_overrides.clear()
