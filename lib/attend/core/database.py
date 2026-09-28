import aiomysql
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv(".local.properties", override=True)

DB_CONFIG = {
    "host": os.getenv("HOST", "localhost"),
    "user": os.getenv("USER", "root"),
    "password": os.getenv("PASSWORD", ""),
    "db": os.getenv("DATABASE", "attendance_db"),
    "port": int(os.getenv("PORT", 3306)),
    "autocommit": os.getenv("AUTOCOMMIT", "True").lower() == "true",
}
print("user is",DB_CONFIG['user'])

# Create a connection pool on application startup or demand
_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await aiomysql.create_pool(**DB_CONFIG)
    return _pool

async def get_db_cursor() -> AsyncGenerator:
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            yield cursor