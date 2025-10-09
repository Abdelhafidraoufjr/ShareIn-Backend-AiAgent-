from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.database_config import DatabaseConfig

Base = declarative_base()

class GrisDataDB(Base):
    __tablename__ = "gris_data"

    id = Column(Integer, primary_key=True)

    numero_matricule_marocain = Column(String, unique=True, nullable=False)
    immatriculation_anterieure = Column(String, nullable=True)

    date_premiere_immatriculation = Column(Date, nullable=True)      
    date_derniere_immatriculation = Column(Date, nullable=True)     
    date_mutation = Column(Date, nullable=True)

    marque = Column(String, nullable=True)
    type = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    type_carburant = Column(String, nullable=True)
    numero_chassis = Column(String, nullable=True)
    nombre_cylindres = Column(Integer, nullable=True)
    puissance_fiscale = Column(Integer, nullable=True)
    restriction = Column(String, nullable=True)

    usage_type = Column(String, nullable=True)
    usage_description = Column(String, nullable=True)

    nom_fr = Column(String, nullable=True)
    nom_ar = Column(String, nullable=True)
    prenom_fr = Column(String, nullable=True)
    prenom_ar = Column(String, nullable=True)

    adresse_fr = Column(String, nullable=True)
    adresse_ar = Column(String, nullable=True)

    date_validite = Column(Date, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Create engine with connection pooling and SSL configuration
engine = create_engine(
    DatabaseConfig.get_db_url(),
    **DatabaseConfig.get_engine_options()
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(engine)
