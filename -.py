import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib

# Veri yükle
df = pd.read_csv("tmdb_movies.csv")[["Popularity", "Runtime"]].dropna()

# Sahte Revenue oluştur
np.random.seed(42)
df["Revenue"] = (df["Popularity"] * 1_000_000) + (df["Runtime"] * 50_000) + np.random.normal(0, 5_000_000, len(df))

# Train-test ayır
X = df[["Popularity", "Runtime"]]
y = df["Revenue"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model: XGBoost
model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Tahmin ve metrikler
y_pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R²:", r2_score(y_test, y_pred))

# Kaydet
joblib.dump(model, "xgb_revenue_model.pkl")
