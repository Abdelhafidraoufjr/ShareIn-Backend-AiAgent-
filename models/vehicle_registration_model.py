from pydantic import BaseModel, Field, validator, model_validator
from typing import Literal
import re

ARABIC_LETTERS = r"\u0621-\u064A\u0660-\u0669"

class LangText(BaseModel):
    fr: str
    ar: str
    
    @validator('fr')
    def validate_french_text(cls, v):
        arabic_chars = sum(1 for c in v if '\u0600' <= c <= '\u06FF')
        if arabic_chars > len(v) * 0.3:  
            raise ValueError(f"Le champ français contient trop de caractères arabes: {v}")
        return v
    
    @validator('ar')
    def validate_arabic_text(cls, v):
        arabic_chars = sum(1 for c in v if '\u0600' <= c <= '\u06FF')
        if arabic_chars == 0 and len(v) > 0:
            raise ValueError(f"Le champ arabe ne contient aucun caractère arabe: {v}")
        return v

class Identite(BaseModel):
    nom: LangText
    prenom: LangText

class Adresse(LangText):
    pass    

class NumeroMatriculeMarocain(BaseModel):
    numero: str = Field(..., description="Numéro de matricule marocain au format NNNN L NN")

    @validator("numero")
    def check_numero_format(cls, v):
        pattern = r"^\d{1,5}\s[أ-يA-Z]\s\d{2}$"
        if not re.fullmatch(pattern, v, flags=re.IGNORECASE):
            raise ValueError("Le numéro matricule doit être au format NNNN L NN (ex: 1234 أ 56 ou 1234 B 56)")
        return v

class ImmatriculationAnterieure(BaseModel):
    numero: str = Field(..., description="Numéro d'immatriculation antérieure (WW) au format WW-NNNNNN")

    @validator("numero")
    def check_numero_format(cls, v):
        pattern = r"^WW-\d{1,6}$"
        if not re.fullmatch(pattern, v, flags=re.IGNORECASE):
            raise ValueError("Le numéro d'immatriculation antérieure doit être au format WW-NNNNNN (ex: WW-123456)")
        return v
    
class MiseEnCirculation(BaseModel):
    date: str = Field(..., description="Date au format JJ.MM.AAAA ou JJ/MM/AAAA")

    @validator("date")
    def check_date_format(cls, v):
        if not re.fullmatch(r"\d{2}[./]\d{2}[./]\d{4}", v):
            raise ValueError("La date doit être au format JJ.MM.AAAA ou JJ/MM/AAAA")
        return v.replace("/", ".")
class MiseEnCirculationAuMaroc(BaseModel):
    date: str = Field(..., description="Date au format JJ.MM.AAAA ou JJ/MM/AAAA")

    @validator("date")
    def check_date_format(cls, v):
        if not re.fullmatch(r"\d{2}[./]\d{2}[./]\d{4}", v):
            raise ValueError("La date doit être au format JJ.MM.AAAA ou JJ/MM/AAAA")
        return v.replace("/", ".")
class Mutation(BaseModel):
    date: str = Field(..., description="Date au format JJ.MM.AAAA ou JJ/MM/AAAA")

    @validator("date")
    def check_date_format(cls, v):
        if not re.fullmatch(r"\d{2}[./]\d{2}[./]\d{4}", v):
            raise ValueError("La date doit être au format JJ.MM.AAAA ou JJ/MM/AAAA")
        return v.replace("/", ".")

class Usage(BaseModel):
    type: Literal["Particulier", "Transport de marchandises", "Transport en commun", "Location avec chauffeur", "Location sans chauffeur"]
    description: str = Field(..., description="Description textuelle de l'usage")
    @validator("description")
    def validate_description(cls, v):
        if len(v) < 3:
            raise ValueError("La description doit contenir au moins 3 caractères")
        return v
    

class CartGrisData(BaseModel):
    numero_matricule_marocain: NumeroMatriculeMarocain
    immatriculation_anterieure: ImmatriculationAnterieure
    mise_en_circulation: MiseEnCirculation
    mise_en_circulation_au_maroc: MiseEnCirculationAuMaroc
    mutation: Mutation
    usage: Usage
    marque: str = Field(..., description="Marque du véhicule")
    Type: str = Field(..., description="Type du véhicule")
    Genre: str = Field(..., description="Genre du véhicule")
    type_carburant: str = Field(..., description="Type de carburant")
    numero_chassis: str = Field(..., description="Numéro de châssis")
    nombre_cylindres: int = Field(..., description="Nombre de cylindres")
    puissance_fiscale: int = Field(..., description="Puissance fiscale en CV")
    restriction: str = Field(..., description="Restrictions éventuelles")
    identite: Identite
    adresse: Adresse
    valiadtion: str = Field(..., description="Date de validité au format JJ.MM.AAAA ou JJ/MM/AAAA")
    @validator("valiadtion")
    def check_date_format(cls, v):
        if not re.fullmatch(r"\d{2}[./]\d{2}[./]\d{4}", v):
            raise ValueError("La date doit être au format JJ.MM.AAAA ou JJ/MM/AAAA")
        return v.replace("/", ".")

