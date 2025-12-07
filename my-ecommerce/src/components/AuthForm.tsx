import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./AuthBook.css";

function AuthBook() {
  const [flipped, setFlipped] = useState(false); // false = login, true = signup
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // تحديث المسار حسب الصفحة
  useEffect(() => {
    navigate(flipped ? "/signup" : "/login", { replace: true });
  }, [flipped, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const endpoint = flipped ? "signup" : "login";
      const res = await fetch(`http://127.0.0.1:8000/auth/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Something went wrong");
      } else {
        console.log(`${endpoint} success:`, data);
        // مثال: تخزين التوكن لو موجود
        if (data.access_token) {
          localStorage.setItem("token", data.access_token);
        }
        // مثال: إعادة التوجيه للصفحة الرئيسية بعد تسجيل الدخول/التسجيل
        navigate("/");
      }
    } catch {
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
          <p onClick={() => setFlipped(true)}>Go to Sign Up →</p>
        </div>

        {/* Signup page */}
        <div className="page page-back">
          <h2 className="auth-title">Sign Up</h2>
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
            {loading ? "Please wait..." : "Sign Up"}
          </button>
          <p onClick={() => setFlipped(false)}>← Back to Login</p>
        </div>
      </div>
    </div>
  );
}

export default AuthBook;
