// App.tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Cart from "./pages/Cart";
import AuthBook from "./pages/AuthBook";
import { AuthProvider } from "./context/AuthContext";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Navbar />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/login" element={<AuthBook defaultPage="login" />} />
          <Route path="/signup" element={<AuthBook defaultPage="signup" />} />
        </Routes>

      </AuthProvider>
    </BrowserRouter>
  );
}
