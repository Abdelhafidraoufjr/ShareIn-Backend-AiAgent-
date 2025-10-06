"""
Routes pour les données des graphiques du dashboard
"""
from flask import Blueprint, jsonify
from middlewares.decorators import token_required
from charts.chart_service import ChartService

charts_bp = Blueprint('charts', __name__)

@charts_bp.route('/overview', methods=['GET'])
@token_required
def get_cards_overview(current_user):
    """Récupère l'aperçu général des cartes"""
    try:
        data = ChartService.get_cards_overview()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@charts_bp.route('/gender-distribution', methods=['GET'])
@token_required
def get_gender_distribution(current_user):
    """Récupère la distribution des genres"""
    try:
        data = ChartService.get_gender_distribution()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@charts_bp.route('/cities-distribution', methods=['GET'])
@token_required
def get_cities_distribution(current_user):
    """Récupère la distribution des villes"""
    try:
        data = ChartService.get_cities_distribution()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@charts_bp.route('/license-categories', methods=['GET'])
@token_required
def get_license_categories(current_user):
    """Récupère les catégories de permis"""
    try:
        data = ChartService.get_license_categories()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@charts_bp.route('/car-usage-types', methods=['GET'])
@token_required
def get_car_usage_types(current_user):
    """Récupère les types d'usage des voitures"""
    try:
        data = ChartService.get_car_usage_types()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@charts_bp.route('/monthly-stats', methods=['GET'])
@token_required
def get_monthly_stats(current_user):
    """Récupère les statistiques mensuelles"""
    try:
        data = ChartService.get_monthly_processing_stats()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@charts_bp.route('/daily-stats', methods=['GET'])
@token_required
def get_daily_stats(current_user):
    """Récupère les statistiques quotidiennes"""
    try:
        data = ChartService.get_daily_processing_stats()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@charts_bp.route('/dashboard', methods=['GET'])
@token_required
def get_all_dashboard_data(current_user):
    """Récupère toutes les données nécessaires pour le dashboard"""
    try:
        data = ChartService.get_all_dashboard_charts()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@charts_bp.route('/essential', methods=['GET'])
@token_required
def get_essential_dashboard(current_user):
    """Récupère seulement les données essentielles et fiables"""
    try:
        data = ChartService.get_essential_dashboard_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500