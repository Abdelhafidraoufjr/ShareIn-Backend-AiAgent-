import os
from flask import Blueprint, request, jsonify, current_app
from azure.AzureOCRService import AzureOCRService
from services.vehicle_registration_ai_service import AIServiceCartGris
from database.cart_gris_matricul.vehicle_registration_database_service import save_gris_data, get_all_gris_data
from middlewares.decorators import token_required
import json


ocr_service = AzureOCRService()
ai_service_gris = AIServiceCartGris()

gris_bp = Blueprint("gris_bp", __name__)

@gris_bp.route("/process", methods=["POST"])
@token_required
def process_gris(current_user):
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
        gris_data = ai_service_gris.parse_cart_gris_data(full_text)
        save_gris_data(gris_data)
        return jsonify(gris_data.model_dump())
    except ValueError as ve:
        return jsonify({"error": f"Erreur de parsing: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur générale: {str(e)}"}), 500
    
@gris_bp.route("/all", methods=["GET"])
@token_required
def get_all_gris(current_user):
    try:
        gris_list = get_all_gris_data()
        result = [gris.__dict__ for gris in gris_list]
        for item in result:
            item.pop('_sa_instance_state', None)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des données: {str(e)}"}), 500

@gris_bp.route("/evolution-mensuel", methods=["GET"])
@token_required
def get_monthly_evolution(current_user):
    try:
        gris_list = get_all_gris_data()
        monthly_counts = {}

        for gris in gris_list:
            month_year = gris.date_premiere_immatriculation.strftime("%Y-%m")
            if month_year not in monthly_counts:
                monthly_counts[month_year] = 0
            monthly_counts[month_year] += 1

        sorted_monthly_counts = dict(sorted(monthly_counts.items()))

        return jsonify(sorted_monthly_counts)
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des données: {str(e)}"}), 500
