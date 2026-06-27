from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Invoice OCR Processor"
    debug: bool = True
    api_keys: list[str] = ["demo-key"]
    gemini_api_key: str = ""


settings = Settings()
