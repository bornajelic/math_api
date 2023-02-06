import logging

import aioredis
from aioredis.exceptions import ConnectionError, RedisError, ResponseError


class RedisCache:
    """Creates async connection pooling to maintain the connection from FastAPI to Redis and
    reduce open-closing connection costs.
    Redis clients and connections have implemented __del__ methods,
    so will attempt to automatically clean up any open connections when garbage-collected.
    """

    def __init__(self) -> str:
        self.redis_cache = None

    async def create_connection(self, redis_url):
        try:
            self.redis_cache = await aioredis.from_url(redis_url)
        except (ConnectionError, RedisError) as conn_err:
            logging.error(conn_err)
            raise

    async def get_item(self, key) -> float:
        try:
            result = await self.redis_cache.get(key)
            return result
        except (ResponseError, RedisError) as redis_err:
            logging.error(redis_err)
            raise

    async def setex_item(self, key, value, timedelta) -> None:
        try:
            await self.redis_cache.setex(key, timedelta, value)
        except (ResponseError, RedisError) as redis_err:
            logging.error(redis_err)
            raise

    async def health(self):
        return await self.redis_cache.ping()


redis_cache = RedisCache()
