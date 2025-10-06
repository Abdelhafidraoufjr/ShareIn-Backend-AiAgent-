import os
import re
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from models.vehicle_registration_model import CartGrisData


class AIServiceCartGris:
    def __init__(self):
        endpoint = "https://models.github.ai/inference"
        model = "openai/gpt-4.1-nano"
        token = os.environ["GITHUB_TOKEN"]

        self.model = model
        self.client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

    def _normalize_matricule_number(self, numero: str) -> str:
        """Normalise le numéro de matricule au bon format"""
        if not numero:
            return "1234 أ 56"
        
        numero = str(numero).strip()
        
        pattern = r"^\d{1,5}\s[أ-يA-Z]\s\d{2}$"
        if re.match(pattern, numero, flags=re.IGNORECASE):
            return numero
        
        dash_pattern = r"^(\d{1,5})[-.]?(\d+)[-.]?(\d{2})$"
        match = re.match(dash_pattern, numero)
        if match:
            num1, middle, num2 = match.groups()
            letter_map = {"1": "أ", "2": "ب", "3": "ج", "4": "د", "5": "ه"}
            letter = letter_map.get(middle, "أ")
            return f"{num1} {letter} {num2}"
        
        return "1234 أ 56"
    
    def _normalize_immatriculation_anterieure(self, numero: str) -> str:
        """Normalise le numéro d'immatriculation antérieure"""
        if not numero:
            return "WW-123456"
        
        numero = str(numero).strip()
        
        if re.match(r"^WW-\d{1,6}$", numero, flags=re.IGNORECASE):
            return numero.upper()
        
        ww_pattern = r"WW\s*[-.]?\s*(\d+)"
        match = re.search(ww_pattern, numero, flags=re.IGNORECASE)
        if match:
            return f"WW-{match.group(1)}"
        
        return "WW-123456"
    
    def _normalize_usage_type(self, usage_type: str) -> str:
        """Normalise le type d'usage"""
        if not usage_type:
            return "Particulier"
        
        usage_type = str(usage_type).strip().lower()
        
        usage_mapping = {
            "propriétaire": "Particulier",
            "particulier": "Particulier",
            "personnel": "Particulier",
            "privé": "Particulier",
            "transport marchandises": "Transport de marchandises",
            "marchandises": "Transport de marchandises",
            "commercial": "Transport de marchandises",
            "transport commun": "Transport en commun",
            "transport public": "Transport en commun",
            "location chauffeur": "Location avec chauffeur",
            "location sans chauffeur": "Location sans chauffeur",
            "location": "Location sans chauffeur"
        }
        
        return usage_mapping.get(usage_type, "Particulier")
    
    def _safe_int(self, value, default=0):
        """Conversion sécurisée en entier"""
        if value is None:
            return default
        try:
            return int(float(str(value)))
        except (ValueError, TypeError):
            return default
    
    def _safe_float(self, value, default=0.0):
        """Conversion sécurisée en float"""
        if value is None:
            return default
        try:
            return float(str(value))
        except (ValueError, TypeError):
            return default

    def _post_process_data(self, data: dict) -> dict:
        """Post-traitement des données extraites"""
        processed = data.copy()
        
        if "numero_matricule_marocain" in processed:
            numero = processed["numero_matricule_marocain"].get("numero", "")
            processed["numero_matricule_marocain"]["numero"] = self._normalize_matricule_number(numero)
        
        if "immatriculation_anterieure" in processed:
            numero = processed["immatriculation_anterieure"].get("numero", "")
            processed["immatriculation_anterieure"]["numero"] = self._normalize_immatriculation_anterieure(numero)
        
        if "usage" in processed and "type" in processed["usage"]:
            usage_type = processed["usage"]["type"]
            processed["usage"]["type"] = self._normalize_usage_type(usage_type)
        
        numeric_fields = {
            "nombre_cylindres": 4,
            "puissance_fiscale": 8,
        }
        
        for field, default in numeric_fields.items():
            if field in processed:
                if isinstance(default, int):
                    processed[field] = self._safe_int(processed[field], default)
                else:
                    processed[field] = self._safe_float(processed[field], default)
        
        return processed

    def parse_with_fallback(self, raw_text: str) -> CartGrisData:
        """Version avec fallback robuste"""
        try:
            return self.parse_cart_gris_data(raw_text)
        except Exception as e:
            print(f"Échec parsing: {e}")
            print("Utilisation fallback...")
            
            default_data = {
                "numero_matricule_marocain": {"numero": "1234 أ 56"},
                "immatriculation_anterieure": {"numero": "WW-123456"},
                "mise_en_circulation": {"date": "01.01.2020"},
                "mise_en_circulation_au_maroc": {"date": "01.01.2020"},
                "mutation": {"date": "01.01.2021"},
                "usage": {"type": "Particulier", "description": "Usage personnel du véhicule"},
                "marque": "NON DETECTE",
                "Type": "NON DETECTE",
                "Genre": "VP", 
                "type_carburant": "Essence",
                "numero_chassis": "NON DETECTE",
                "nombre_cylindres": 4,
                "puissance_fiscale": 8,
                "restriction": "Aucune",
                "identite": {
                    "nom": {"fr": "NON DETECTE", "ar": "غير محدد"},
                    "prenom": {"fr": "NON DETECTE", "ar": "غير محدد"}
                },
                "adresse": {"fr": "Adresse non détectée", "ar": "عنوان غير محدد"},
                "valiadtion": "31.12.2025"
            }
            
            return CartGrisData.model_validate(default_data)

    def parse_cart_gris_data(self, raw_text: str) -> CartGrisData:
        prompt = f"""
Tu es un expert en extraction de données de cartes grises marocaines.
Analyse le texte OCR et retourne UNIQUEMENT un JSON avec les données extraites.

ATTENTION FORMATS CRITIQUES :
- numero_matricule_marocain : Format EXACT "NNNN L NN" avec espaces (ex: "1234 أ 56")
- immatriculation_anterieure : Format EXACT "WW-NNNNNN" avec tiret (ex: "WW-123456") 
- usage.type : EXACTEMENT un de ces mots: "Particulier", "Transport de marchandises", "Transport en commun", "Location avec chauffeur", "Location sans chauffeur"

STRUCTURE JSON ATTENDUE:
{{
  "numero_matricule_marocain": {{ "numero": "1234 أ 56" }},
  "immatriculation_anterieure": {{ "numero": "WW-123456" }},
  "mise_en_circulation": {{ "date": "01.01.2020" }},
  "mise_en_circulation_au_maroc": {{ "date": "01.01.2020" }},
  "mutation": {{ "date": "01.01.2021" }},
  "usage": {{ "type": "Particulier", "description": "Usage personnel" }},
  "marque": "Toyota",
  "Type": "Berline", 
  "Genre": "VP",
  "type_carburant": "Essence",
  "numero_chassis": "ABC123456789",
  "nombre_cylindres": 4,
  "puissance_fiscale": 8,
  "restriction": "Aucune",
  "identite": {{
    "nom": {{ "fr": "DUPONT", "ar": "دوبونت" }},
    "prenom": {{ "fr": "Jean", "ar": "جان" }}
  }},
  "adresse": {{ "fr": "Casablanca", "ar": "الدار البيضاء" }},
  "valiadtion": "31.12.2025"
}}

RÈGLES IMPORTANTES :
- Si un numéro ressemble à "1107-1-81", convertis en "1107 أ 81" (remplace tirets par espaces et chiffre du milieu par lettre arabe)
- Si immatriculation est "WW131384", convertis en "WW-131384"  
- Pour usage, utilise EXACTEMENT "Particulier" au lieu de "Propriétaire"
- JAMAIS de valeur null/None pour les nombres - utilise des valeurs par défaut réalistes
- Retourne UNIQUEMENT le JSON, aucun autre texte

Texte OCR :
{raw_text}
        """

        response = self.client.complete(
            model=self.model,
            messages=[
                SystemMessage("Tu extrais des données de cartes grises. JSON valide uniquement, formats exacts requis."),
                UserMessage(prompt),
            ],
            temperature=0.1,
            top_p=0.9,
        )

        output = response.choices[0].message.content.strip()

        if output.startswith("```"):
            lines = output.split('\n')
            start_idx = 0
            end_idx = len(lines)
            
            for i, line in enumerate(lines):
                if line.strip().startswith('```'):
                    start_idx = i + 1
                    break
            
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip().endswith('```'):
                    end_idx = i
                    break
            
            output = '\n'.join(lines[start_idx:end_idx])

        first_brace = output.find('{')
        if first_brace != -1:
            output = output[first_brace:]

        last_brace = output.rfind('}')
        if last_brace != -1:
            output = output[:last_brace + 1]

        try:
            parsed_json = json.loads(output)
            
            processed_json = self._post_process_data(parsed_json)
            
            return CartGrisData.model_validate(processed_json)
            
        except json.JSONDecodeError as e:
            print(f"Erreur JSON: {e}")
            raise ValueError(f"Réponse JSON invalide: {e}")
        except Exception as e:
            print(f"Erreur validation: {e}")
            raise