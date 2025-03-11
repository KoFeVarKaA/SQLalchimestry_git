import asyncio
from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import String, create_engine, text
from src.config import settings

#Подключение к БД(синхронный вариант)
#url - адрес БД
#echo - debug
#pool_size - max кол-во соединений (5 по ум.)
#max_overflow - количество подключений для "превышения" лимита (10 по ум.)
sync_engine = create_engine(
    url = settings.DATABASE_URL_psycopg,
    echo = False, 
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
async_session_factory = async_sessionmaker(async_engine)

#Если без sessionmaker
# with Session(sync_engine, autoflush и т.д.) as session:
#     session... (вып. запроса)

#С sessionmaker
# session = sessionmaker(sync_engine)
# with session() as session:
#     session...

# Пример запроса (СЫРОЙ - быстро, но не удобно)
def get_123_sync():
    with sync_engine.connect() as conn:
        res = conn.execute(text("select 1, 2, 3 union select 4, 5, 6"))
        print(f"{res=}")
        # Чтобы получить данные из объекта есть ряд методов
        # all - все данные
        # first - получит все, но вернет первую 
        print(f"{res.all()=}")
        conn.commit()

# То же самое, но асинхронно
async def get_123_async():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("select 1, 2, 3 union select 4, 5, 6"))
        print(f"{res.all()=}")
        await conn.commit()

# Вызывать асинхронную функци. только так:
# asyncio.run(get_123())

str_256 = Annotated[str, 256]
# Хз зач, но нужен type_annotation_map
class Base(DeclarativeBase):
    type_annotation_map = {
        str_256 : String(256)
    }

    # Переопределение способа вывода
    # repr_cols_num и repr_cols можно менять в наследующем классе
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            # Если выводить только первые 3 колонки
            # if col in self.repr_cols or idx < self.repr_cols_num:
            cols.append(f"{col}={getattr(self, col)}")

        return f"\n<{self.__class__.__name__} {', '.join(cols)}>"