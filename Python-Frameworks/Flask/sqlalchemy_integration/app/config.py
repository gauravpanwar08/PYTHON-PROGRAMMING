import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


class Config:

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME")
    ).render_as_string(hide_password=False)

    SQLALCHEMY_TRACK_MODIFICATIONS = False