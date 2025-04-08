import os
from dotenv import load_dotenv

# Decide what .env file to load.
env_file = os.environ.get("ENV_FILE", ".env")
load_dotenv(env_file, override=True)

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE = os.getenv("POSTGRES_DB")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

# postgresql+psycopg = "dialect"
DATABASE_URL = f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

JWT_KEY = os.getenv("JWT_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRATION_TIME_MINUTES = int(os.getenv("JWT_EXPIRATION_TIME_MINUTES"))
