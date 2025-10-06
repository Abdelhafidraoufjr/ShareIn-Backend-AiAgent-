import os
import time
import random
from dotenv import load_dotenv
from openai import OpenAI
from models.identity_card_model import CINData

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_BASE_URL = os.getenv("GITHUB_BASE_URL")
MODEL_NAME_GITHUB = os.getenv("MODEL_NAME_GITHUB")


class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=GITHUB_TOKEN, base_url=GITHUB_BASE_URL)
        self.model = MODEL_NAME_GITHUB

    def parse_cin_data(self, raw_text: str, max_retries: int = 5) -> CINData:
        """
        Calls GitHub-hosted OpenAI model to parse CNIE text into structured CINData.
        Handles retries on 502/network errors and cleans raw JSON output.
        """
        prompt = f"""
Voici du texte OCR extrait d'une carte nationale d'identité marocaine CNIE bilingue.

INSTRUCTIONS STRICTES:
1. SÉPARE le texte français du texte arabe pour chaque champ.
2. Le français utilise l'alphabet latin (A-Z, 0-9).
3. L'arabe utilise l'alphabet arabe (٠-٩, ا-ي).
4. Pour l'adresse : cherche 'RES', 'IMM', 'NR', 'CASA' = français / cherche 'إقامة', 'عمارة', 'رقم' = arabe.
5. Pour les noms : cherche la version MAJUSCULES = français / cherche les caractères arabes = arabe.
6. Pour les lieux : ex 'AIN SEBAA' = français / 'عين السبع' = arabe.
7. ⚠️ Numéro d'état civil = uniquement registre naissance. Ne pas mettre le numéro du verso (ex: CAN 279975).
8. Concernant les noms des parents, ignore Fils de / Fille de / Etde / Et de / و.
9. Concernant le lieu de naissance en arab ignore ب.

Texte OCR à analyser:
{raw_text}
"""

        attempt = 0
        while attempt < max_retries:
            try:
                response = self.client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Tu es expert en cartes d'identité marocaines bilingues. Sépare parfaitement le FRANÇAIS et l'ARABE, retourne uniquement JSON."
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format=CINData,
                )
                return response.choices[0].message.parsed
            except Exception as e:
                if "502" in str(e) or "network" in str(e).lower():
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(wait_time)
                    attempt += 1
                else:
                    raise e

