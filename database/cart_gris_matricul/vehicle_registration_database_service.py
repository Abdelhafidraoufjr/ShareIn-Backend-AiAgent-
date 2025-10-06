from database.cart_gris_matricul.vehicle_registration_entity import SessionLocal, GrisDataDB
from datetime import datetime

def save_gris_data(gris_data):
    session = SessionLocal()
    try:
        db_entry = GrisDataDB(
            numero_matricule_marocain = gris_data.numero_matricule_marocain.numero,
            immatriculation_anterieure = gris_data.immatriculation_anterieure.numero,
            date_premiere_immatriculation = datetime.strptime(
                gris_data.mise_en_circulation.date, "%d.%m.%Y"
            ).date() if gris_data.mise_en_circulation.date else None,
            date_derniere_immatriculation = datetime.strptime(
                gris_data.mise_en_circulation_au_maroc.date, "%d.%m.%Y"
            ).date() if gris_data.mise_en_circulation_au_maroc.date else None,
            date_mutation = datetime.strptime(
                gris_data.mutation.date, "%d.%m.%Y"
            ).date() if gris_data.mutation.date else None,

            marque = gris_data.marque,
            type = gris_data.Type,
            genre = gris_data.Genre,
            type_carburant = gris_data.type_carburant,
            numero_chassis = gris_data.numero_chassis,
            nombre_cylindres = gris_data.nombre_cylindres,
            puissance_fiscale = gris_data.puissance_fiscale,
            restriction = gris_data.restriction,

            usage_type = gris_data.usage.type,
            usage_description = gris_data.usage.description,

            nom_fr = gris_data.identite.nom.fr,
            nom_ar = gris_data.identite.nom.ar,
            prenom_fr = gris_data.identite.prenom.fr,
            prenom_ar = gris_data.identite.prenom.ar,

            adresse_fr = gris_data.adresse.fr,
            adresse_ar = gris_data.adresse.ar,

            date_validite = datetime.strptime(
                gris_data.valiadtion, "%d.%m.%Y"
            ).date() if gris_data.valiadtion else None
        )
        session.add(db_entry)
        session.commit()
        print("Carte grise enregistrée avec succès !")
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

def get_all_gris_data():
    session = SessionLocal()
    try:
        return session.query(GrisDataDB).all()
    finally:
        session.close()
                

