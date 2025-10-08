import os

class DatabaseConfig:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "intelli_backend_db")
    DB_SSLMODE = os.getenv("DB_SSLMODE", "disable")
    DB_CHANNEL_BINDING = os.getenv("DB_CHANNEL_BINDING", "disable")


    @classmethod
    def get_db_url(cls):
        return (
            f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
            f"?sslmode={cls.DB_SSLMODE}&channel_binding={cls.DB_CHANNEL_BINDING}"
        )

