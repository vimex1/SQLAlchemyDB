from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

























"""
Это файл конфигурации приложения, написанный на Python с использованием библиотеки Pydantic.

В этом файле определяется класс `Settings`, который наследуется от `BaseSettings` из Pydantic. Этот класс представляет собой набор настроек приложения, которые могут быть загружены из файла окружения (`.env`).

В классе `Settings` определены следующие атрибуты:

* `DB_HOST`: строка, содержащая имя хоста базы данных
* `DB_PORT`: целое число, содержащее порт базы данных
* `DB_USER`: строка, содержащая имя пользователя базы данных
* `DB_PASS`: строка, содержащая пароль пользователя базы данных
* `DB_NAME`: строка, содержащая имя базы данных

Также в классе определены два свойства:

* `DATABASE_URL_asyncpg`: возвращает строку подключения к базе данных в формате, совместимом с библиотекой asyncpg
* `DATABASE_URL_psycopg`: возвращает строку подключения к базе данных в формате, совместимом с библиотекой psycopg

В конце файла создается экземпляр класса `Settings` и присваивается переменной `settings`. Это позволяет использовать настройки приложения в других частях кода.

В целом, этот файл позволяет хранить настройки приложения в отдельном файле и загружать их в приложение в виде объекта Python.
"""
