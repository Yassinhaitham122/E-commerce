import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";

interface NavbarProps {
  onSearch?: (query: string) => void;
}

export default function Navbar({ onSearch }: NavbarProps) {
  const location = useLocation();
  const isCartPage = location.pathname === "/cart";

  return (
    <nav className="navbar">
      {/* الشمال: شعار المتجر */}
      <div className="navbar-left">
        <h2 className="logo">JORDEN</h2>
      </div>

      {/* الوسط: Search Bar */}
      <div className="navbar-center">
        {!isCartPage && (
          <input
            type="text"
            placeholder="Search products..."
            className="search-input"
            onChange={(e) => onSearch?.(e.target.value)}
          />
        )}
      </div>

      {/* اليمين: Cart أو Home + Login/Signup */}
      <div className="navbar-right">
        {isCartPage ? (
          <Link to="/">
            <button className="home-button">Home</button>
          </Link>
        ) : (
          <>
            <Link to="/cart">
              <span className="cart-icon">🛒</span>
            </Link>
            {location.pathname !== "/login" && (
              <Link to="/login">
                <button className={location.pathname === "/login" ? "active" : ""}>
                  Login
                </button>
              </Link>
            )}
            {location.pathname !== "/signup" && (
              <Link to="/signup">
                <button className={location.pathname === "/signup" ? "active" : ""}>
                  Sign Up
                </button>
              </Link>
            )}
          </>
        )}
      </div>
    </nav>
  );
}
