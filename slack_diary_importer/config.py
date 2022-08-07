from pydantic import BaseSettings


class Settings(BaseSettings):
    slack_bot_token: str
    slack_channel: str
    hatena_oauth_consumer_key: str
    hatena_oauth_consumer_secret: str
    hatena_oauth_token: str = ""
    hatena_oauth_token_secret: str = ""
    hatena_id: str
    hatena_blog_id: str

    class Config:
        env_file = ".env"


settings = Settings()
