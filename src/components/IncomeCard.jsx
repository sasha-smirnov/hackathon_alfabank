// src/components/IncomeCard.jsx
import React from "react";
import "./IncomeCard.css"

export default function IncomeCard({ income, confidence, loading, error }) {
  return (
    <div className="card income-card">
      <h2 className = "income-title" >Прогноз дохода</h2>

      {loading && <p>Считаем прогноз…</p>}
      {error && <p className="error">Ошибка: {error}</p>}

      {!loading && !error && income != null && (
        <>
          <h3 className="income-value">
            <span className="income-number">{income}</span> ₽ / мес
          </h3>
          {confidence != null && (
            <p className="income-confidence">
              Уверенность модели: {(confidence * 100).toFixed(0)}%
            </p>
          )}
        </>
      )}

      {!loading && !error && income == null && (
        <p className="muted">Выберите клиента, чтобы увидеть прогноз.</p>
      )}
    </div>
  );
}
