from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


EMAIL = os.getenv("EMAIL")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_PASS")



if __name__=="__main__":
    print(ROOT)



"""
python3 -m src.settings

"""