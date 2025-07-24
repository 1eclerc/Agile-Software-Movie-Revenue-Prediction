# 🎬 Movie Revenue Predictor with Flask and TMDB API

This project is a web-based application that allows users to explore movie metadata and predict box office revenue using a machine learning model. It utilizes the TMDB API to fetch movie details and an XGBoost regression model to estimate potential revenue based on popularity and runtime.

---

## 🚀 Features

- 🔐 Login system with basic role-based access (admin/user)
- 🔍 Movie search via TMDB API
- 📊 Revenue prediction using a pre-trained XGBoost model
- 🧹 Data cleaning and text sanitization for cleaner display
- 📁 Save and display movie data in CSV format or on web table
- 🧠 Admins can filter by genre/year and choose append/overwrite modes

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML (Jinja templates)
- **Machine Learning**: XGBoost, joblib
- **External API**: [The Movie Database (TMDB)](https://www.themoviedb.org/)
- **Others**: NumPy, Requests, CSV, RegEx

---

## 📂 Project Structure

```
.
├── main.py              # Flask application entry point
├── config.py            # Contains TMDB API key
├── xgb_revenue_model.pkl# Pre-trained XGBoost model
├── templates/           # HTML templates (login, index, user panel, etc.)
├── static/              # (Optional) For styles, images, etc.
└── output.csv           # Saved movie data (created at runtime)
```

---

## 🧪 How It Works

1. **Login** as either an admin or user.
2. **Admins** can search movies by genre/year and choose how data is saved.
3. Movie data is **fetched from TMDB**, cleaned, and displayed or saved to CSV.
4. Revenue is predicted using an ML model trained on popularity and runtime.

---

## 🧠 Model Info

The `xgb_revenue_model.pkl` file contains a trained XGBoost regression model. It takes:

- `popularity` (float)
- `runtime` (float)

as input features to predict the estimated **box office revenue**.

---

## 🧰 Requirements

Install required packages via pip:

```bash
pip install -r requirements.txt
```

**Example `requirements.txt`:**
```
flask
requests
numpy
joblib
```

---

## 🔐 Default Credentials

| Username | Password   | Role  |
|----------|------------|-------|
| admin    | adminpass  | Admin |
| user     | userpass   | User  |

---

## 👥 Team & Contributors

- [@1eclerc](https://github.com/1eclerc)
- [@ishowkenobi](https://github.com/ishowkenobi)

---

## 📝 License

This project is for educational purposes.

---
