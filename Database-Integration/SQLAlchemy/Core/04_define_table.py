# ============================================================
#                       TABLE
#
# Table       → Represents a database table in SQLAlchemy
# Column()    → Defines a table column
# Integer     → Integer data type
# String      → String/VARCHAR data type
# primary_key → Defines the primary key
#
# MetaData stores and tracks the Table object
# ============================================================


from sqlalchemy import MetaData, Table, Column, Integer, String

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


print("Table defined successfully")
print(users)
