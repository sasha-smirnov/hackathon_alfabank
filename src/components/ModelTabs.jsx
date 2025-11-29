import React, { useState } from "react";
import "./ModelTabs.css";

export default function ModelTabs({ tabs, onChange }) {
  const [active, setActive] = useState(tabs[0].value);

  const handleClick = (val) => {
    setActive(val);
    onChange(val);
  };

  return (
    <div className="tabs-bg">
      {tabs.map((t) => (
        <button
          key={t.value}
          className={`tab-btn ${active === t.value ? "active" : ""}`}
          onClick={() => handleClick(t.value)}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}