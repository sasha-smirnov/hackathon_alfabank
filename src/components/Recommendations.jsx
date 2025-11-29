// src/components/Recommendations.jsx
import React from "react";
import "./ProductCard.css";

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
        <div className="product-list">
          {products.map((p) => (
            <div key={p.code} className="product-card-big">

              <div className="product-image">
                <img src={`/src/assets/${p.img}`} alt={p.title} />
              </div>

              {/*  RIGHT SIDE CONTENT */}
              <div className="product-content">
                <h3 className="product-title">{p.title}</h3>
                <p className="product-sub">{p.reason}</p>

                <div className="product-features">
                  <div className="feature">
                    <span className="feature-title">Приоритет</span>
                    <span className="feature-value">{p.priority}</span>
                  </div>

                  <div className="feature">
                    <span className="feature-title">Продукт</span>
                    <span className="feature-value">{p.code}</span>
                  </div>

                  <div className="feature">
                    <span className="feature-title">Категория</span>
                    <span className="feature-value">Доход</span>
                  </div>
                </div>

                <div className="product-buttons">
                  <button className="btn-outline">Подробнее</button>
                  <button className="btn-red">Открыть</button>
                </div>
              </div>

            </div>
          ))}
        </div>
      )}
    </div>
  );
}