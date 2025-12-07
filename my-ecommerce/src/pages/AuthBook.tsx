// src/pages/AuthBook.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext"; // تأكد من المسار الصحيح
import "./AuthBook.css";

export default function AuthBook() {
  const [flipped, setFlipped] = useState(false); // false = login, true = signup
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const { login } = useAuth(); // لازم AuthProvider يكون ملفوف حوالين App

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (flipped) {
        // SIGNUP => JSON to /auth/signup
        const res = await fetch("http://127.0.0.1:8000/auth/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, email, password }),
        });

        const data = await res.json();
        if (!res.ok) {
          setError(data.detail || data.message || JSON.stringify(data) || "Signup failed");
        } else {
          // store token via context
          login(data.access_token);
          navigate("/");
        }
      } else {
        // LOGIN => OAuth2 form-urlencoded to /auth/token
        const formBody = new URLSearchParams();
        formBody.append("grant_type", "password");
        formBody.append("username", email); // backend expects username field (email)
        formBody.append("password", password);

        const res = await fetch("http://127.0.0.1:8000/auth/token", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: formBody.toString(),
        });

        const data = await res.json();
        if (!res.ok) {
          setError(data.detail || data.message || JSON.stringify(data) || "Login failed");
        } else {
          login(data.access_token);
          navigate("/");
        }
      }
    } catch (err) {
      console.error(err);
      setError("Network error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="book-wrapper">
      <div className={`book ${flipped ? "flipped" : ""}`}>
        {/* Login page */}
        <div className="page page-front">
          <h2 className="auth-title">Login</h2>
          {error && <p className="error-msg">{error}</p>}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleSubmit} disabled={loading}>
            {loading ? "Please wait..." : "Login"}
          </button>
          <p style={{ cursor: "pointer", marginTop: 12 }} onClick={() => setFlipped(true)}>
            Go to Sign Up →
          </p>
        </div>

        {/* Signup page */}
        <div className="page page-back">
          <h2 className="auth-title">Sign Up</h2>
          {error && <p className="error-msg">{error}</p>}
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleSubmit} disabled={loading}>
            {loading ? "Please wait..." : "Sign Up"}
          </button>
          <p style={{ cursor: "pointer", marginTop: 12 }} onClick={() => setFlipped(false)}>
            ← Back to Login
          </p>
        </div>
      </div>
    </div>
  );
}
