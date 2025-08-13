from snowflake import SnowflakeGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config.settings import envs

_async_engine = create_async_engine(
    envs.DATABASE_URL,
    echo=envs.DATABASE_ECHO,
)

AsyncLocalSession = async_sessionmaker(
    _async_engine, autoflush=False, expire_on_commit=False
)


async def get_session():
    async with AsyncLocalSession() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


_snowflake_generator = SnowflakeGenerator(envs.INSTANCE_ID)


def generate_snowflake_id() -> int:
    return next(_snowflake_generator)
