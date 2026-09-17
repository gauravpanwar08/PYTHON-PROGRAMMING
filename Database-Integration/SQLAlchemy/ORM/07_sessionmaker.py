# ==============================================================================================================
#                SQLALCHEMY ORM — SESSIONMAKER
#
# sessionmaker is a factory used to create configured Session objects with predefined configuration.
# Purpose : Reuse the same configuration for multiple Session objects without repeating the configuration code.
#
# Important Parameters:
#
# bind             - Engine/connection that Sessions will use.
# class_           - Session class to create. Default is Session.
# autoflush        - Controls automatic flushing of pending changes.
# expire_on_commit - Controls expiration of object state after commit.
# info             - Optional information dictionary for the Session.
# ================================================================================================================


from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker


# Create PostgreSQL connection URL
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="aura123",
    host="localhost",
    port=5432,
    database="sqlalchemy_db",
)


# Create Engine

engine = create_engine(
    DATABASE_URL,
    echo=True,
)


# ------------------------------------------------------------
# sessionmaker - Create a Session factory
# ------------------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
)


# ------------------------------------------------------------
# Create Session
# ------------------------------------------------------------

with SessionLocal() as session:

    print("Session created:", session)
    print("Session type:", type(session))

    # Database operations will be performed using this session


# ------------------------------------------------------------
# Multiple Sessions - Each SessionLocal() creates a new Session
# ------------------------------------------------------------

session1 = SessionLocal()
session2 = SessionLocal()

print("Session 1:", session1)
print("Session 2:", session2)

print("Are they the same object?", session1 is session2)

session1.close()
session2.close()


# ------------------------------------------------------------
# sessionmaker parameters
# ------------------------------------------------------------

ConfiguredSession = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
    info={"application": "SQLAlchemy ORM Learning"},
)


with ConfiguredSession() as session:
    
    print("\nConfigured Session:", session)
    print("Session info:", session.info)
    print("Autoflush:", session.autoflush)
    print("Expire on commit:", session.expire_on_commit)
