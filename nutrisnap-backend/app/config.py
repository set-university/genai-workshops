from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # AWS Bedrock (needed by future stories, define placeholder)
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"

    # Database
    database_url: str = "sqlite:///data/nutrisnap.db"


settings = Settings()
