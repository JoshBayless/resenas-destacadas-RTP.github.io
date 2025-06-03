from flask import Flask, render_template, jsonify
import json
from collections import Counter
import re

app = Flask(__name__)

def get_reviews():
    with open('reviews.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_top_words(reviews, n=10):
    all_text = ' '.join([r['review'] for r in reviews]).lower()
    words = re.findall(r'\b\w+\b', all_text)
    stopwords = {'la', 'el', 'de', 'y', 'a', 'en', 'que', 'los', 'las', 'por', 'un', 'una', 'con', 'es', 'al', 'del', 'se', 'para', 'su'}
    filtered_words = [w for w in words if w not in stopwords]
    top_words = Counter(filtered_words).most_common(n)
    return top_words

@app.route('/')
def index():
    reviews = get_reviews()
    top_words = get_top_words(reviews)
    return render_template('index.html', reviews=reviews, top_words=top_words)

@app.route('/api/reviews')
def api_reviews():
    return jsonify(get_reviews())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
