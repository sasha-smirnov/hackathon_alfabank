from mode_utils import load_features
from explainability import load_model, get_shap_explainer, explain_single_prediction, FEATURE_DESCRIPTIONS
from recommendations import build_recommendations

model = load_model()
df, X, feature_names, cat_cols = load_features("backend/explainability/test.csv")
explainer = get_shap_explainer(model)

x_row = X.iloc[0]
explanation = explain_single_prediction(explainer, model, x_row, FEATURE_DESCRIPTIONS, top_k=40)
prediction = explanation["prediction"]
features_row = x_row.to_dict()


recs = build_recommendations(
    predicted_income=prediction,
    features_row=features_row,
    shap_explanation=explanation
)

print("EXPLANATION:\n", explanation)
print("\nRECOMMENDATIONS:\n", recs)