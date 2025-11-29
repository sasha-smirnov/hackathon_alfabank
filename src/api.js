// src/api.js

const BASE_URL = "http://localhost:8000"; // замени на свой backend

async function postJson(path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error(`API error ${res.status}`);
  }
  return res.json();
}

export async function predictIncome(clientId) {
  // ожидаем ответ вида { income: number, confidence: number }
  return postJson("/predict", { client_id: clientId });
}

export async function explainIncome(clientId) {
  // ожидаем ответ вида { features: [{ name, value, impact }] }
  return postJson("/explain", { client_id: clientId });
}

export async function recommendProducts(clientId) {
  // ожидаем ответ вида { products: [{ id, name, description, reason }] }
  return postJson("/recommend", { client_id: clientId });
}
