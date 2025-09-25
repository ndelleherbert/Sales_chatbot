from pydantic import BaseModel
from typing import Optional

# Base schema for Item: defines the core fields shared across other schemas
class ItemBase(BaseModel):
    name: str                   # Name of the item (required)
    description: Optional[str]  # Optional description; can be None
    price: float                # Price of the item (required)
    quantity: int               # Quantity in stock (required)

# Schema for creating a new item
# Inherits all fields from ItemBase
# Used when a user submits data to create a new item
class ItemCreate(ItemBase):
    pass

# Schema for reading an item (response schema)
# Inherits all fields from ItemBase and adds 'id' field
# Used when returning data from the database to the client
class ItemRead(ItemBase):
    id: int                     # Auto-generated database ID of the item

    # Pydantic v2 update:
    # 'orm_mode' from v1 has been renamed to 'from_attributes' in v2
    # This allows the model to read data directly from SQLAlchemy ORM objects
    model_config = {
        "from_attributes": True
    }
