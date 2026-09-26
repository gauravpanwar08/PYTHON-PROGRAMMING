from sqlalchemy import create_engine, MetaData


# Create engine
engine = create_engine("sqlite:///employee_management.db")

# Create metadata
metadata = MetaData()
