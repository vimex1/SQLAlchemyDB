import asyncio
from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import String, create_engine
from config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    # pool_size=5,
    # max_overflow=10,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)



str_256 = Annotated[str, 256]   # создаем тип аннотацию str_256, она будет заменяться на sqlalchemy.String(256)

# создаем базовый класс для моделей, он будет наследоваться от DeclarativeBase
class Base(DeclarativeBase):
    # создаем тип аннотацию, которая будет заменяться на sqlalchemy.String(256)
    type_annotation_map = {
        str_256: String(256)
    }
