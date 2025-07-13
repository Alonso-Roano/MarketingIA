import os
from dotenv import load_dotenv

load_dotenv()

AI21_API_URL = os.getenv("AI21_API_URL")
AI21_API_TOKEN_1 = os.getenv("AI21_API_TOKEN_1")
AI21_API_TOKEN_2 = os.getenv("AI21_API_TOKEN_2")
AI21_API_TOKEN_3 = os.getenv("AI21_API_TOKEN_3")
TOKEN_URL = os.getenv("TOKEN_URL")

# MinIO Configuración
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"