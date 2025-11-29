import pandas as pd
import numpy as np
import shap
from catboost import CatBoostRegressor


FEATURE_DESCRIPTIONS = {
    # --- Служебные (в модели не используются, но описания оставим на всякий случай) ---
    "id": "ID клиента",
    "dt": "Дата актуальности данных",
    "target": "Целевая переменная (доход клиента)",

    # --- Обороты по текущим счетам ---
    "turn_cur_cr_avg_act_v2": "Средний текущий кредитовый оборот по текущим счетам (12 мес)",
    "avg_cur_cr_turn": "Средний кредитовый оборот по текущим счетам (3 мес)",
    "turn_cur_cr_avg_v2": "Средний кредитовый оборот по текущим счетам (12 мес)",
    "turn_cur_cr_max_v2": "Максимальный кредитовый оборот по текущим счетам (12 мес)",
    "turn_cur_cr_sum_v2": "Суммарный кредитовый оборот по текущим счетам (12 мес)",
    "turn_cur_cr_min_v2": "Минимальный кредитовый оборот по текущим счетам (12 мес)",
    "turn_cur_cr_7avg_avg_v2": "Средний кредитовый оборот за последние 7 дней",

    # --- Дебетовые обороты по текущим счетам ---
    "turn_cur_db_sum_v2": "Суммарный дебетовый оборот по текущим счетам (12 мес)",
    "turn_cur_db_avg_act_v2": "Средний текущий дебетовый оборот по текущим счетам (12 мес)",
    "turn_cur_db_avg_v2": "Средний дебетовый оборот по текущим счетам (12 мес)",
    "avg_cur_db_turn": "Средний дебетовый оборот по текущим счетам (3 мес)",
    "turn_cur_db_max_v2": "Максимальный дебетовый оборот по текущим счетам (12 мес)",
    "turn_other_db_max_v2": "Максимальный дебетовый оборот по другим счетам",
    "turn_cur_db_min_v2": "Минимальный дебетовый оборот по текущим счетам (12 мес)",
    "turn_cur_db_7avg_avg_v2": "Средний дебетовый оборот за последние 7 дней",

    # --- Остатки на счетах ---
    "curr_rur_amt_cm_avg": "Средний остаток на текущих счетах (12 мес)",
    "curr_rur_amt_3m_avg": "Средний остаток на текущих счетах (3 мес)",
    "dda_rur_amt_curr_v2": "Остаток на счетах до востребования",
    "total_rur_amt_cm_avg": "Средний общий остаток по всем счетам (12 мес)",
    "loanacc_rur_amt_cm_avg": "Средний остаток на кредитных счетах (12 мес)",
    "loanacc_rur_amt_curr_v2": "Текущий остаток на кредитных счетах",
    "loanacc_rur_amt_cm_avg_inc_v2": "Изменение остатка на кредитных счетах за период",
    "curr_rur_amt_cm_avg_inc_v2": "Изменение остатка на текущих счетах за период",
    "curr_rur_amt_cm_avg_period_days_ago_v2": "Средний остаток по текущим счетам (смещённый период)",

    # --- Категориальные траты ---
    "avg_by_category__amount__sum__cashflowcategory_name__vydacha_nalichnyh_v_bankomate":
        "Средняя сумма снятия наличных в банкомате (12 мес)",

    "transaction_category_supermarket_percent_cnt_2m":
        "Доля транзакций в категории 'Супермаркеты' за 2 месяца",

    "avg_credit_turn_rur": "Средний кредитовый оборот по всем счетам (3 мес)",
    "avg_debet_turn_rur": "Средний дебетовый оборот по всем счетам (3 мес)",

    "avg_amount_daily_transactions_90d":
        "Средняя дневная сумма транзакций (90 дней)",
    
    "avg_6m_all": "Средние траты клиента за 6 месяцев",
    "summarur_1m_purch": "Сумма покупок за текущий месяц",

    # --- Электронные платежи ---
    "by_category__amount__sum__eoperation_type_name__perevod_po_nomeru_telefona":
        "Переводы по номеру телефона (средняя сумма)",

    # --- Доход ---
    "incomeValue": "Заявленный доход клиента",

    # --- Локация ---
    "city_smart_name": "Город клиента по SMART-модели",

    # --- Кредитная активность (БКИ/Банк) ---
    "hdb_bki_total_max_limit": "Максимальный кредитный лимит по данным БКИ",
    "hdb_bki_total_cc_max_limit": "Максимальный лимит по кредитным картам (БКИ)",
    "hdb_bki_total_pil_max_limit": "Максимальный лимит по кредитам наличными (БКИ)",
    "hdb_bki_total_products": "Количество кредитных продуктов клиента (БКИ)",
    "hdb_bki_total_cnt": "Количество обращений в БКИ",
    "hdb_bki_total_ip_cnt": "Количество ипотечных продуктов (БКИ)",
    "hdb_bki_total_micro_cnt": "Количество микрокредитов (БКИ)",
    "hdb_bki_active_cc_max_limit": "Максимальный лимит по активной кредитной карте (БКИ)",
    "hdb_bki_active_pil_cnt": "Количество активных кредитов наличными (БКИ)",
    "hdb_bki_active_pil_max_limit": "Максимальный лимит по активному кредиту наличными (БКИ)",
    "hdb_bki_total_pil_last_days": "Дней с момента последнего кредита наличными",
    "hdb_bki_last_product_days": "Дней с момента последнего кредитного продукта",
    "bki_total_active_products": "Количество активных кредитных продуктов (все продукты)",
    "bki_total_max_limit": "Максимальный кредитный лимит клиента",
    "bki_total_il_max_limit": "Максимальный лимит по продукту 'Кредит'",

    # --- Просрочки ---
    "hdb_bki_total_max_overdue_sum": "Максимальная сумма просрочки по данным БКИ",
    "hdb_bki_total_pil_max_overdue": "Максимальная просрочка по кредиту наличными",
    "hdb_bki_total_pil_max_del90": "Количество просрочек 90+ дней по кредиту наличными",
    "hdb_bki_total_cc_max_overdue": "Максимальная просрочка по кредитным картам",
    "hdb_bki_active_cc_max_outstand": "Максимальная задолженность по активной кредитной карте",
    "hdb_bki_active_cc_max_overdue": "Максимальная текущая просрочка по активной кредитной карте",

    "hdb_outstand_sum": "Сумма задолженности (БКИ)",
    "hdb_relend_outstand_sum": "Сумма задолженности по кредитам других типов",
    "hdb_other_outstand_sum": "Задолженность по кредитам в других банках",
    "hdb_ovrd_sum": "Сумма просрочки по данным БКИ",
    "ovrd_sum": "Сумма просрочки по данным банка",
    "total_sum": "Общая сумма просрочек клиента",

    # --- Рефинансирование / ПСК ---
    "hdb_relend_active_max_psk": "Максимальная ПСК по активным кредитам",
    "hdb_other_active_max_psk": "Максимальная ПСК по кредитам в других банках",

    # --- Кредитные продукты: структура ---
    "pil": "Количество кредитов наличными",
    "other_credits_count": "Количество кредитов клиента в других банках",

    # --- Прочее ---
    "tz_msk_timedelta": "Разница с московским часовым поясом",
    "curbal_usd_amt_cm_avg": "Средний баланс USD-счетов за период",
    "winback_cnt": "Количество возвратов из состояния оттока",
    "client_active_flag": "Признак активности клиента",
    "nonresident_flag": "Признак нерезидента РФ",
    "accountsalary_out_flag": "Признак наличия зарплатного проекта",

    # --- UniScore ---
    "uniV5": "Композитный скоринговый показатель UniV5"
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
                              feature_descriptions,
                              top_k=10):

    X = x_row.to_frame().T
    shap_values = explainer.shap_values(X)[0]
    base_value = explainer.expected_value
    prediction = model.predict(X)[0]

    contributions = []
    for fname, fval, sval in zip(X.columns, X.iloc[0], shap_values):
        
        desc = feature_descriptions.get(fname, "")

        contributions.append({
            "feature": fname,
            "feature_description": desc,
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