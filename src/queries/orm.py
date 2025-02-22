from sqlalchemy import insert, text
from src.database import async_engine, sync_engine, session_factory, async_session_factory
from src.models import metadata_obj, Workers

#Создаем все таблицы через встроенный в метаданные метод - create_all(<название движка>)
def create_tables():
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True

def insert_data():
    worker_bobr = Workers(username='bobr')
    worker_volk = Workers(username='Volk')
    with session_factory() as session:
        #По факту мы добавляем огромное кол-во данных в сейссию,
        #А сейсия за нас определяет порядок внесения данных в бд и прописывает команды
        session.add_all([worker_bobr, worker_volk])
        session.commit()