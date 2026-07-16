from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str 
    APP_VERSION: str 

    DATABASE_URL: str 
    
    HOST: str
    PORT: int

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    OLLAMA_URL: str
    OLLAMA_MODEL: str
    
    TAVILY_API_KEY: str
    
    WHISPER_MODEL: str
    WHISPER_DEVICE: str
    WHISPER_COMPUTE_TYPE: str
    
    TEMP_AUDIO_PATH: str
    
    MAX_AUDIO_SIZE: float = 25 * 1024 * 1024
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()