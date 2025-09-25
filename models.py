from sqlalchemy import Column, Integer, String, Float
from database import Base  # Import the declarative base from database.py

# Define the Item table in the database
class Item(Base):
    __tablename__ = "items"  # Name of the table in the database

    # Primary key column: unique identifier for each item
    id = Column(Integer, primary_key=True, index=True)

    # Name of the item
    # - Must be unique
    # - Indexed for faster search
    # - Cannot be null
    name = Column(String, unique=True, index=True, nullable=False)

    # Optional description of the item
    # Can be null if not provided
    description = Column(String, nullable=True)

    # Price of the item
    # Cannot be null
    price = Column(Float, nullable=False)

    # Quantity in stock
    # Defaults to 0 if not specified
    quantity = Column(Integer, default=0)
