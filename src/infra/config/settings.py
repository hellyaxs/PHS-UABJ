import os
from pathlib import Path
from dotenv import load_dotenv
from passlib.context import CryptContext

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

# Instância única do CryptContext para garantir consistência
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DatabaseSettings:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "carlos")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    
    @classmethod
    def get_database_url(cls) -> str:
        return f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"

class MQTTSettings:
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
    MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

class AppSettings:
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    API_V1_STR = "/api/v1"
    PROJECT_NAME = os.getenv("PROJECT_NAME", "FastAPI App")

class EmailSettings:
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@example.com")

class UserSettings:
    DEFAULT_USER_EMAIL = os.getenv("DEFAULT_USER_EMAIL", "admin@exemplo.com")
    DEFAULT_USER_PASSWORD = os.getenv("DEFAULT_USER_PASSWORD", "123456")
    DEFAULT_USER_FULL_NAME = os.getenv("DEFAULT_USER_FULL_NAME", "Administrador")
    DEFAULT_USER_IS_ACTIVE = os.getenv("DEFAULT_USER_IS_ACTIVE", True)

    def get_hashed_password(self) -> str:
        return pwd_context.hash(self.DEFAULT_USER_PASSWORD)

# Instância única das configurações
db_settings = DatabaseSettings()
mqtt_settings = MQTTSettings()
app_settings = AppSettings()
email_settings = EmailSettings()
user_settings = UserSettings()
