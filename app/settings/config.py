import os
from dotenv import load_dotenv

load_dotenv()

# In a non-toy example, would have to split those envs.
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE = os.getenv("POSTGRES_DB")
TEST_DATABASE = os.getenv("POSTGRES_TEST_DB")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

# postgresql+psycopg = "dialect"
url_prefix = f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/"
DATABASE_URL = url_prefix + DATABASE
TEST_DATABASE_URL = url_prefix + TEST_DATABASE
