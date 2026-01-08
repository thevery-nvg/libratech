from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Run(BaseModel):
    port: int = 8000
    host: str = "0.0.0.0"


class Auth(BaseModel):
    secret_key: str = "the_first_rule_about_fight_club"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

class DBConfig(BaseModel):
    url: str =  'postgresql+asyncpg://aihunt_user:aihunt_password@localhost:5432/aihunt_db'
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 100
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="FASTAPI_CONFIG__",
    )

    run: Run = Run()
    auth: Auth = Auth()
    db: DBConfig = DBConfig()


settings = Settings()
