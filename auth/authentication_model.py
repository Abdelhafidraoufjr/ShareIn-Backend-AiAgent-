import bcrypt
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.database_config import DatabaseConfig

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)

    def verify_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), self.hashed_password.encode())

    @classmethod
    def create(cls, session, email: str, plain_password: str, full_name: str = None):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode(), salt).decode()
        user = cls(email=email, hashed_password=hashed, full_name=full_name)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

engine = create_engine(DatabaseConfig.get_db_url())
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
