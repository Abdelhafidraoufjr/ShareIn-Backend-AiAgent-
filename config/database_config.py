import os

class DatabaseConfig:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "intelli_backend_db")
    DB_SSLMODE = os.getenv("DB_SSLMODE", "require")
    # Note: channel_binding removed as it causes issues with Neon PostgreSQL

    @classmethod
    def get_db_url(cls):
        """
        Returns database URL with SSL configuration for Neon PostgreSQL.
        Removes channel_binding to avoid SSL connection issues.
        """
        return (
            f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
            f"?sslmode={cls.DB_SSLMODE}"
        )
    
    @classmethod
    def get_engine_options(cls):
        """
        Returns SQLAlchemy engine configuration options optimized for Neon PostgreSQL.
        
        Key options:
        - pool_pre_ping: Test connections before using them
        - pool_recycle: Recycle connections after 300 seconds (5 minutes)
        - pool_size: Maximum 10 concurrent connections
        - max_overflow: Allow up to 20 overflow connections
        - pool_timeout: Wait up to 30 seconds for a connection
        """
        return {
            "pool_pre_ping": True,  # Test connection before using
            "pool_recycle": 300,    # Recycle connections after 5 minutes
            "pool_size": 10,        # Max concurrent connections
            "max_overflow": 20,     # Max overflow connections
            "pool_timeout": 30,     # Timeout for getting connection
            "echo": False,          # Disable SQL query logging
        }

