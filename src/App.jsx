// src/App.jsx
import React, { useEffect, useState } from "react";
import {
  predictIncome,
  explainIncome,
  recommendProducts,
} from "./api";

import ClientSelector from "./components/ClientSelector";
import IncomeCard from "./components/IncomeCard";
import ShapExplanation from "./components/ShapExplanation";
import Recommendations from "./components/Recommendations";
import alfa_logo from './assets/alfa_logo.jpg';

export default function App() {
  const [clientId, setClientId] = useState(null);

  // income
  const [income, setIncome] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [incomeLoading, setIncomeLoading] = useState(false);
  const [incomeError, setIncomeError] = useState(null);

  // shap
  const [shap, setShap] = useState([]);
  const [shapLoading, setShapLoading] = useState(false);

  // recommendations
  const [products, setProducts] = useState([]);
  const [productsLoading, setProductsLoading] = useState(false);

  useEffect(() => {
    if (!clientId) {
      setIncome(null);
      setConfidence(null);
      setShap([]);
      setProducts([]);
      return;
    }

    setIncomeLoading(true);
    predictIncome(clientId)
      .then((data) => {
        setIncome(data.income);
        setConfidence(data.confidence);
      })
      .catch((err) => setIncomeError(err.message))
      .finally(() => setIncomeLoading(false));

    setShapLoading(true);
    explainIncome(clientId)
      .then((data) => setShap(data.features))
      .finally(() => setShapLoading(false));

    setProductsLoading(true);
    recommendProducts(clientId)
      .then((data) => setProducts(data.products))
      .finally(() => setProductsLoading(false));
  }, [clientId]);

  return (
    <div className="page">
      <img src={alfa_logo} className="corner-img" alt="logo" />
      <header className="header">
        <div>
          <h1>Прогнозирование дохода клиентов</h1>
        </div>

      </header>

      <main className="layout">

        {/* Левая колонка */}
        <section className="left-column">
          <ClientSelector selectedId={clientId} onChange={setClientId} />

          <IncomeCard
            income={income}
            confidence={confidence}
            loading={incomeLoading}
            error={incomeError}
          />
        </section>

        {/* Правая колонка */}
        <section className="right-column">
          <ShapExplanation features={shap} loading={shapLoading} />

          <Recommendations products={products} loading={productsLoading} />
        </section>

      </main>

      <footer className="footer">
        <span className="muted">
          ПИКМЕ
        </span>
      </footer>
    </div>
  );
}
