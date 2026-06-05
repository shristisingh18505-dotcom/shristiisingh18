import os
from dotenv import load_dotenv
load_dotenv()

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB = "sqlite:///" + os.path.join(BASEDIR, "edutrack.db")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", DEFAULT_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PDF_OUTPUT = os.path.join(BASEDIR, "generated_pdfs")
    WTF_CSRF_TIME_LIMIT = None
