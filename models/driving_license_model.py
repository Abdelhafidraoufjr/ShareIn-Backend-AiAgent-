from pydantic import BaseModel, Field, validator, model_validator
from typing import Literal
import re

ARABIC_LETTERS = r"\u0621-\u064A\u0660-\u0669"

class LangText(BaseModel):
    fr: str = Field(..., description="Texte en alphabet latin")
    ar: str = Field(..., description="Texte en alphabet arabe")

    @validator("fr")
    def fr_must_be_latin(cls, v):
        if not re.fullmatch(r"[A-Z0-9\s\-\.'']+", v):
            raise ValueError("Le texte FR doit n’utiliser que A-Z, 0-9, espaces, apostrophes, traits d’union ou points")
        return v

    @validator("ar")
    def ar_must_be_arabic(cls, v):
        v_clean = v.rstrip(". ").strip()
        if not re.fullmatch(rf"[{ARABIC_LETTERS}\s]+", v_clean):
            raise ValueError("Le texte AR doit n’utiliser que des lettres arabes et chiffres arabes-indiens")
        return v_clean

class Identite(BaseModel):
    nom: LangText
    prenom: LangText

class Naissance(BaseModel):
    date: str = Field(..., description="Date au format JJ.MM.AAAA ou JJ/MM/AAAA")
    lieu: LangText

    @validator("date")
    def check_date_format(cls, v):
        if not re.fullmatch(r"\d{2}[./]\d{2}[./]\d{4}", v):
            raise ValueError("La date doit être au format JJ.MM.AAAA ou JJ/MM/AAAA")
        return v.replace("/", ".")

class Permis(BaseModel):
    numero_permis: str = Field(..., description="Format N/MMMMMM ex. 55/193059")
    date_delivrance: str = Field(..., description="Date JJ.MM.AAAA ou JJ/MM/AAAA")
    date_expiration: str = Field(..., description="Date JJ.MM.AAAA ou JJ/MM/AAAA")
    categorie: str = Field(..., description="Catégorie du permis parmi: A1, A, B, C, D, E(B), E(C), E(D)")
    
    @validator("categorie")
    def check_categorie(cls, v):
        valid_categories = ["A1", "A", "B", "C", "D", "E(B)", "E(C)", "E(D)"]
        if v not in valid_categories:
            raise ValueError(f"La catégorie doit être l'une de ces valeurs : {', '.join(valid_categories)}")
        return v
        
    @validator("categorie")
    def check_categorie(cls, v):
        if not re.fullmatch(r"[A-Z0-9]+", v):
            raise ValueError("La catégorie doit n’utiliser que des lettres majuscules A-Z et chiffres 0-9")
        return v

    @validator("numero_permis")
    def check_numero_permis(cls, v):
        if not re.fullmatch(r"\d{1,2}/\d{6}", v):
            raise ValueError("Le numéro de permis doit suivre le format N/MMMMMM (ex. 55/193059)")
        return v

    @validator("date_delivrance", "date_expiration")
    def check_date_fields(cls, v):
        if not re.fullmatch(r"\d{2}[./]\d{2}[./]\d{4}", v):
            raise ValueError("La date doit être au format JJ.MM.AAAA ou JJ/MM/AAAA")
        return v.replace("/", ".")

    @model_validator(mode="after")
    def check_expiration_after_delivrance(cls, model):
        d1 = list(map(int, model.date_delivrance.split(".")))
        d2 = list(map(int, model.date_expiration.split(".")))
        if (d2[2], d2[1], d2[0]) <= (d1[2], d1[1], d1[0]):
            raise ValueError("La date d'expiration doit être postérieure à la date de délivrance")
        return model

class PermisData(BaseModel):
    permis: Permis
    identite: Identite
    naissance: Naissance
