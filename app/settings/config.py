from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    mongodb_connection_uri: str = Field(...)
    mongodb_chat_database: str = Field(default="chat")
    mongodb_chat_collection: str = Field(default="chat_collection")

    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")
