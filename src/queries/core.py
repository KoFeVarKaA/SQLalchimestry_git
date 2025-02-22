from sqlalchemy import insert, text
from database import async_engine, sync_engine
from src.models import metadata_obj, Workers
from src.database import session_factory


class SyncORM:
    @staticmethod
    #Создаем все таблицы через встроенный в метаданные метод - create_all(<название движка>)
    def create_tables():
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)

    @staticmethod
    def insert_workers():
        worker_1 = Workers( 
            title = "Python Junor Developer",
            compensation = 50000,
            workload = "fulltime",
            worker_id = 1,
        )
        worker_2 = Workers( 
            title = "Python Разработчик",
            compensation = 150000,
            workload = "fulltime",
            worker_id = 1,
        ) 
        worker_3 = Workers( 
            title = "Python Data Engineer",
            compensation = 250000,
            workload = "parttime",
            worker_id = 2,
        )
        worker_4 = Workers( 
            title = "Data Scientist",
            compensation = 300000,
            workload = "fulltime",
            worker_id = 2,
        )   
        with session_factory() as session:
            session.add_all([worker_1, worker_2, worker_3, worker_4])
            #flush - все изменения в session отправляет в бд не завершая транзакцию 
            #Пригождается для генерации id или для данных, которые ссылаются на что-то
            # session.flush()
            session.commit()

class OtherFunc:
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

    def insert_data():
        with sync_engine.connect() as conn:
            # Плохой способ(
            # stmt = """INSERT INTO workers (id, username)
            #         VALUES (1, 'BOSS'),
            #                (2, 'NOBOSS');"""
            # conn.execute(text(stmt))
            stmt = insert(workers_table).values(
                [
                    {"username":"Bobr"},
                    {"username":"Volk"},
                ]
            )
            conn.execute(stmt)
            conn.commit()