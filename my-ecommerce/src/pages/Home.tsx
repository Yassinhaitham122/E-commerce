import { useState } from "react";
import Hero from "../components/Hero";
import Products from "./Products";
import Footer from "../components/Footer";
import { useAuth } from "../context/AuthContext";

import "./home.css";
import "../components/Hero.css";

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const { token } = useAuth();

  return (
    <main>
      <Hero />

      <section className="search-section">
        <input
          type="text"
          placeholder="Search products..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
      </section>

      <section id="products-section">
        <Products searchQuery={searchQuery} token={token} />
      </section>

      <Footer />
    </main>
  );
}
