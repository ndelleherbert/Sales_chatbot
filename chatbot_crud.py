from sqlalchemy.orm import Session
import crud, models

def chatbot_response(db: Session, message: str):
    """
    Generate a response for the chatbot based on user input.

    Parameters:
    - db (Session): SQLAlchemy database session to query items.
    - message (str): The user's input message.

    Returns:
    - str: Chatbot's response.
    """

    # 1️⃣ Normalize the message: make it lowercase to ignore case sensitivity
    message = message.lower()

    # 2️⃣ Check if the user wants a list of all items
    if any(keyword in message for keyword in ["list", "show", "items", "products", "all"]):
        # Query all items from the database
        items = db.query(models.Item).all()
        
        if not items:  # No items found
            return "No items are currently available."
        
        # Build the response string listing all items
        response = "Here are the available items:\n"
        for item in items:
            response += f"- {item.name}: ${item.price}, Qty: {item.quantity}\n"
        return response.strip()  # Remove trailing newline

    # 3️⃣ If user did not ask for all items, try to find a specific item
    words = message.split()  # Split the message into individual words
    for word in words:
        # Search the database for an item matching the word
        item = crud.get_item_by_name(db, word)
        if item:
            # 4️⃣ Check user intent based on keywords in the message

            # User wants the price of the item
            if "price" in message:
                return f"The price of {item.name} is ${item.price}."

            # User wants to know quantity/stock
            elif "how many" in message or "stock" in message or "quantity" in message:
                return f"We currently have {item.quantity} units of {item.name} in stock."

            # User wants the item description
            elif "description" in message or "tell me about" in message:
                return f"{item.name}: {item.description or 'No description available.'}"

            # Default response: show all information
            else:
                return (f"{item.name} costs ${item.price}, quantity: {item.quantity}. "
                        f"Description: {item.description or 'N/A'}")

    # 5️⃣ If no item is found, return a friendly fallback message
    return "Sorry, I couldn't find that item. Try asking about another product or say 'list items'."
