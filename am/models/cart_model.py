from am.models.books_model import books

# السلة هتبقى عبارة عن list مؤقتة
cart = []

def add_to_cart(book_id):
    
    for book in books:
        if book['id'] == book_id:
            cart.append(book)
            return {"msg": f"✅ '{book['title']}' added to cart!", "status": 200}
    return {"msg": "❌ Book not found!", "status": 404}

def remove_from_cart(book_id):
    for book in cart:
        if book['id'] == book_id:
            cart.remove(book)
            return {"msg": f"✅ '{book['title']}' removed from cart!", "status": 200}
    return {"msg": "❌ Book not found in cart!", "status": 404}
  
def get_cart():
    return {"cart": cart,"count" : len(cart)} 