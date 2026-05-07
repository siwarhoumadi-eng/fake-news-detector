from flask import Flask, request, jsonify, send_file
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/check', methods=['POST'])
def check_news():
    data = request.json
    text = data.get("text", "")

    API_KEY = "AlzaSyXXXX"

    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {
        "query": text,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    result = response.json()

    # If Google found something
    if "claims" in result and len(result["claims"]) > 0:
        return jsonify({
            "prediction": "Fact-checked",
            "details": "Verified by fact-check sources",
            "confidence": 90
        })

    text_lower = text.lower()

    fake_indicators = [
        "shocking", "secret", "miracle",
        "they don't want you to know",
        "100% cure", "guaranteed"
    ]

    absurd_indicators = [
        "moon is made of cheese",
        "earth is flat",
        "humans don't need oxygen"
    ]

    for phrase in absurd_indicators:
        if phrase in text_lower:
            return jsonify({
                "prediction": "Fake News",
                "details": "Scientifically incorrect claim",
                "confidence": 95
            })

    score = 0
    for word in fake_indicators:
        if word in text_lower:
            score += 1

    if score >= 1:
        return jsonify({
            "prediction": "Suspicious",
            "details": "Contains misleading language",
            "confidence": 70
        })

    return jsonify({
        "prediction": "Unverified",
        "details": "No reliable data found",
        "confidence": 40
    })
if __name__ == "__main__":
    app.run(debug=True)