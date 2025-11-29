import React, { useState } from "react";
import "./ModelTabs.css";

export default function ModelTabs({ onChange }) {
  const tabs = [
    { id: "income", label: "Доходы" },
    { id: "credit", label: "Кредитный риск" },
    { id: "salary", label: "Зарплата" },
    { id: "behaviour", label: "Поведение" },
    { id: "style", label: "Стиль трат"},
    { id: "invest", label: "Инвестиции"},
  ];

  const [active, setActive] = useState("income");

  const handleClick = (id) => {
    setActive(id);
    onChange && onChange(id);
  };

  return (
    <div className="tabs_bg">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={`tab-btn ${active === tab.id ? "active" : ""}`}
          onClick={() => handleClick(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}