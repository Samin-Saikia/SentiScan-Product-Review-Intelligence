<div align="center">

# 🔮 SentiScan
### Product Review Intelligence — ML-Powered Sentiment Analysis

[![Live Demo](https://img.shields.io/badge/Live%20Demo-sentiscan.onrender.com-7c6bff?style=for-the-badge&logo=render&logoColor=white)](https://sentiscan-product-review-intelligence.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)

*Predict star ratings from product reviews using a TF-IDF + Linear Regression pipeline trained on 190,000+ real Flipkart reviews.*

</div>

---

## ✨ Features

- **Real-time Text Analysis** — Paste any product review and instantly get a predicted star rating (1–5) with confidence score and animated visual feedback
- **CSV Batch Processing** — Upload any CSV file with review data and get a full sentiment distribution, star breakdown, and row-by-row preview
- **Flexible Column Detection** — Works with standard columns (`ProductName`, `Review`, `Summary`) or any custom column names automatically
- **Production Ready** — Deployed on Render with Gunicorn, CORS-enabled REST API, and a fully responsive frontend

---

## 🚀 Live Demo

**[https://sentiscan-product-review-intelligence.onrender.com](https://sentiscan-product-review-intelligence.onrender.com)**

> ⚠️ Hosted on Render's free tier — first load may take 30–60 seconds to wake up from idle.

---

## 📸 Preview

| Text Analysis | CSV Batch Results |
|---|---|
| Paste a review → get star rating + confidence | Upload CSV → full distribution + preview table |

---

## 🧠 How It Works

```
Raw Review Text
      │
      ▼
Text Cleaning (lowercase, remove special chars)
      │
      ▼
TF-IDF Vectorization (5,000 features)
      │
      ▼
Linear Regression Model
      │
      ▼
Predicted Star Rating (1–5) + Confidence Score
```

The model was trained on **189,874 Flipkart product reviews** combining `ProductName`, `Review`, and `Summary` columns into a single text feature. The predicted float is clipped and rounded to the nearest integer in the 1–5 range.

---

## 🗂️ Project Structure

```
SentiScan/
├── app.py                  # Flask backend — REST API
├── requirements.txt        # Python dependencies
├── sentiment_model.pkl     # Trained model + TF-IDF vectorizer
└── static/
    └── index.html          # Frontend — HTML, CSS, Vanilla JS
```

---

## ⚙️ API Reference

### `GET /api/health`
Check if the server and model are running.

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

### `POST /api/predict`
Predict sentiment for a single text input.

**Request:**
```json
{
  "text": "Amazing product! Totally worth the price."
}
```

**Response:**
```json
{
  "score": 5,
  "raw": 4.823,
  "label": "Very Positive",
  "color": "#10b981",
  "confidence": 82.3
}
```

---

### `POST /api/analyze-csv`
Batch analyze an entire CSV file.

**Request:** `multipart/form-data` with a `file` field containing a `.csv` file

**Response:**
```json
{
  "total": 200,
  "distribution": {
    "1": { "count": 20, "pct": 10.0 },
    "5": { "count": 95, "pct": 47.5 }
  },
  "summary": {
    "good":    { "count": 130, "pct": 65.0 },
    "neutral": { "count": 30,  "pct": 15.0 },
    "bad":     { "count": 40,  "pct": 20.0 }
  },
  "preview": [...]
}
```

---

## 🏃 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Samin-Saikia/SentiScan-Product-Review-Intelligence.git
cd SentiScan-Product-Review-Intelligence
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the server**
```bash
python app.py
```

**4. Open in browser**
```
http://localhost:5000
```

---

## 📊 Dataset

Trained on the [Flipkart Product Reviews](https://www.kaggle.com/) dataset containing **189,874 entries** across 812 unique products.

| Column | Description |
|---|---|
| `ProductName` | Name of the product |
| `Price` | Listed price |
| `Rate` | Star rating (1–5) — **target variable** |
| `Review` | Short review title |
| `Summary` | Full review text |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| ML Model | scikit-learn — TF-IDF + Linear Regression |
| Backend | Python, Flask, Gunicorn |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Deployment | Render |

---

## 📈 Model Performance

| Metric | Value |
|---|---|
| Algorithm | Linear Regression |
| Vectorizer | TF-IDF (5,000 features) |
| Train/Test Split | 80% / 20% |
| Target | Star Rating (1–5) |

---

## 👤 Author

**Samin Saikia**
- GitHub: [@Samin-Saikia](https://github.com/Samin-Saikia)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built with 🔮 and deployed to production</sub>
</div>