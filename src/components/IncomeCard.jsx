// src/components/IncomeCard.jsx
import React from "react";

export default function IncomeCard({ income, confidence, loading, error }) {
  return (
    <div className="card">
      <h2>Прогноз дохода</h2>

      {loading && <p>Считаем прогноз…</p>}
      {error && <p className="error">Ошибка: {error}</p>}

      {!loading && !error && income != null && (
        <>
          <p className="income-value">
            {income.toLocaleString("ru-RU")} ₽ / мес
          </p>
          {confidence != null && (
            <p className="muted">
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
