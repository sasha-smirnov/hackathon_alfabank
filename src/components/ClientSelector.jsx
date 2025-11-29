// src/components/ClientSelector.jsx
import React from "react";
import './ClientSelector.css'

const MOCK_CLIENTS = [
  { id: 1001, name: "Клиент 1001" },
  { id: 1002, name: "Клиент 1002" },
  { id: 1003, name: "Клиент 1003" },
];

export default function ClientSelector({ selectedId, onChange }) {
  return (
    <div className="card client-card">
      <h2>Выбор клиента</h2>

       <div className="select-card"></div>
        <select
          className = "client-select"
          value={selectedId ?? ""}
          onChange={(e) => onChange(Number(e.target.value))}
        >
        <option value="">Выберите клиента</option>
        {MOCK_CLIENTS.map((c) => (
          <option key={c.id} value={c.id}>
            {c.name} (ID {c.id})
          </option>
        ))}
      </select>
    </div>
  );
}
