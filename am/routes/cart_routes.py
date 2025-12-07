from flask import Blueprint, jsonify, request
from am.models.cart_model import add_to_cart, remove_from_cart, get_cart

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart', methods=['GET'])
def view_cart():
    return jsonify(get_cart())
    
     
@cart_bp.route("/add", methods=["POST"])
def add_book_to_cart():
    """إضافة كتاب للسلة"""
    data = request.get_json()
    book_id = data.get("book_id")
    result = add_to_cart(book_id)
    return jsonify(result), result["status"] 

@cart_bp.route("/remove", methods=["POST"])  
def remove_book_from_cart():
    """حذف كتاب من السلة"""
    data = request.get_json()
    book_id = data.get("book_id")
    result = remove_from_cart(book_id)
    return jsonify(result), result["status"]
  
    
    
