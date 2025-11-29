// src/components/Recommendations.jsx
import React from "react";

export default function Recommendations({ products, loading }) {
  return (
    <div className="card">
      <h2>Персональные рекомендации</h2>

      {loading && <p>Подбираем продукты…</p>}

      {!loading && (!products || products.length === 0) && (
        <p className="muted">
          После выбора клиента здесь появятся предложения банка.
        </p>
      )}

      {!loading && products && products.length > 0 && (
        <div className="products-grid">
          {products.map((p) => (
            <div key={p.id} className="product-card">
              <h3>{p.name}</h3>
              {p.description && <p>{p.description}</p>}
              {p.reason && <p className="muted">Почему: {p.reason}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
