# ==========================================================================
#                              METADATA
#
# MetaData → Stores database schema information in Python/SQLAlchemy objects
#            also reduces writing manual SQL statements.
# MetaData tracks Table, Column and Constraint objects, etc.

# schema   → Defines the default database schema
# naming_convention → Defines automatic names for constraints
# ===========================================================================


from sqlalchemy import MetaData

# Create Metadata

metadata = MetaData()

print("Metadata created successfully")
print(metadata)
