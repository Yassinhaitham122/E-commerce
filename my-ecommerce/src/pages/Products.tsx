import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import "./products.css";

interface Product {
  id: number;
  name: string;
  img?: string;
}

interface ProductsProps {
  searchQuery?: string;
  token?: string | null;
}

export default function Products({ searchQuery = "", token }: ProductsProps) {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const { token: authToken } = useAuth(); // token من الـ context

  useEffect(() => {
    fetch("http://127.0.0.1:8000/products", {
      headers: {
        Authorization: authToken ? `Bearer ${authToken}` : "",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch products:", err);
        setLoading(false);
      });
  }, [authToken]);

  const handleAddToCart = async (productId: number) => {
    if (!authToken) {
      alert("Please login first!");
      return;
    }
    try {
      const res = await fetch("http://127.0.0.1:8000/orders/create_order_orders__post", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authToken}`,
        },
        body: JSON.stringify({ product_id: productId }),
      });
      if (!res.ok) throw new Error("Failed to add to cart");
      alert("Product added to cart!");
    } catch (err) {
      console.error(err);
      alert("Error adding product to cart");
    }
  };

  const filteredProducts = products.filter((product) =>
    product.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) return <p>Loading products...</p>;

  return (
    <section className="products">
      <h2 className="products-title">Our Products</h2>
      <div className="products-grid">
        {filteredProducts.map((product) => (
          <div key={product.id} className="product-card">
            <img
              src={product.img || "/assets/shoe-blue.jpg"}
              alt={product.name}
              className="product-img"
            />
            <h3 className="product-name">{product.name}</h3>
            <button onClick={() => handleAddToCart(product.id)}>
              Add to Cart
            </button>
          </div>
        ))}
      </div>
    </section>
  );
}
