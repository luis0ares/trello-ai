
from functools import lru_cache
from snowflake import SnowflakeGenerator

from app.config.settings import envs


@lru_cache(maxsize=1)
def __snowflake_generator_factory(instance: int = envs.INSTANCE_ID):
    return SnowflakeGenerator(instance)


def generate_snowflake_id() -> int:
    snowflake_gen = __snowflake_generator_factory()
    return next(snowflake_gen)
