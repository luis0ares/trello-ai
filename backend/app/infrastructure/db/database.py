from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import get_config


_async_engine = create_async_engine(
    get_config().DATABASE_URL,
    echo=get_config().DATABASE_ECHO,
)

AsyncLocalSession = async_sessionmaker(
    _async_engine, autoflush=False, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_session():
    async with AsyncLocalSession() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
