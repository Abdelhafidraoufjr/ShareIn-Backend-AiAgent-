from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config.database_config import DatabaseConfig

Base = declarative_base()

class PermiDataDB(Base):
    __tablename__ = "permi_data"
    
    id = Column(Integer, primary_key=True)
    numero_permis = Column(String, unique=True)
    nom_fr = Column(String)
    nom_ar = Column(String)
    prenom_fr = Column(String)
    prenom_ar = Column(String)
    date_naissance = Column(Date)
    lieu_fr = Column(String)
    lieu_ar = Column(String)
    date_delivrance = Column(Date)
    date_expiration = Column(Date)
    categorie = Column(String)



# Create engine with connection pooling and SSL configuration
engine = create_engine(
    DatabaseConfig.get_db_url(),
    **DatabaseConfig.get_engine_options()
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(engine)
def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
