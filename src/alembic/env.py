# Здесь мы конфигурируем какие есть модели, бд, адрес, подключения и т.д.

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.config import settings
#Обязательно всегда импортировать все файлы с моделями (у меня все в одном )
from src.database import Base 
from src.models import Workers 

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

#Меняем опицию на адрес бд
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_psycopg)
#Сюда передаются все созданные нами таблицы
#Metadata - все данные о таблицах
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


#Создание миграций
# alembic init <Название>/<src/имя>(Если в папку)
#compare_server_default=True в connect добавить обязательно!

# alembic revision --autogenerate -m "комент"
# Где revision - миграция, 
# --autogenerate - сравнение состояний моделей в коде с состоянием Бд
# (далее можно задать какой-то коментарий) -m "комент"
# Для асинхроности еще в set_main_option + "?async_fallback=True"

#alembic upgrade head - накатить все миграции на бд


#Папка versions
#alembic upgrade head/<название миграции>нужна для добавления различных столбцов, таблиц, индексов и пр.
#alembic downgrade base/<название миграции> нужна для понижения версии бд, обычно связана с удалением теблиц, индексов
# Где head - моследняя миграция
# Base -  вообще все миграции 