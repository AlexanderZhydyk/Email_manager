from pydantic import BaseSettings, Field


class Config(BaseSettings):
    OPENAI_KEY: str = Field(..., env='OPENAI_KEY')

    class Config:
        case_sensitive = True
        env_file = '../.env'
        env_file_encoding = 'utf-8'


conf = Config()
