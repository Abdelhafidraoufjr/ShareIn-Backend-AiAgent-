from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config.database_config import DatabaseConfig

Base = declarative_base()

class CINDataDB(Base):
    __tablename__ = "cin_data"
    
    id = Column(Integer, primary_key=True)
    cin = Column(String, unique=True)
    nom_fr = Column(String)
    nom_ar = Column(String)
    prenom_fr = Column(String)
    prenom_ar = Column(String)
    date_naissance = Column(Date)
    lieu_fr = Column(String)
    lieu_ar = Column(String)
    adresse_fr = Column(String)
    adresse_ar = Column(String)
    sexe = Column(String)
    validite = Column(Date)
    pere_fr = Column(String)
    pere_ar = Column(String)
    mere_fr = Column(String)
    mere_ar = Column(String)
    numero_etat_civil = Column(String)

engine = create_engine(DatabaseConfig.get_db_url())
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}