from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
import os
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/'.env')
class Settings(BaseModel):
    app_name:str=os.getenv('APP_NAME','PocketSmart AI')
    secret_key:str=os.getenv('SECRET_KEY','dev-secret-change-me')
    database_url:str=os.getenv('DATABASE_URL','sqlite:///' + str(BASE_DIR / 'pocketsmart.db'))
    gemini_api_key:str=os.getenv('GEMINI_API_KEY','')
    gemini_model:str=os.getenv('GEMINI_MODEL','gemini-2.5-flash')
    cors_origins:list[str]=[x.strip() for x in os.getenv('CORS_ORIGINS','http://127.0.0.1:8000,http://localhost:8000').split(',') if x.strip()]
    max_upload_mb:int=int(os.getenv('MAX_UPLOAD_MB','5'))
settings=Settings()
UPLOAD_DIR=BASE_DIR/'app'/'uploads'; UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
