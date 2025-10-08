# =========================================================
# Dockerfile optimisé pour Flask AI Agent (CPU only)
# =========================================================
FROM python:3.9-slim

WORKDIR /app

# Copier les fichiers
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Variables d'environnement de base
ENV FLASK_APP=application.py
ENV PYTHONPATH=/app
ENV PATH=/opt/conda/bin:$PATH

# Utilisateur non-root
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "application:create_app()"]
