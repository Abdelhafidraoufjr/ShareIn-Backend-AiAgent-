from database.cart_identite_national.identity_card_entity import SessionLocal, CINDataDB
from datetime import datetime

def save_cin_data(cin_data):
    session = SessionLocal()
    try:
        db_entry = CINDataDB(
            cin=cin_data.cin,
            nom_fr=cin_data.identite.nom.fr,
            nom_ar=cin_data.identite.nom.ar,
            prenom_fr=cin_data.identite.prenom.fr,
            prenom_ar=cin_data.identite.prenom.ar,
            date_naissance=datetime.strptime(cin_data.naissance.date, "%d.%m.%Y").date(),
            lieu_fr=cin_data.naissance.lieu.fr,
            lieu_ar=cin_data.naissance.lieu.ar,
            adresse_fr=cin_data.adresse.fr,
            adresse_ar=cin_data.adresse.ar,
            sexe=cin_data.sexe,
            validite=datetime.strptime(cin_data.validite, "%d.%m.%Y").date(),
            pere_fr=cin_data.parents.pere.fr,
            pere_ar=cin_data.parents.pere.ar,
            mere_fr=cin_data.parents.mere.fr,
            mere_ar=cin_data.parents.mere.ar,
            numero_etat_civil=cin_data.etat_civil.numero_etat_civil
        )
        session.add(db_entry)
        session.commit()
        print("CIN enregistré avec succès !")
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        
def get_all_cin_data():
    session = SessionLocal()
    try:
        return session.query(CINDataDB).all()
    finally:
        session.close()

        