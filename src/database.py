#Импортируем все необходимое
import asyncio
import src.queries.core as core

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text
from src.config import settings

#Подключение к БД(синхронный вариант)
#url - адрес БД
#echo - debug
#pool_size - max кол-во соединений (5 по ум.)
#max_overflow - количество подключений для "превышения" лимита (10 по ум.)
sync_engine = create_engine(
    url = settings.DATABASE_URL_psycopg,
    echo = True, 
    pool_size = 5,
    max_overflow = 10
)

#Подключение к БД(aсинхронный вариант)
async_engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo = False, 
    pool_size = 5,
    max_overflow = 10
)

session_factory = sessionmaker(sync_engine)
async_session_factorysession_factory = async_sessionmaker(async_engine)

#Если без sessionmaker
# with Session(sync_engine, autoflush и т.д.) as session:
#     session... (вып. запроса)

#С sessionmaker
# session = sessionmaker(sync_engine)
# with session() as session:
#     session...


class Base(DeclarativeBase):
    pass