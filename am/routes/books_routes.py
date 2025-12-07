from flask import Blueprint, render_template, redirect, url_for, session
from am.models.books_model import books

books_bp = Blueprint('books_bp', __name__)


@books_bp.route('/books')
def show_books():
    return render_template('books.html', books=books)


    

@books_bp.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    if 'cart' not in session:
        session['cart'] = []
    
    # Find the book by its ID
    book = next((b for b in books if b['id'] == book_id), None)
    
    if book:
        cart = session.get('cart', [])
        cart.append(book)
        session['cart'] = cart
    return redirect(url_for('books_bp.show_books'))
       