import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "SafeWalk API"
    APP_VERSION: str = "1.0.0"
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "safewalk")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()
