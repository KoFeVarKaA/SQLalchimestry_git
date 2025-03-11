from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from src.database import Base, async_engine, async_session_factory, session_factory, sync_engine
from src.models import Resumes, Workers, Workload



class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_jack = Workers(username="Jack")
            worker_michael = Workers(username="Michael")
            session.add_all([worker_jack, worker_michael])
            # flush отправляет запрос в базу данных
            # После flush каждый из работников получает первичный ключ id, который отдала БД
            session.flush()
            session.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(Workers)
            result = session.execute(query)
            workers = result.scalars().all()
            # print(f"{workers=}")

    @staticmethod
    def update_worker(worker_id: int = 0, new_username: str = "Somebody"):
        with session_factory() as session:
            worker_michael = session.get(Workers, worker_id)
            worker_michael.username = new_username
            # refresh нужен, если мы хотим заново подгрузить данные модели из базы.
            # Подходит, если мы давно получили модель и в это время
            # данные в базе данныхмогли быть изменены
            session.refresh(worker_michael)
            session.commit()

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_jack_1 = Resumes(
                title="Python Junior Developer", compensation=50000, workload=Workload.fulltime, worker_id=1)
            resume_jack_2 = Resumes(
                title="Python Разработчик", compensation=150000, workload=Workload.fulltime, worker_id=1)
            resume_michael_1 = Resumes(
                title="Python Data Engineer", compensation=250000, workload=Workload.parttime, worker_id=2)
            resume_michael_2 = Resumes(
                title="Data Scientist", compensation=300000, workload=Workload.fulltime, worker_id=2)
            session.add_all([resume_jack_1, resume_jack_2, 
                             resume_michael_1, resume_michael_2])
            session.commit()

    @staticmethod
    def insert_additional_resumes():
        with session_factory() as session:
            workers = [
                {"username": "Artem"},  # id 3
                {"username": "Roman"},  # id 4
                {"username": "Petr"},   # id 5
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000, "workload": "fulltime", "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload": "parttime", "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000, "workload": "parttime", "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload": "fulltime", "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000, "workload": "fulltime", "worker_id": 5},
            ]
            insert_workers = insert(Workers).values(workers)
            insert_resumes = insert(Resumes).values(resumes)
            session.execute(insert_workers)
            session.execute(insert_resumes)
            session.commit()

    @staticmethod
    # Ленивая подгрузка - много запросов(неправильно)
    def select_workers_with_lazy_relationship():
        with session_factory() as session:
            query = (select (Workers))
            res = session.execute(query)
            # scalars т.к. будет кортеж и очень удобно его конвертировать к модели
            result = res.scalars().all()

            # Проблема n+1 - С каждым работником забирается его резюме
            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)

    @staticmethod
    # Без доп запросов - важно
    def select_workers_with_joined_relationship():
        with session_factory() as session:
            query = (
                select (Workers)
                # select... подходит только для many to many или one to many загрузки
                .options(joinedload(Workers.resumes))    
            )
            res = session.execute(query)
            # scalars т.к. будет кортеж и очень удобно его конвертировать к модели
            # unique - Чтобы не повторялись первичные ключи в join таблице 
            result = res.unique().scalars().all()

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)
        
    @staticmethod
    # Сначала подгружаем работников, а потом резюме для них (уникальное и к нему уникальное)   
    def select_workers_with_selectin_relationship():
        with session_factory() as session:
            query = (
                select (Workers)
                # selectin подходит только для many to many или one to many загрузки
                .options(selectinload(Workers.resumes))    
            )
            res = session.execute(query)

            result = res.unique().scalars().all()

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)
    
    @staticmethod
    def select_workers_with_condition_relationship():
        with session_factory() as session:
            query = (
                select(Workers)
                .options(selectinload(Workers.resumes_parttime))
            )

            res = session.execute(query)
            result = res.scalars().all()
            print(result)

    @staticmethod
    # contains_eager подтяни Workers.resumes, чтобы была вложенная структура, а не табличная
    def select_workers_with_condition_relationship_contains_eager():
        with session_factory() as session:
            query = (
                select(Workers)
                .join(Workers.resumes)
                .options(contains_eager(Workers.resumes))
                .filter(Resumes.workload == 'parttime')
            )

            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)