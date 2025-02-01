from pydantic_settings import BaseSettings, SettingsConfigDict
#В данном файле мы забераем данные из ".env" и формируем ссылки для подключения к БД

class Settings(BaseSettings):
    DB_HOST:str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    #Асинхронный вариант с asycopg
    @property
    def DATABASE_URL_asyncpg(self):
    # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    #Синхронный вариант с psycopg
    @property
    def DATABASE_URL_psycopg(self):
    # Выглядит ссылка (DSN) след образом:
    # postgresql+psycopg://postgres:postgres@localhost:5432/sa
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()