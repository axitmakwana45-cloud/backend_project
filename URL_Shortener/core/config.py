from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME : str
    APP_VERSION : str

    DB_HOST : str
    DB_PORT : str
    DB_USER : str
    DB_PASSWORD : str
    DB_NAME : str

    SECRET_KEY : str

    DEBUG : bool

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()