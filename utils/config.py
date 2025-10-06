import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    AZURE_OCR_ENDPOINT = os.getenv("AZURE_OCR_ENDPOINT")
    AZURE_OCR_KEY = os.getenv("AZURE_OCR_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    TOKEN_EXPIRATION_HOURS = int(os.getenv("TOKEN_EXPIRATION_HOURS", 24))
    
