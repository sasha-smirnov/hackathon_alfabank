import pandas as pd
import numpy as np
import shap
from catboost import CatBoostRegressor


feature_names = {
    "turn_cur_cr_avg_act_v2": "Кредитовый оборот (12м)",
    "avg_cur_cr_turn": "Кредитовый оборот (3м)",
    "turn_cur_cr_avg_v2": "Кредитовый оборот (12м)",
    "turn_cur_cr_max_v2": "Макс. кредитовый оборот",
    "turn_cur_cr_sum_v2": "Сумма кредитового оборота",
    "turn_cur_cr_min_v2": "Мин. кредитовый оборот",
    "turn_cur_cr_7avg_avg_v2": "Кредитовый оборот (7д)",
    "turn_cur_db_sum_v2": "Дебетовый оборот (12м)",
    "turn_cur_db_avg_act_v2": "Дебетовый оборот (12м)",
    "turn_cur_db_avg_v2": "Дебетовый оборот (12м)",
    "avg_cur_db_turn": "Дебетовый оборот (3м)",
    "turn_cur_db_max_v2": "Макс. дебетовый оборот",
    "turn_other_db_max_v2": "Макс. дебет по другим счетам",
    "turn_cur_db_min_v2": "Мин. дебетовый оборот",
    "turn_cur_db_7avg_avg_v2": "Дебетовый оборот (7д)",
    "curr_rur_amt_cm_avg": "Остаток на счёте (12м)",
    "curr_rur_amt_3m_avg": "Остаток на счёте (3м)",
    "dda_rur_amt_curr_v2": "Остаток на текущих счетах",
    "total_rur_amt_cm_avg": "Общий остаток (12м)",
    "loanacc_rur_amt_cm_avg": "Остаток по кредитным счетам (12м)",
    "loanacc_rur_amt_curr_v2": "Остаток по кредитам",
    "loanacc_rur_amt_cm_avg_inc_v2": "Изм. остатка по кредитам",
    "curr_rur_amt_cm_avg_inc_v2": "Изм. остатка (текущий)",
    "curr_rur_amt_cm_avg_period_days_ago_v2": "Остаток (смещённый период)",
    "avg_by_category__amount__sum__cashflowcategory_name__vydacha_nalichnyh_v_bankomate":
        "Снятие в банкоматах",
    "transaction_category_supermarket_percent_cnt_2m": "Супермаркеты %",
    "avg_credit_turn_rur": "Кредитовый оборот (3м)",
    "avg_debet_turn_rur": "Дебетовый оборот (3м)",
    "avg_amount_daily_transactions_90d": "Дневные траты (90д)",
    "avg_6m_all": "Средние траты (6м)",
    "summarur_1m_purch": "Покупки (1м)",
    "by_category__amount__sum__eoperation_type_name__perevod_po_nomeru_telefona":
        "Переводы по номеру телефона",
    "incomeValue": "Заявленный доход",
    "city_smart_name": "Город",
    "hdb_bki_total_max_limit": "Кредитный лимит (макс)",
    "hdb_bki_total_cc_max_limit": "Лимит по кредиткам (макс)",
    "hdb_bki_total_pil_max_limit": "Лимит по кредитам нал.",
    "hdb_bki_total_products": "Кредитных продуктов",
    "hdb_bki_total_cnt": "Запросов в БКИ",
    "hdb_bki_total_ip_cnt": "Ипотек",
    "hdb_bki_total_micro_cnt": "Микрозаймов",
    "hdb_bki_active_cc_max_limit": "Активная кредитка (лимит)",
    "hdb_bki_active_pil_cnt": "Активных кредитов нал.",
    "hdb_bki_active_pil_max_limit": "Активный кредит нал. (лимит)",
    "hdb_bki_total_pil_last_days": "Дней с последнего кредита",
    "hdb_bki_last_product_days": "Дней с последнего продукта",
    "bki_total_active_products": "Активных кредитов",
    "bki_total_max_limit": "Макс. лимит",
    "bki_total_il_max_limit": "Макс. лимит (Кредит)",
    "hdb_bki_total_max_overdue_sum": "Просрочка (макс)",
    "hdb_bki_total_pil_max_overdue": "Просрочка по кредитам нал.",
    "hdb_bki_total_pil_max_del90": "Просрочки 90+",
    "hdb_bki_total_cc_max_overdue": "Просрочка по кредиткам",
    "hdb_bki_active_cc_max_outstand": "Задолженность по кредитке",
    "hdb_bki_active_cc_max_overdue": "Просрочка по кредитке (текущая)",
    "hdb_outstand_sum": "Задолженность (БКИ)",
    "hdb_relend_outstand_sum": "Задолженность по refi",
    "hdb_other_outstand_sum": "Задолженность (другие банки)",
    "hdb_ovrd_sum": "Просрочки (БКИ)",
    "ovrd_sum": "Просрочки (банк)",
    "total_sum": "Общая сумма просрочек",
    "hdb_relend_active_max_psk": "ПСК по активным кредитам",
    "hdb_other_active_max_psk": "ПСК по другим кредитам",
    "pil": "Кредиты нал.",
    "other_credits_count": "Других кредитов",
    "tz_msk_timedelta": "Часовой пояс",
    "curbal_usd_amt_cm_avg": "USD баланс",
    "winback_cnt": "Возвраты клиента",
    "client_active_flag": "Активность",
    "nonresident_flag": "Нерезидент",
    "accountsalary_out_flag": "Зарплатный проект",
    "uniV5": "UniScore"
}

feature_category = {
    "incomeValue": "income",
    "turn_cur_cr_avg_act_v2": "income",
    "avg_cur_cr_turn": "income",
    "turn_cur_cr_avg_v2": "income",
    "turn_cur_cr_max_v2": "income",
    "turn_cur_cr_sum_v2": "income",
    "turn_cur_cr_min_v2": "income",
    "turn_cur_cr_7avg_avg_v2": "income",
    "turn_cur_db_sum_v2": "income",
    "turn_cur_db_avg_act_v2": "income",
    "turn_cur_db_avg_v2": "income",
    "avg_cur_db_turn": "income",
    "turn_cur_db_max_v2": "income",
    "turn_cur_db_min_v2": "income",
    "turn_cur_db_7avg_avg_v2": "income",
    "avg_debet_turn_rur": "income",
    "avg_credit_turn_rur": "income",
    "pil": "credit_risk",
    "other_credits_count": "credit_risk",
    "hdb_bki_total_products": "credit_risk",
    "bki_total_active_products": "credit_risk",
    "hdb_bki_total_cnt": "credit_risk",
    "hdb_bki_active_pil_cnt": "credit_risk",
    "hdb_bki_total_ip_cnt": "credit_risk",
    "hdb_bki_total_micro_cnt": "credit_risk",
    "hdb_bki_total_max_limit": "credit_risk",
    "hdb_bki_total_cc_max_limit": "credit_risk",
    "hdb_bki_total_pil_max_limit": "credit_risk",
    "bki_total_max_limit": "credit_risk",
    "bki_total_il_max_limit": "credit_risk",
    "hdb_bki_total_max_overdue_sum": "credit_risk",
    "hdb_bki_total_pil_max_overdue": "credit_risk",
    "hdb_bki_total_pil_max_del90": "credit_risk",
    "hdb_bki_total_cc_max_overdue": "credit_risk",
    "hdb_bki_active_cc_max_overdue": "credit_risk",
    "hdb_outstand_sum": "credit_risk",
    "hdb_relend_outstand_sum": "credit_risk",
    "hdb_other_outstand_sum": "credit_risk",
    "hdb_ovrd_sum": "credit_risk",
    "ovrd_sum": "credit_risk",
    "total_sum": "credit_risk",
    "hdb_relend_active_max_psk": "credit_risk",
    "hdb_other_active_max_psk": "credit_risk",
    "accountsalary_out_flag": "salary",
    "turn_other_db_max_v2": "salary",  
    "dda_rur_amt_curr_v2": "salary",  
    "avg_amount_daily_transactions_90d": "behavior",
    "winback_cnt": "behavior",
    "client_active_flag": "behavior",
    "nonresident_flag": "behavior",
    "tz_msk_timedelta": "behavior",
    "avg_6m_all": "spending",
    "summarur_1m_purch": "spending",
    "avg_by_category__amount__sum__cashflowcategory_name__vydacha_nalichnyh_v_bankomate":
        "spending",
    "transaction_category_supermarket_percent_cnt_2m": "spending",
    "by_category__amount__sum__eoperation_type_name__perevod_po_nomeru_telefona":
        "spending",
    "curr_rur_amt_cm_avg": "assets",
    "curr_rur_amt_3m_avg": "assets",
    "total_rur_amt_cm_avg": "assets",
    "curr_rur_amt_cm_avg_inc_v2": "assets",
    "curr_rur_amt_cm_avg_period_days_ago_v2": "assets",
    "loanacc_rur_amt_cm_avg": "assets",
    "loanacc_rur_amt_curr_v2": "assets",
    "loanacc_rur_amt_cm_avg_inc_v2": "assets",
    "curbal_usd_amt_cm_avg": "assets",
    "uniV5": "assets",
    "city_smart_name": "location",
}


def load_model(model_path: str = "model.cbm") -> CatBoostRegressor:
    model = CatBoostRegressor()
    model.load_model(model_path)
    return model


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def get_shap_explainer(model: CatBoostRegressor):
    explainer = shap.TreeExplainer(model)
    return explainer


def compute_shap_values(explainer, X: pd.DataFrame, max_samples: int = 1000):
    if len(X) > max_samples:
        X_sample = X.sample(max_samples, random_state=42)
    else:
        X_sample = X
    
    shap_values = explainer.shap_values(X_sample)
    base_value = explainer.expected_value

    return X_sample, shap_values, base_value


def explain_single_prediction(explainer,
                              model,
                              x_row,
                              feature_names,
                              feature_category,
                              top_k=10):

    X = x_row.to_frame().T
    shap_values = explainer.shap_values(X)[0]
    base_value = explainer.expected_value
    prediction = model.predict(X)[0]

    contributions = []
    for fname, fval, sval in zip(X.columns, X.iloc[0], shap_values):
        
        desc = feature_names.get(fname, "")
        category = feature_category.get(fname, "other")

        contributions.append({
            "feature": fname,
            "feature_name": desc,
            "category": category,
            "value": float(fval) if isinstance(fval, (float, int)) else str(fval),
            "shap_value": float(sval)
        })

    contributions_sorted = sorted(
        contributions,
        key=lambda x: abs(x["shap_value"]),
        reverse=True
    )[:top_k]

    return {
        "base_value": float(base_value),
        "prediction": float(prediction),
        "contributions": contributions_sorted
    }
