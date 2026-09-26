# ------------ Raw SQL Integration -----------------

from sqlalchemy import text
from database import engine


def get_database_version():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT sqlite_version()")
        )
        return result.scalar()
    
print(get_database_version())


# ---------------------- Database Inspection --------------

from sqlalchemy import inspect
from database import engine


def show_database_info():
    inspector = inspect(engine)

    print("Tables:", inspector.get_table_names())

    for table_name in inspector.get_table_names():
        print(f"\n{table_name}")
        print("Columns:", inspector.get_columns(table_name))
        
