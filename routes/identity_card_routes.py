import os
from flask import Blueprint, request, jsonify, current_app
from azure.AzureOCRService import AzureOCRService
from services.identity_card_ai_service import AIService
from database.cart_identite_national.identity_card_database_service import save_cin_data, get_all_cin_data
from middlewares.decorators import token_required

ocr_service = AzureOCRService()
ai_service = AIService()

cin_bp = Blueprint("cin_bp", __name__)

@cin_bp.route("/process", methods=["POST"])
@token_required
def process_cin(current_user):
    recto = request.files.get("recto")
    verso = request.files.get("verso")

    if not recto or not verso:
        return jsonify({"error": "Veuillez uploader recto et verso"}), 400

    recto_path = os.path.join(current_app.config["UPLOAD_FOLDER"], recto.filename)
    verso_path = os.path.join(current_app.config["UPLOAD_FOLDER"], verso.filename)
    recto.save(recto_path)
    verso.save(verso_path)

    recto_text = ocr_service.extract_text(recto_path)
    verso_text = ocr_service.extract_text(verso_path)
    full_text = recto_text + "\n" + verso_text

    try:
        cin_data = ai_service.parse_cin_data(full_text)
        save_cin_data(cin_data)
        return jsonify(cin_data.model_dump())  
    except ValueError as ve:
        return jsonify({"error": f"Erreur de parsing: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur générale: {str(e)}"}), 500

@cin_bp.route("/all", methods=["GET"])
@token_required
def get_all_cin(current_user):
    try:
        cin_list = get_all_cin_data()
        result = [cin.__dict__ for cin in cin_list]
        for item in result:
            item.pop('_sa_instance_state', None)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des données: {str(e)}"}), 500

