# ================================================================================
#                    SQLALCHEMY ORM — POSTGRESQL SPECIFIC FEATURES
#
# PostgreSQL provides advanced database features that can be used through 
# SQLAlchemy ORM using the PostgreSQL dialect.
#
# Important PostgreSQL Features:
#
# JSONB          - Stores and queries JSON data efficiently
# ARRAY          - Stores PostgreSQL array values
# UUID           - Stores UUID values
# ENUM           - Stores predefined values
# GIN            - Specialized index for JSONB, ARRAY and similar data
# RETURNING      - Returns inserted/updated database values
# ON CONFLICT    - Handles duplicate records and upserts
#
# PostgreSQL-specific types are imported from:
# sqlalchemy.dialects.postgresql
# ================================================================================


from uuid import UUID, uuid4

from sqlalchemy.dialects.postgresql import JSONB, ARRAY, UUID as PG_UUID

from sqlalchemy import (
    JSON,
    Enum,
    Index,
    String,
    URL,
    create_engine,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

# Create PostgreSQL connection URL
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="aura123",
    host="localhost",
    port=5432,
    database="sqlalchemy_db",
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


# Create Declarative Base
class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "orm_postgresql_products"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    name: Mapped[str] = mapped_column(String(100))

    # PostgreSQL JSONB
    metadata_json: Mapped[dict] = mapped_column(JSONB)

    # PostgreSQL ARRAY
    tags: Mapped[list[str]] = mapped_column(ARRAY(String))

    # PostgreSQL ENUM
    status: Mapped[str] = mapped_column(
        Enum(
            "active",
            "inactive",
            "out_of_stock",
            name="product_status",
        )
    )


# PostgreSQL-specific GIN indexes
Index(
    "ix_product_metadata_json",
    Product.metadata_json,
    postgresql_using="gin",
)

Index(
    "ix_product_tags",
    Product.tags,
    postgresql_using="gin",
)


# Create tables
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)


with SessionLocal() as session:

    # Add sample products
    product1 = Product(
        name="FastAPI Course",
        metadata_json={
            "category": "backend",
            "level": "advanced",
        },
        tags=["Python", "FastAPI", "SQLAlchemy"],
        status="active",
    )

    product2 = Product(
        name="Python Course",
        metadata_json={
            "category": "programming",
            "level": "beginner",
        },
        tags=["Python", "Programming"],
        status="active",
    )

    session.add_all([product1, product2])
    session.commit()

    # ---------------------------------------------------------------------
    # JSONB
    # JSONB stores structured JSON data inside PostgreSQL.
    # ---------------------------------------------------------------------

    stmt = select(Product).where(
        Product.metadata_json["category"].as_string() == "backend"
    )

    products = session.scalars(stmt).all()

    for product in products:
        print(product.name)

    # ---------------------------------------------------------------------
    # ARRAY
    # ARRAY stores PostgreSQL array values.
    # ---------------------------------------------------------------------

    stmt = select(Product).where(Product.tags.contains(["Python"]))

    products = session.scalars(stmt).all()

    for product in products:
        print(product.name)

    # ---------------------------------------------------------------------
    # UUID
    # UUID provides globally unique identifiers.
    # ---------------------------------------------------------------------

    product = session.get(Product, product1.id)

    print(product.id)

    # ---------------------------------------------------------------------
    # ENUM
    # ENUM restricts a column to predefined values.
    # ---------------------------------------------------------------------

    stmt = select(Product).where(Product.status == "active")

    active_products = session.scalars(stmt).all()

    for product in active_products:
        print(product.name)

    # ---------------------------------------------------------------------
    # PostgreSQL GIN Index
    # GIN is useful for searching JSONB and ARRAY data.
    # ---------------------------------------------------------------------

    print(Product.__table__.indexes)

    # ---------------------------------------------------------------------
    # PostgreSQL ON CONFLICT
    # PostgreSQL can handle duplicate records using ON CONFLICT.
    # This feature is mainly used through the PostgreSQL insert construct.
    # ---------------------------------------------------------------------

    from sqlalchemy.dialects.postgresql import insert

    stmt = insert(Product).values(
        id=product1.id,
        name="FastAPI Course Updated",
        metadata_json={
            "category": "backend",
            "level": "advanced",
        },
        tags=["Python", "FastAPI", "SQLAlchemy"],
        status="active",
    )

    stmt = stmt.on_conflict_do_update(
        index_elements=[Product.id],
        set_={
            "name": stmt.excluded.name,
            "metadata_json": stmt.excluded.metadata_json,
            "tags": stmt.excluded.tags,
            "status": stmt.excluded.status,
        },
    )

    session.execute(stmt)
    session.commit()

    # ---------------------------------------------------------------------
    # RETURNING
    # PostgreSQL can return database-generated values after INSERT/UPDATE.
    # ---------------------------------------------------------------------

    stmt = (
        insert(Product)
        .values(
            name="PostgreSQL Course",
            metadata_json={
                "category": "database",
                "level": "advanced",
            },
            tags=["PostgreSQL", "SQLAlchemy"],
            status="active",
        )
        .returning(Product.id, Product.name)
    )

    result = session.execute(stmt)

    returned_product = result.one()

    print(returned_product.id)
    print(returned_product.name)

    session.commit()
