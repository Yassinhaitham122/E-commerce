import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Cart.css";

interface CartItem {
  id: number;
  quantity: number;
  product: {
    id: number;
    name: string;
    img?: string;
  };
}

export default function Cart() {
  const navigate = useNavigate();
  const { token } = useAuth();
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    fetch("http://127.0.0.1:8000/orders/create_order_orders__post", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        setCartItems(data.items || []);
        setLoading(false);
      })
      .catch(console.error);
  }, [token]);

  const handleCheckout = () => {
    navigate("/checkout");
  };

  if (loading) return <p>Loading cart...</p>;

  return (
    <main className="cart-page">
      <h2>Your Cart</h2>
      {cartItems.length === 0 ? (
        <p>هنا هتبقى المنتجات اللي أضفتها.</p>
      ) : (
        <ul className="cart-list">
          {cartItems.map((item) => (
            <li key={item.id} className="cart-item">
              <img
                src={item.product.img || "/assets/shoe-blue.jpg"}
                alt={item.product.name}
                className="cart-img"
              />
              <div className="cart-info">
                <p>{item.product.name}</p>
                <p>Quantity: {item.quantity}</p>
              </div>
            </li>
          ))}
        </ul>
      )}
      <div className="cart-buttons">
        <button className="home-button" onClick={() => navigate("/")}>
          Home
        </button>
        {cartItems.length > 0 && (
          <button className="checkout-button" onClick={handleCheckout}>
            Checkout
          </button>
        )}
      </div>
    </main>
  );
}
