const BASE_URL = "http://127.0.0.1:8000";

export async function getCart(token) {
  const res = await fetch(`${BASE_URL}/cart/`, {
    headers: { "Authorization": `Bearer ${token}` },
  });
  return res.json();
}

export async function addToCart(productId, token) {
  const res = await fetch(`${BASE_URL}/cart/add/${productId}`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
  });
  return res.json();
}
