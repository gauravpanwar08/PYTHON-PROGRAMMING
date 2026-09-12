# ============================================================
#                           INSERT
#
# insert()  → Creates an INSERT SQL statement
# values()  → Provides values for the columns
# execute() → Executes the INSERT statement
# commit()  → Makes the transaction permanent
# ============================================================


from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert

# SQLite Database URL

DATABASE_URL = "sqlite:///example.db"


# Create Engine

engine = create_engine(DATABASE_URL)


# Create Metadata

metadata = MetaData()


# Define Users Table

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String),
)


# Create Table

metadata.create_all(engine)


# Create INSERT Statement with Keyword arguments

stmt = insert(users).values(name="Gaurav", email="gaurav@example.com")

# Create INSERT Statement with Dictionary

stmt = insert(users).values({"name": "Ajay", "email": "ajay@example.com"})

# Create INSERT Statement with Multiple rows

stmt = insert(users).values(
    [
        {"name": "Gautam", "email": "gautam@example.com"},
        {"name": "Rahul", "email": "rahul@example.com"},
    ]
)


# Execute INSERT

with engine.connect() as connection:
    connection.execute(stmt)
    connection.commit()               # Commit the transaction to make the changes permanent


print("User inserted successfully")
