import os
from flask import Blueprint, request, jsonify, current_app
from azure.AzureOCRService import AzureOCRService
from services.driving_license_ai_service import AIServicePermis
from database.cart_permi_conduite.driving_license_database_service import save_permi_data, get_all_permi_data
from middlewares.decorators import token_required

ocr_service = AzureOCRService()
ai_service_permis = AIServicePermis()

permis_bp = Blueprint("permis_bp", __name__)


@permis_bp.route("/process", methods=["POST", "OPTIONS"])
@token_required
def process_permis(current_user):
    recto = request.files.get("recto")
    verso = request.files.get("verso")

    if not recto:
        return jsonify({"error": "Veuillez uploader recto"}), 400

    recto_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], recto.filename)
    verso_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], verso.filename)
    recto.save(recto_path)
    verso.save(verso_path)

    recto_text = ocr_service.extract_text(recto_path)
    verso_text = ocr_service.extract_text(verso_path)
    full_text = recto_text + "\n" + verso_text

    try:
        permis_data = ai_service_permis.parse_permi_data(full_text)
        save_permi_data(permis_data)
        return jsonify(permis_data.model_dump())
    except ValueError as ve:
        return jsonify({"error": f"Erreur de parsing: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur générale: {str(e)}"}), 500


@permis_bp.route("/all", methods=["GET"])
@token_required
def get_all_permis(current_user):
    try:
        permis_list = get_all_permi_data()
        result = [permis.__dict__ for permis in permis_list]
        for item in result:
            item.pop('_sa_instance_state', None)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des données: {str(e)}"}), 500
