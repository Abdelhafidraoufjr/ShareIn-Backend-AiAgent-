from pydantic import BaseModel, Field, validator
from typing import Optional
import re


class LangText(BaseModel):
    fr: str
    ar: str

    @validator('fr')
    def validate_french_text(cls, v):
        arabic_chars = sum(1 for c in v if '\u0600' <= c <= '\u06FF')
        if arabic_chars > len(v) * 0.3:  # Plus de 30% de caractères arabes
            raise ValueError(
                f"Le champ français contient trop de caractères arabes: {v}")
        return v

    @validator('ar')
    def validate_arabic_text(cls, v):
        arabic_chars = sum(1 for c in v if '\u0600' <= c <= '\u06FF')
        if arabic_chars == 0 and len(v) > 0:
            raise ValueError(
                f"Le champ arabe ne contient aucun caractère arabe: {v}")
        return v


class Identite(BaseModel):
    nom: LangText
    prenom: LangText


class Naissance(BaseModel):
    date: str = Field(..., description="Date au format DD.MM.YYYY")
    lieu: LangText

    @validator('date')
    def validate_date_format(cls, v: str) -> str:
        """
        Valide et reformate automatiquement la date.
        Accepte :
        - DD/MM/YYYY → DD.MM.YYYY
        - DD-YYYY → DD.01.YYYY
        """
        v = v.replace("-", ".").replace("/", ".")

        if re.match(r'^\d{1,2}\.\d{4}$', v):
            day, year = v.split(".")
            v = f"{int(day):02d}.01.{year}"

        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', v):
            raise ValueError(f"Date must be in DD.MM.YYYY format, got '{v}'")
        return v


class Adresse(LangText):
    pass


class Parent(BaseModel):
    pere: LangText
    mere: LangText


class EtatCivil(BaseModel):
    numero_etat_civil: Optional[str] = Field(
        None, description="Numéro d'état civil (format: XX/YYYY, XXX/YYYY, etc.)"
    )


@validator('numero_etat_civil')
def validate_and_format_etat_civil(cls, v: Optional[str]) -> Optional[str]:
    if not v:
        return v

    # Normalisation classique
    match_plain = re.match(r'^(\d{2,4})(\d{4})$', v)
    if match_plain:
        return f"{match_plain.group(1)}/{match_plain.group(2)}"

    v = re.sub(r'^(\d+)-(\d{4})$', r'\1/\2', v)
    v = re.sub(r'^(\d{2,4}/\d{4}).*$', r'\1', v)

    # Vérifier si c’est un vrai numéro d’état civil
    if re.match(r'^\d{2,4}/\d{4}$', v):
        return v

    # ✅ Si c’est un code genre CAN 279975 → on l’ignore
    if v.startswith("CAN"):
        return None

    raise ValueError(
        f"Numéro état civil format not recognized: {v}. "
        "Expected formats: XX/YYYY, XXX/YYYY, XXXX/YYYY, XXYYYY, or XX-YYYY"
    )


class CINData(BaseModel):
    cin: str = Field(..., description="Numéro de la carte nationale")
    identite: Identite
    naissance: Naissance
    adresse: Adresse = Field(..., description="Adresse en français et arabe")
    sexe: str = Field(..., description="Sexe de la personne (M/F)")
    validite: str = Field(...,
                          description="Date de validité au format DD.MM.YYYY")
    parents: Parent
    etat_civil: EtatCivil

    @validator('cin')
    def validate_cin(cls, v: str) -> str:
        """
        Extrait et valide le CIN : format flexible pour cartes marocaines
        Accepte différents formats comme: A123456, AB123456, OPI7KJEG, etc.
        """
        v = v.strip().upper()

        patterns = [
            r'[A-Z]{1,3}\d{3,6}[A-Z]{0,3}',
            r'[A-Z]{1,2}\d{3,6}',
            r'\d{6,8}',
            r'[A-Z0-9]{6,10}'
        ]

        for pattern in patterns:
            match = re.search(pattern, v)
            if match:
                return match.group(0)

        if len(v) >= 6 and len(v) <= 10 and v.isalnum():
            return v

        raise ValueError(f"CIN format invalid: {v}")

    @validator('sexe')
    def validate_sexe(cls, v: str) -> str:
        if v not in ['M', 'F']:
            raise ValueError("Sexe must be 'M' or 'F'")
        return v

    @validator('validite')
    def validate_validite(cls, v: str) -> str:
        v = v.replace("-", ".").replace("/", ".")
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', v):
            raise ValueError(
                f"Validité must be in DD.MM.YYYY format, got '{v}'")
        return v
