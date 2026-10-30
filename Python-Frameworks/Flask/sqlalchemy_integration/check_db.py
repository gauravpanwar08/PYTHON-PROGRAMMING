from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():

    with db.engine.connect() as connection:
        connection.exec_driver_sql("SELECT 1")

    print("PostgreSQL connection successful!")
    