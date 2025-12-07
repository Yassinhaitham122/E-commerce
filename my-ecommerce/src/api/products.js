const BASE_URL = "http://127.0.0.1:8000";

export async function getProducts(token) {
  const res = await fetch(`${BASE_URL}/products/`, {
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });
  return res.json();
}