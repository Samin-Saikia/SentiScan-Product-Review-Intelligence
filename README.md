# SentiScan — Product Review Intelligence
### Flask + HTML/CSS/JS frontend for your sentiment_model.pkl

---

## 📂 Project Structure
```
sentiment_app/
├── app.py                  ← Flask backend
├── requirements.txt
├── sentiment_model.pkl     ← ⬅ place your .pkl here!
└── static/
    └── index.html          ← frontend
```

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Place your model
Copy `sentiment_model.pkl` into the `sentiment_app/` folder (same level as `app.py`).
The pkl must contain a dict with keys `model` and `vectorizer` (matches your notebook).

### 3. Run the server
```bash
python app.py
```

### 4. Open in browser
Visit: **http://localhost:5000**

---

## ✨ Features

| Feature | Description |
|---|---|
| **Text Analysis** | Paste any review → get star rating + sentiment label |
| **Star Ring** | Animated circular progress shows predicted score |
| **Confidence** | Shows how close the raw prediction was to the rounded score |
| **CSV Batch** | Upload a Flipkart CSV, get full distribution + summary |
| **Preview Table** | See first 10 rows of predictions in batch mode |
| **Drag & Drop** | Drag CSV files directly onto the upload zone |
| **Keyboard shortcut** | `Ctrl+Enter` triggers analysis |

---

## 🔌 API Endpoints

| Method | URL | Description |
|---|---|---|
| GET | `/api/health` | Check if model is loaded |
| POST | `/api/predict` | `{"text": "..."}` → single prediction |
| POST | `/api/analyze-csv` | multipart/form-data CSV → batch analysis |

---

## 📝 CSV Format
Your CSV should have these columns (same as training data):
- `ProductName`
- `Review`
- `Summary`

Missing columns are handled gracefully (treated as empty strings).
