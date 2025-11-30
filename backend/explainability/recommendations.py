from typing import Dict, Any, Optional, List

def get_income_segment(predicted_income: float) -> str:
    if predicted_income < 40_000:
        return "low_income"
    elif predicted_income < 80_000:
        return "mass"
    elif predicted_income < 150_000:
        return "mass_affluent"
    else:
        return "affluent"


def get_risk_level(features_row: dict) -> str:
    blacklist = features_row.get("blacklist_flag", 0) or 0
    max_overdue = features_row.get("hdb_bki_total_max_overdue_sum", 0) or 0
    total_overdue = features_row.get("total_sum", 0) or 0
    ovrd_sum = features_row.get("ovrd_sum", 0) or 0
    active_products = features_row.get("hdb_bki_total_active_products", 0) or 0
    active_products_bki = features_row.get("bki_total_active_products", 0) or 0
    pil_del90 = features_row.get("hdb_bki_total_pil_max_del90", 0) or 0
    other_credits = features_row.get("other_credits_count", 0) or 0
    pil_cnt = features_row.get("pil", 0) or 0

    if blacklist == 1:
        return "high"
    if float(max_overdue) > 0 or total_overdue > 0 or ovrd_sum > 0 or pil_del90 > 0:
        return "high"
    if active_products + active_products_bki + other_credits + pil_cnt >= 7:
        return "high"
    if active_products + active_products_bki + other_credits + pil_cnt >= 3:
        return "medium"
    return "low"

def build_recommendations(predicted_income: float,
                          features_row: dict,
                          shap_explanation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    segment = get_income_segment(predicted_income)
    risk_level = get_risk_level(features_row)

    products: List[Dict[str, Any]] = []
    reasons: List[str] = []

    if segment == "low_income":
        products.append({
            "code": "basic_debit",
            "title": "Базовая дебетовая карта с кэшбэком",
            "priority": 2,
            "reason": "Низкий доход — без лишней кредитной нагрузки",
            "img": "debit.png"
        })
        reasons.append("Доход ниже 40 000 ₽ — приоритет базовые продукты")

    elif segment == "mass":
        products.append({
            "code": "classic_credit_card",
            "title": "Классическая кредитная карта",
            "priority": 2,
            "reason": "Стабильный доход позволяет пользоваться кредитным лимитом",
            "img": "credit.png"
        })
        products.append({
            "code": "savings_account",
            "title": "Накопительный счёт",
            "priority": 3,
            "reason": "Можно откладывать часть дохода",
            "img": "save.png"
        })
        reasons.append("Доход 40 000–80 000 ₽ — клиент готов к кредитным и сберегательным продуктам")

    elif segment == "mass_affluent":
        products.append({
            "code": "premium_credit_card",
            "title": "Премиальная карта с повышенным кэшбэком",
            "priority": 2,
            "reason": "Повышенный доход — релевантны премиальные опции",
            "img": "only.png"
        })
        products.append({
            "code": "investment_account",
            "title": "Инвестиционный счёт",
            "priority": 3,
            "reason": "Часть дохода можно направить в инвестиции",
            "img": "investment.png"
        })
        reasons.append("Доход 80 000–150 000 ₽ — клиент готов к более сложным продуктам")

    else:  # affluent
        products.append({
            "code": "private_banking",
            "title": "Персональное премиальное обслуживание",
            "priority": 1,
            "reason": "Высокий доход — релевантен индивидуальный сервис",
            "img": "private.png"
        })
        products.append({
            "code": "advanced_invest",
            "title": "Продвинутые инвестиционные решения",
            "priority": 2,
            "reason": "Можно предложить сложные портфельные продукты",
            "img": "proinvest.png"
        })
        reasons.append("Доход выше 150 000 ₽ — премиальный сегмент клиентов")

    # риск
    if risk_level == "high":
        reasons.append("Высокий кредитный риск — просрочки и/или высокая задолженность")
        products.insert(0, {
            "code": "debt_consulting",
            "title": "Финансовая консультация по снижению долговой нагрузки",
            "priority": 0,
            "reason": "Приоритет — стабилизация текущей долговой нагрузки",
            "img": "credit_consult.png"
        })
        products = [
            p for p in products
            if not p["code"].startswith("classic_credit_card")
            and not p["code"].startswith("premium_credit_card")
        ]
    elif risk_level == "medium":
        reasons.append("Средний кредитный риск — есть кредиты и задолженность, но без критичных просрочек")
    else:
        reasons.append("Низкий кредитный риск — кредиты и задолженность в допустимых пределах")

    # SHAP — доп. объяснение
    if shap_explanation is not None:
        top_contribs = shap_explanation.get("contributions", [])[:3]
        for c in top_contribs:
            fname = c["feature"]
            sval = c["shap_value"]
            if sval > 0:
                reasons.append(f"Признак '{fname}' увеличивает оценку дохода моделью")
            else:
                reasons.append(f"Признак '{fname}' снижает оценку дохода моделью")

    return {
        "segment": segment,
        "risk_level": risk_level,
        "predicted_income": float(predicted_income),
        "products": products,
        "reasons": reasons
    }
