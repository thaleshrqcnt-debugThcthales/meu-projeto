from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
import os


class Settings(BaseSettings):
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    ai_model: str = Field(default="claude-sonnet-4-6", env="AI_MODEL")
    ai_provider: str = Field(default="anthropic", env="AI_PROVIDER")

    app_host: str = Field(default="127.0.0.1", env="APP_HOST")
    app_port: int = Field(default=8000, env="APP_PORT")
    debug: bool = Field(default=False, env="DEBUG")

    database_url: str = Field(
        default="sqlite:///./app/data/flow_editor.sqlite3",
        env="DATABASE_URL"
    )

    exports_dir: str = Field(default="./app/exports", env="EXPORTS_DIR")
    uploads_dir: str = Field(default="./app/uploads", env="UPLOADS_DIR")

    base_dir: Path = Path(__file__).parent

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def get_exports_path(self) -> Path:
        p = Path(self.exports_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def get_uploads_path(self) -> Path:
        p = Path(self.uploads_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def has_api_key(self) -> bool:
        return bool(self.anthropic_api_key and self.anthropic_api_key.startswith("sk-"))


settings = Settings()
