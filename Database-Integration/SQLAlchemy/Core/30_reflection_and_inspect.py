# ===============================================================================================================
#                         REFLECTION & INSPECT

# REFLECTION → Automatically loads existing database schema into SQLAlchemy.
# INSPECT    → Retrieves and examines database schema information.
#
# - inspect()                         : Provides methods to inspect and retrieve database schema information.
# - get_table_names()                 : Returns the names of tables in the database.
# - get_columns()                     : Returns column information of a table.
# - get_pk_constraint()               : Returns primary key constraint information of a table.
# - get_foreign_keys()                : Returns foreign key information of a table.
# - get_indexes()                     : Returns index information of a table.
# - get_unique_constraints()          : Returns unique constraint information of a table.
# - Table(..., autoload_with=engine)  : Loads an existing table's structure automatically from the database.
# - MetaData.reflect()                : Loads database table definitions into MetaData automatically.
# ===============================================================================================================

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
    Index,
    inspect,
    select,
)


# Create engine
engine = create_engine("sqlite:///reflection.db", echo=True)


# ===============================================================================================================
# PART 1 — CREATE EXISTING DATABASE SCHEMA
# ===============================================================================================================

metadata = MetaData()


# Create departments table
departments = Table(
    "departments",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False, unique=True),
)


# Create employees table
employees = Table(
    "employees",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("email", String(100), nullable=False),
    Column(
        "department_id",
        Integer,
        ForeignKey("departments.id"),
    ),

    UniqueConstraint("email", name="uq_employees_email"),
)


# Create index
Index(
    "ix_employees_name",
    employees.c.name,
)


# Create tables
metadata.create_all(engine)


# Insert sample data
with engine.begin() as connection:

    connection.execute(
        departments.insert(),
        [
            {"id": 1, "name": "IT"},
            {"id": 2, "name": "HR"},
        ],
    )

    connection.execute(
        employees.insert(),
        [
            {
                "id": 1,
                "name": "Gaurav",
                "email": "gaurav@example.com",
                "department_id": 1,
            },
            {
                "id": 2,
                "name": "Priya",
                "email": "priya@example.com",
                "department_id": 2,
            },
        ],
    )


# ===============================================================================================================
# PART 2 — INSPECT DATABASE
# ===============================================================================================================

inspector = inspect(engine)


# Get table names
print("\nTABLES:")
print(inspector.get_table_names())


# Get columns
print("\nEMPLOYEES COLUMNS:")
for column in inspector.get_columns("employees"):
    print(column)


# Get primary key
print("\nEMPLOYEES PRIMARY KEY:")
print(inspector.get_pk_constraint("employees"))


# Get foreign keys
print("\nEMPLOYEES FOREIGN KEYS:")
print(inspector.get_foreign_keys("employees"))


# Get indexes
print("\nEMPLOYEES INDEXES:")
print(inspector.get_indexes("employees"))


# Get unique constraints
print("\nEMPLOYEES UNIQUE CONSTRAINTS:")
print(inspector.get_unique_constraints("employees"))


# ===============================================================================================================
# PART 3 — REFLECT SINGLE TABLE
# ===============================================================================================================

reflected_metadata = MetaData()

reflected_employees = Table(
    "employees",
    reflected_metadata,
    autoload_with=engine,
)


# Access reflected columns
print("\nREFLECTED COLUMNS:")
print(reflected_employees.c.keys())


# Query reflected table
stmt = select(
    reflected_employees.c.id,
    reflected_employees.c.name,
    reflected_employees.c.email,
)


with engine.connect() as connection:

    result = connection.execute(stmt)

    print("\nREFLECTED TABLE DATA:")

    for row in result:
        print(row)


# ===============================================================================================================
# PART 4 — REFLECT ALL TABLES
# ===============================================================================================================

all_metadata = MetaData()

all_metadata.reflect(bind=engine)


print("\nREFLECTED TABLES:")
print(list(all_metadata.tables.keys()))


# Access reflected table from metadata
reflected_departments = all_metadata.tables["departments"]

print("\nDEPARTMENTS COLUMNS:")
print(reflected_departments.c.keys())
