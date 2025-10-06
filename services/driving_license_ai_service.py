import os
import time
import random
from dotenv import load_dotenv
from openai import OpenAI
from models.driving_license_model import PermisData


load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_BASE_URL = os.getenv("GITHUB_BASE_URL")
MODEL_NAME_GITHUB = os.getenv("MODEL_NAME_GITHUB")


class AIServicePermis:
    def __init__(self):
        self.client = OpenAI(api_key=GITHUB_TOKEN, base_url=GITHUB_BASE_URL)
        self.model = MODEL_NAME_GITHUB

    def parse_permi_data(self, raw_text: str, max_retries: int = 5) -> PermisData:
        prompt = f"""
... (instructions inchangées ci-dessus) ...
3. DÉTECTION DE LA CATÉGORIE :
   - Cherchez dans le texte les catégories suivantes UNIQUEMENT : A1, A, B, C, D, E(B), E(C), E(D)
   - Ces catégories peuvent apparaître :
     * Dans un carré sur le recto du permis
     * Dans le tableau "Catégories | Date de délivrance | Restrictions" au verso
     * Accompagnées de leur équivalent arabe : A1 (1أ), A (أ), B (ب), C (ج), D (د)
   - Si plusieurs catégories sont présentes, prenez celle associée à la date de délivrance principale
   - Format attendu : exactement comme trouvé (A, A1, B, C, D, etc.)

IMPORTANT : La catégorie doit être exactement l'une de ces valeurs : A1, A, B, C, 

Texte OCR :
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
                            "content": "Tu es un expert en permis de conduire marocains bilingues. Extrais les champs avec séparation FR/AR."
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format=PermisData,
                )
                return response.choices[0].message.parsed
            except Exception as e:
                if "502" in str(e) or "network" in str(e).lower():
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(wait_time)
                    attempt += 1
                else:
                    raise e
