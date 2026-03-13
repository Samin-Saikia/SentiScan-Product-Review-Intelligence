from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import re
import os
import pandas as pd

app = Flask(__name__, static_folder='static')
CORS(app)

# ── Load model ──────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'sentiment_model.pkl')
model_bundle = None

def load_model():
    global model_bundle
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model_bundle = pickle.load(f)
        print("✅  Model loaded successfully.")
    else:
        print("⚠️   sentiment_model.pkl not found. Place it next to app.py.")

load_model()

# ── Text cleaning (mirrors your notebook) ───────────────────────────────────
def clean_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
    else:
        text = ''
    return text

# ── Routes ───────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'model_loaded': model_bundle is not None})

@app.route('/api/predict', methods=['POST'])
def predict():
    if model_bundle is None:
        return jsonify({'error': 'Model not loaded. Place sentiment_model.pkl next to app.py and restart.'}), 503

    data = request.get_json()
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    cleaned = clean_text(text)
    vec = model_bundle['vectorizer'].transform([cleaned])
    raw = model_bundle['model'].predict(vec)[0]
    score = max(1, min(5, round(raw)))
    confidence = round(min(100, max(0, (1 - abs(raw - score)) * 100)), 1)

    labels = {1: 'Very Negative', 2: 'Negative', 3: 'Neutral', 4: 'Positive', 5: 'Very Positive'}
    colors = {1: '#ef4444', 2: '#f97316', 3: '#eab308', 4: '#22c55e', 5: '#10b981'}

    return jsonify({
        'score': score,
        'raw': round(float(raw), 3),
        'label': labels[score],
        'color': colors[score],
        'confidence': confidence
    })

@app.route('/api/analyze-csv', methods=['POST'])
def analyze_csv():
    if model_bundle is None:
        return jsonify({'error': 'Model not loaded.'}), 503

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are supported'}), 400

    try:
        df = pd.read_csv(file, encoding='latin1')
    except Exception as e:
        return jsonify({'error': f'Could not read CSV: {str(e)}'}), 400

    text_cols = ['ProductName', 'Review', 'Summary']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
        else:
            df[col] = ''

    df['combined_text'] = (
        df['ProductName'].fillna('') + ' ' +
        df['Review'].fillna('') + ' ' +
        df['Summary'].fillna('')
    )

    X = model_bundle['vectorizer'].transform(df['combined_text'])
    preds = model_bundle['model'].predict(X)
    df['Predicted_Rate'] = [max(1, min(5, round(p))) for p in preds]

    counts = df['Predicted_Rate'].value_counts().sort_index()
    total = len(df)

    distribution = {}
    for star in range(1, 6):
        c = int(counts.get(star, 0))
        distribution[str(star)] = {'count': c, 'pct': round(c / total * 100, 2) if total else 0}

    good  = int(df[df['Predicted_Rate'].isin([4, 5])].shape[0])
    neutral = int(df[df['Predicted_Rate'] == 3].shape[0])
    bad   = int(df[df['Predicted_Rate'].isin([1, 2])].shape[0])

    # Sample rows for preview
    preview = df[['combined_text', 'Predicted_Rate']].head(10).to_dict(orient='records')

    return jsonify({
        'total': total,
        'distribution': distribution,
        'summary': {
            'good':    {'count': good,    'pct': round(good    / total * 100, 2) if total else 0},
            'neutral': {'count': neutral, 'pct': round(neutral / total * 100, 2) if total else 0},
            'bad':     {'count': bad,     'pct': round(bad     / total * 100, 2) if total else 0},
        },
        'preview': preview
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
