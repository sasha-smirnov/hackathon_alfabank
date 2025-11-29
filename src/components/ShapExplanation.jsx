// src/components/ShapExplanation.jsx
import React from "react";

export default function ShapExplanation({ features, loading }) {
  return (
    <div className="card">
      <h2>Почему модель решила так?</h2>

      {loading && <p>Считаем вклад признаков…</p>}

      {!loading && (!features || features.length === 0) && (
        <p className="muted">
          Выберите клиента и дождитесь объяснения модели.
        </p>
      )}

      {!loading && features && features.length > 0 && (
        <div className="shap-list">
          {features.map((f) => {
            const width = Math.min(Math.abs(f.impact) * 100, 100); // impact в условных единицах 0–1
            const sign = f.impact >= 0 ? "+" : "−";
            return (
              <div key={f.name} className="shap-row">
                <div className="shap-label">
                  <strong>{f.name}</strong>
                  <span className="muted">значение: {String(f.value)}</span>
                </div>
                <div className="shap-bar-container">
                  <div
                    className={
                      "shap-bar " + (f.impact >= 0 ? "shap-pos" : "shap-neg")
                    }
                    style={{ width: `${width}%` }}
                  />
                </div>
                <div className="shap-impact">
                  {sign}
                  {Math.abs(f.impact).toFixed(2)}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
