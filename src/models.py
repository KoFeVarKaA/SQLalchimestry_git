#Сейссии нужны для транзакций. Входим = открываем; Делаем набор запросов; Либо commit, либо rollback
from sqlalchemy.orm import Session, sessionmaker, Mapped, mapped_column
from sqlalchemy import Table, Column, Integer, String, MetaData
#Вариант через питонячие запросы - имеративный стиль (иначе - декларативный)

from src.database import sync_engine, Base

#В metadata_obj будут храниться данные о всех таблицах, созданных на стороне приложения
#Будем передовать ее во все таблицы и модели (потом и для миграций используем)
metadata_obj = MetaData()

# #Таблица с работниками(императивный вариант)
# workers_table = Table(
#     "workers",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("username", String)
# )

#Таблица с работниками(декларативный вариант)
class WorkersOrm(Base):
    __tablename__ = "workers"


    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str]