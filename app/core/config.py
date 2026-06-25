from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Invoice OCR Processor"
    debug: bool = True
    api_keys: list[str] = ["demo-key"]
    gemini_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
