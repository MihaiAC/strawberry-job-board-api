import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE = os.getenv("POSTGRES_DB")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

# postgresql+psycopg = "dialect"
DATABASE_URL = f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# TODO: How to get/mock these in conftest?
JWT_KEY = os.getenv("JWT_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRATION_TIME_MINUTES = os.getenv("JWT_EXPIRATION_TIME_MINUTES")
