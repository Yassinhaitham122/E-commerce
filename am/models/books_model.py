import datetime
import random

# دالة بتولد ID عشوائي لكل كتاب
def get_new_id():
    return random.getrandbits(28)

books = [
    {
        "id": 1,
        "title": "The lord of the Rings",   
        "author": "J.R.R. Tolkien",
        "price": 250,
        "imageUrl": "https://example.com/images/61215351.jpg",
        "description": "fantasy novel"
        
        
    },    {
        
        "id": 2,
        "title": "rich dad poor dad",
        "author": "Robert T. Kiyosaki",
        "price": 180,
        "imageUrl": "https://example.com/images/download.jpg",
        "description": "fantasy novel"
        
        
    }
    
    
    
]