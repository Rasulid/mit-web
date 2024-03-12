import getpass
import pathlib
import socket

from pydantic import EmailStr
from pydantic_settings import BaseSettings

if getpass.getuser() == "rasulabduvaitov":
    env_filename = ".env.dev"
elif socket.gethostname() == "pop-os":
    env_filename = ".env.dev"
else:
    env_filename = ".env.prod"

ENV_FILE_PATH = f"{pathlib.Path(__file__).parents[3]}/{env_filename}"

BASE_DIR = pathlib.Path(__file__).parents[1]
TEMPLATES_DIR = pathlib.Path(BASE_DIR, 'templates')
STATIC_DIR = pathlib.Path(BASE_DIR, 'static')


class Settings(BaseSettings):
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"
    API_V2_VERSION: str = "v2"
    API_V2_PREFIX: str = f"/api/{API_V2_VERSION}"
    SVC_PORT: int
    TIMEZONE: str = 'Asia/Tashkent'
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    OTP_CODE_VALID_SECONDS: int = 30000000
    SECRET_KEY: str
    ENCRYPT_KEY: str
    PROJECT_NAME: str
    # BACKEND_CORS_ORIGINS: List[HttpUrl] = []  # Assuming it's a list of URLs
    # Database
    DATABASE: str
    DATABASE_PORT: int
    DATABASE_PASSWORD: str
    DATABASE_USER: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    # JWT
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int = 60 * 24 * 10  # 10 days
    ACCESS_TOKEN_EXPIRES_IN: int = 60  # 60 minutes
    JWT_ALGORITHM: str
    # Test Database
    TEST_DATABASE: str = "test_db"

    class Config:
        env_file = ENV_FILE_PATH or ".env.dev"


def assemble_postgres_dsn(user: str, password: str, host: str, port: int, database: str) -> str:
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def assemble_postgres_dsn_test(user: str, password: str, host: str, port: int, database: str) -> str:
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


settings = Settings()
SYNC_DATABASE_URI = assemble_postgres_dsn(settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_HOST,
                                          settings.DATABASE_PORT, settings.DATABASE_NAME)

SYNC_TEST_DATABASE_URI = assemble_postgres_dsn_test(settings.DATABASE_USER, settings.DATABASE_PASSWORD,
                                                    settings.DATABASE_HOST,
                                                    settings.DATABASE_PORT, settings.TEST_DATABASE)
