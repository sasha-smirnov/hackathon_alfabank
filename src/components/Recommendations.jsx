// src/components/Recommendations.jsx
import React from "react";
import "./ProductCard.css";

export default function Recommendations({ products, loading }) {
  return (
    <div className="card product-card">
      <h2>Персональные рекомендации</h2>

      {loading && <p>Подбираем продукты…</p>}

      {!loading && (!products || products.length === 0) && (
        <p className="muted">
          После выбора клиента здесь появятся предложения банка.
        </p>
      )}

      {!loading && products && products.length > 0 && (
        <div className="product-list">
          {products.map((p) => (
            <div key={p.code} className="product-card-big">

              <div className="priority-label">
                Приоритет: {p.priority}
              </div>

              <div className="product-image">
                <img src={`/src/assets/${p.img}`} alt={p.title} />
              </div>

              <div className="product-content">
                <h3 className="product-title">{p.title}</h3>
                <p className="product-sub">{p.reason}</p>
              </div>

            </div>
          ))}
        </div>
      )}
    </div>
  );
}