from database.cart_permi_conduite.driving_license_entity import SessionLocal, PermiDataDB
from datetime import datetime


def save_permi_data(permi_data):
    session = SessionLocal()
    try:
        db_entry = PermiDataDB(
            numero_permis=permi_data.permis.numero_permis,
            nom_fr=permi_data.identite.nom.fr,
            nom_ar=permi_data.identite.nom.ar,
            prenom_fr=permi_data.identite.prenom.fr,
            prenom_ar=permi_data.identite.prenom.ar,
            date_naissance=datetime.strptime(permi_data.naissance.date, "%d.%m.%Y").date(),
            lieu_fr=permi_data.naissance.lieu.fr,
            lieu_ar=permi_data.naissance.lieu.ar,
            date_delivrance=datetime.strptime(permi_data.permis.date_delivrance, "%d.%m.%Y").date(),
            date_expiration=datetime.strptime(permi_data.permis.date_expiration, "%d.%m.%Y").date(),
            categorie=permi_data.permis.categorie
        )
        session.add(db_entry)
        session.commit()
        print("Permis de conduire enregistré avec succès !")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_all_permi_data():
    session = SessionLocal()
    try:
        return session.query(PermiDataDB).all()
    finally:
        session.close()
        