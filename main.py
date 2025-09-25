from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud, chatbot_crud, database

# Import models to ensure they are registered with Base
print("Creating database tables...")
models.Base.metadata.create_all(bind=database.engine)  # Use models.Base, not database.Base

# Initialize FastAPI app
app = FastAPI(title="Simple Store Chatbot")

# --- Items Endpoints ---
@app.post("/items", response_model=schemas.ItemRead)
def create_item(item: schemas.ItemCreate, db: Session = Depends(database.get_db)):
    """
    Create a new item in the database.
    - item: ItemCreate schema from client
    - db: database session
    Returns the created item with its ID (ItemRead schema).
    """
    return crud.create_item(db, item)

# --- Chatbot Endpoints ---
@app.post("/chat")
def chat(message: str, db: Session = Depends(database.get_db)):
    """
    Send a message to the chatbot.
    - message: string from client
    - db: database session
    Returns chatbot response as a JSON object.
    """
    response = chatbot_crud.chatbot_response(db, message)
    return {"response": response}
