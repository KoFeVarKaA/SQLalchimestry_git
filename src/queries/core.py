from sqlalchemy import insert, text
from database import async_engine, sync_engine
from src.models import metadata_obj, WorkersOrm

#Синхронный вариант выполнения команд
def get_123_sync():
    #Будем использовать контекстный менеджер, 
    #чтобы не париться с открытием и закрытием
    with sync_engine.connect() as conn:
        #Алхимия не принимает строки, ей нужен текст
        fect = conn.execute(text("SELECT 1,2,3 union SELECT 4,5,6"))
        #Чтобы получить данные из бд есть ряд методов
        #all() - все данные 
        #first() - первая строчка
        print(f"{fect.all()=}")

#Асинхронный вариант выполнения команд
async def get_123_async():
    async with async_engine.connect() as conn:
        fect = await conn.execute(text("SELECT 1,2,3 union SELECT 4,5,6"))
        print(f"{fect.all()=}")

#Создаем все таблицы через встроенный в метаданные метод - create_all(<название движка>)
def create_tables():
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True

# def insert_data():
#     with sync_engine.connect() as conn:
#         # Плохой способ(
#         # stmt = """INSERT INTO workers (id, username)
#         #         VALUES (1, 'BOSS'),
#         #                (2, 'NOBOSS');"""
#         # conn.execute(text(stmt))
#         stmt = insert(workers_table).values(
#             [
#                 {"username":"Bobr"},
#                 {"username":"Volk"},
#             ]
#         )
#         conn.execute(stmt)
#         conn.commit()