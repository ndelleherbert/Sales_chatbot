from sqlalchemy.orm import Session
import crud, models

def chatbot_response(db: Session, message: str):
    message = message.lower()

    # If user asks for all items
    if any(keyword in message for keyword in ["list", "show", "items", "products", "all"]):
        items = db.query(models.Item).all()
        if not items:
            return "No items are currently available."
        response = "Here are the available items:\n"
        for item in items:
            response += f"- {item.name}: ${item.price}, Qty: {item.quantity}\n"
        return response.strip()

    # Otherwise, search for a specific item
    words = message.split()
    for word in words:
        item = crud.get_item_by_name(db, word)
        if item:
            if "price" in message:
                return f"The price of {item.name} is ${item.price}."
            elif "how many" in message or "stock" in message or "quantity" in message:
                return f"We currently have {item.quantity} units of {item.name} in stock."
            elif "description" in message or "tell me about" in message:
                return f"{item.name}: {item.description or 'No description available.'}"
            else:
                return f"{item.name} costs ${item.price}, quantity: {item.quantity}. Description: {item.description or 'N/A'}"

    return "Sorry, I couldn't find that item. Try asking about another product or say 'list items'."
