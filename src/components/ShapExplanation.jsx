import React, { useState } from "react";
import "./ShapExplanation.css";

const TABS = [
  { key: "income", label: "Доходы" },
  { key: "risk", label: "Кредитный риск" },
  { key: "salary", label: "Зарплата" },
  { key: "behavior", label: "Поведение" },
  { key: "spend_style", label: "Стиль трат" },
  { key: "invest", label: "Инвестиции" },
];

export default function ShapExplanation({ features, loading }) {
  const [category, setCategory] = useState("salary");

  const filtered =
    category === "salary"
      ? features
      : features.filter((f) => f.category === category);

  return (
    <div className="shap-card">
      <h2>Почему модель решила так?</h2>

      <div className="tabs-container">
        {TABS.map((t) => (
          <div
            key={t.key}
            className={
              "tab-item " + (category === t.key ? "active" : "")
            }
            onClick={() => setCategory(t.key)}
          >
            {t.label}
          </div>
        ))}
      </div>

      {loading && <p>Загрузка…</p>}
      {!loading && filtered.length === 0 && (
        <p className="muted">
          Выберите клиента и дождитесь объяснения модели.
        </p>
      )}

      {!loading && filtered.length > 0 && (
        <div className="shap-list">
          {filtered.map((f) => {
            const width = Math.min(Math.abs(f.impact) * 100, 100);
            return (
              <div className="shap-row" key={f.name}>
                <div className="shap-label">
                  <strong>{f.name}</strong>
                  <span className="muted">значение: {f.value}</span>
                </div>

                <div className="shap-bar-container">
                  <div
                    className={
                      "shap-bar " + (f.impact >= 0 ? "shap-pos" : "shap-neg")
                    }
                    style={{ width: width + "%" }}
                  />
                </div>

                <div className="shap-impact">
                  {f.impact >= 0 ? "+" : "−"}
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