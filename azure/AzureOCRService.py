import os
import base64
from typing import Optional
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()


class AzureOCRService:
    def __init__(self):
        endpoint = os.getenv("AZURE_OCR_ENDPOINT")
        key = os.getenv("AZURE_OCR_KEY")
        if not endpoint or not key:
            raise ValueError(
                "⚠️ AZURE_OCR_ENDPOINT et AZURE_OCR_KEY doivent être définis dans .env")
        self.client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key))

    def extract_text(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            poller = self.client.begin_analyze_document("prebuilt-read", f)
        result = poller.result()

        text = []
        for page in result.pages:
            for line in page.lines:
                text.append(line.content)
        return "\n".join(text)


