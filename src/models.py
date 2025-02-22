# Свои типы данных
import datetime
import enum
from typing import Annotated

#Сейссии нужны для транзакций. Входим = открываем; Делаем набор запросов; Либо commit, либо rollback
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text
#Вариант через питонячие запросы - имеративный стиль (иначе - декларативный)

from src.database import sync_engine, Base

#В metadata_obj будут храниться данные о всех таблицах, созданных на стороне приложения
#Будем передовать ее во все таблицы и модели (потом и для миграций используем)
metadata_obj = MetaData()

'''#Таблица с работниками(императивный вариант)
workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String)
)'''

# Свои типы данных
intpk = Annotated[int, mapped_column(primary_key=True)]
# Дата создания и удаления (обязательно указать server_default=func.now()/text("TIMEZONE('utc', now())")) utc - часовой пояс)
# onupdate=datetime.datetime.now - для orm
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=func.now(),
        onupdate=datetime.datetime.utcnow,
    )]


class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"

#Таблица с работниками(декларативный вариант)
class Workers(Base):
    __tablename__ = "workers"

    id : Mapped[intpk]
    username : Mapped[str]


class Resumes(Base):
    __tablename__ = "resumes"

    id : Mapped[intpk]
    # str с ограничением длины, создан в database
    title : Mapped[str]
    # Другие варианты (Либо число, либо ничего):
    # compensation : Mapped[int] = mapped_column(nullable=True)
    # compensation : Mapped[Optional [int]] 
    compensation : Mapped[int | None]
    # parttime/fulltime
    workload : Mapped[Workload]
    # Внешний ключ
    # Неоч вариант: worker_id : Mapped[int] = mapped_column(ForeignKey(Workers.id))
    # ondelete="CASCADE" - Если удаляем запись из одной БД за ней удаляется запись из связанных БД
    # Каскадное удаление работает только при удалении данных из workers
    # или "SET NULL" - обнулить данные (но должен быть int | None)
    worker_id : Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at : Mapped[created_at]
    updated_at : Mapped[updated_at]