"""Configuration management for Voice Automation Platform."""

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_model: str = Field(default="gpt-4", description="Default OpenAI model")
    openai_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    openai_max_tokens: int = Field(default=2000, ge=1, le=128000)

    # Server Configuration
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1, le=65535)
    debug: bool = Field(default=False)
    reload: bool = Field(default=False)

    # Database
    database_url: str = Field(
        default="sqlite:///./voice_automation.db",
        description="Database connection URL",
    )

    # Webhook Configuration
    webhook_base_url: str = Field(
        default="http://localhost:8000",
        description="Base URL for webhooks",
    )
    webhook_secret: str = Field(default="change_me_in_production")
    webhook_timeout: int = Field(default=30, ge=1, le=300)

    # MCP Server Configuration
    mcp_server_dir: Path = Field(default=Path("./mcp_servers"))
    mcp_auto_start: bool = Field(default=True)
    mcp_server_timeout: int = Field(default=60, ge=1, le=600)

    # Voice Configuration
    enable_voice_input: bool = Field(default=True)
    enable_voice_output: bool = Field(default=True)
    voice_provider: Literal[
        "web_speech_api", "whisper", "azure_speech", "google_speech"
    ] = Field(default="web_speech_api")

    # Agent Configuration
    max_concurrent_agents: int = Field(default=10, ge=1, le=100)
    agent_timeout: int = Field(default=300, ge=1, le=3600)
    agent_retry_attempts: int = Field(default=3, ge=0, le=10)

    # Task Configuration
    max_concurrent_tasks: int = Field(default=5, ge=1, le=50)
    task_queue_size: int = Field(default=100, ge=1, le=1000)
    task_result_ttl: int = Field(default=3600, ge=60, le=86400)

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO"
    )
    log_format: Literal["json", "text"] = Field(default="json")
    log_file: Path | None = Field(default=Path("./logs/voice_automation.log"))

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"]
    )
    cors_allow_credentials: bool = Field(default=True)

    # Redis (optional)
    redis_url: str | None = Field(default=None)

    # Security
    secret_key: str = Field(default="change_me_in_production")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30, ge=1, le=1440)

    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, ge=1, le=10000)
    rate_limit_per_hour: int = Field(default=1000, ge=1, le=100000)

    # Feature Flags
    enable_analytics: bool = Field(default=True)
    enable_telemetry: bool = Field(default=False)
    enable_webhooks: bool = Field(default=True)

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.debug or self.reload

    @property
    def base_url(self) -> str:
        """Get the base URL for the application."""
        return f"http://{self.host}:{self.port}"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings

