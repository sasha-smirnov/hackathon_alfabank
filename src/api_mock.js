// src/api_mock.js

export async function predictIncome(clientId) {
  await sleep(500); // имитация задержки
  return {
    income: 120000 + clientId * 13, // рандомная логика
    confidence: 0.82
  };
}

export async function explainIncome(clientId) {
  await sleep(400);

  return {
    features: [
      { name: "Возраст", value: 28 + (clientId % 5), impact: +0.32 },
      { name: "Траты в месяц", value: 45000, impact: -0.21 },
      { name: "Скоринговый балл", value: 690, impact: +0.18 },
      { name: "Есть кредиты", value: "Да", impact: -0.09 }
    ]
  };
}

export async function recommendProducts(clientId) {
  await sleep(300);

  return {
    products: [
      {
        id: 1,
        name: "Кредитная карта Alfa Travel",
        description: "Кэшбек до 5%, путешествия, страховка",
        reason: "Подходит при доходе выше 100 000 ₽"
      },
      {
        id: 2,
        name: "Дебетовая карта Alfa Premium",
        description: "Повышенный кэшбек + бесплатные переводы",
        reason: "Ваш скоринговый балл высокий"
      }
    ]
  };
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
