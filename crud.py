from sqlalchemy.orm import Session
import models, schemas

def create_item(db: Session, item: schemas.ItemCreate):
    """
    Create a new item in the database.

    Steps:
    1. Convert the Pydantic model (item) to a dictionary using `model_dump()` 
       (Pydantic v2) so it can be used as keyword arguments for the SQLAlchemy model.
       Example: {"name": "Phone", "description": "Smartphone", "price": 500, "quantity": 10}
    2. Create a SQLAlchemy Item object with these values.
    3. Add the object to the database session using `db.add()`.
    4. Commit the session with `db.commit()` to permanently save the item.
    5. Refresh the object with `db.refresh()` to load auto-generated fields like `id`.
    6. Return the newly created Item object.
    """
    db_item = models.Item(**item.model_dump())  # ✅ Pydantic v2
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item_by_name(db: Session, name: str):
    """
    Retrieve an item from the database by name.

    Steps:
    1. Start a query on the Item table: `db.query(models.Item)`.
    2. Filter rows where the `name` column matches the input name using `ilike` 
       for case-insensitive and partial matching.
       - `%{name}%` allows partial matches (e.g., "phone" matches "Smartphone").
    3. Use `.first()` to return the first matching record or None if not found.
    4. This function is used by the chatbot to fetch items dynamically based on user input.
    """
    return db.query(models.Item).filter(models.Item.name.ilike(f"%{name}%")).first()
