# ================================================================================================
#                    SQLALCHEMY ORM — MYSQL SPECIFIC FEATURES
#
# MySQL-specific features are database capabilities exposed through SQLAlchemy's MySQL dialect.
#
# Important MySQL Features:
#
# JSON                  - Stores JSON data
# ENUM                  - Stores predefined values
# AUTO_INCREMENT        - Automatically generates integer IDs
# UNSIGNED              - Stores only non-negative numeric values
# ON DUPLICATE KEY      - Handles duplicate-key inserts
# MySQL-specific types  - Provides MySQL-specific column definitions
#
# MySQL-specific types are imported from:
# sqlalchemy.dialects.mysql
# ==================================================================================================


from sqlalchemy import (
    Enum,
    Index,
    JSON,
    String,
    URL,
    create_engine,
    select,
)
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)


# Create MySQL connection URL
DATABASE_URL = URL.create(
    drivername="mysql+mysqldb",
    username="root",
    password="aura@123",
    host="localhost",
    port=3306,
    database="sqlalchemy_db",
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


# Create Declarative Base
class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "orm_mysql_products"

    # MySQL AUTO_INCREMENT
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # MySQL JSON
    metadata_json: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    # MySQL ENUM
    status: Mapped[str] = mapped_column(
        Enum(
            "active",
            "inactive",
            "out_of_stock",
            name="product_status",
        ),
        nullable=False,
    )

    # MySQL UNSIGNED INTEGER
    stock: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        nullable=False,
    )


# Create index
Index(
    "ix_mysql_product_name",
    Product.name,
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
        status="active",
        stock=10,
    )

    product2 = Product(
        name="Python Course",
        metadata_json={
            "category": "programming",
            "level": "beginner",
        },
        status="active",
        stock=20,
    )

    session.add_all([product1, product2])
    session.commit()


    # ----------------------------------------------------------------------
    # JSON
    # JSON stores structured JSON data inside MySQL.
    # ----------------------------------------------------------------------
    
    stmt = select(Product).where(
        Product.metadata_json["category"].as_string() == "backend"
    )

    products = session.scalars(stmt).all()

    for product in products:
        print(product.name)


    # ----------------------------------------------------------------------
    # ENUM
    # ENUM restricts a column to predefined values.
    # ----------------------------------------------------------------------
    
    stmt = select(Product).where(
        Product.status == "active"
    )

    active_products = session.scalars(stmt).all()

    for product in active_products:
        print(product.name)


    # ----------------------------------------------------------------------
    # AUTO_INCREMENT
    # MySQL automatically generates the integer primary key.
    # ----------------------------------------------------------------------
    
    print(product1.id)
    print(product2.id)


    # ----------------------------------------------------------------------
    # UNSIGNED
    # UNSIGNED prevents negative numeric values.
    # ----------------------------------------------------------------------
    
    print(product1.stock)


    # ----------------------------------------------------------------------
    # MySQL Index
    # Indexes can improve searches on frequently queried columns.
    # ----------------------------------------------------------------------
    
    print(Product.__table__.indexes)


    # ----------------------------------------------------------------------
    # ON DUPLICATE KEY UPDATE
    # MySQL can update an existing row when a duplicate key occurs.
    # ----------------------------------------------------------------------
    
    from sqlalchemy.dialects.mysql import insert

    stmt = insert(Product).values(
        id=product1.id,
        name="FastAPI Course Updated",
        metadata_json={
            "category": "backend",
            "level": "advanced",
        },
        status="active",
        stock=15,
    )

    stmt = stmt.on_duplicate_key_update(
        name=stmt.inserted.name,
        metadata_json=stmt.inserted.metadata_json,
        status=stmt.inserted.status,
        stock=stmt.inserted.stock,
    )

    session.execute(stmt)
    session.commit()


    # Check updated product
    product = session.get(Product, product1.id)

    print(product.name)
    print(product.stock)
