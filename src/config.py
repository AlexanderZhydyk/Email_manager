from pydantic import BaseSettings, Field


class Config(BaseSettings):
    IMAP_SERVER: str = Field(..., env='IMAP_SERVER')
    IMAP_PORT: int = Field(..., env='IMAP_PORT')
    SMTP_SERVER: str = Field(..., env='SMTP_SERVER')
    SMTP_PORT: int = Field(..., env='SMTP_PORT')
    OPENAI_KEY: str = Field(..., env='OPENAI_KEY')

    class Config:
        case_sensitive = True
        env_file = '../.env'
        env_file_encoding = 'utf-8'


conf = Config()
