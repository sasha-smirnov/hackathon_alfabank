// src/components/ClientSelector.jsx
import React from "react";

const MOCK_CLIENTS = [
  { id: 1001, name: "Клиент 1001" },
  { id: 1002, name: "Клиент 1002" },
  { id: 1003, name: "Клиент 1003" },
];

export default function ClientSelector({ selectedId, onChange }) {
  return (
    <div className="card">
      <h2>Выбор клиента</h2>
      <select
        value={selectedId ?? ""}
        onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)}
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
