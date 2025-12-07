interface ProductCardProps {
  product: {
    id: number;
    name: string;
    description?: string;
  };
  onAdd: (productId: number) => void;
}

export default function ProductCard({ product, onAdd }: ProductCardProps) {
  return (
    <div style={{ border: "1px solid gray", padding: "10px", margin: "10px" }}>
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <button onClick={() => onAdd(product.id)}>Add to Cart</button>
    </div>
  );
}
