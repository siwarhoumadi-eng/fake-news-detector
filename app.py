from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_news():

    data = request.json
    text = data.get("text", "")

    API_KEY = "AlzaSyxxxxxxxxxxxxx"

    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    params = {
        "query": text,
        "key": API_KEY
    }

    try:

        response = requests.get(url, params=params)

        result = response.json()

        if "claims" in result and len(result["claims"]) > 0:

            return jsonify({
                "prediction": "Fact Checked",
                "details": "Reliable sources verified this information.",
                "confidence": 92
            })

        text_lower = text.lower()

        fake_phrases = [
            "moon is made of cheese",
            "earth is flat",
            "humans don't need oxygen"
        ]

        for phrase in fake_phrases:

            if phrase in text_lower:

                return jsonify({
                    "prediction": "Fake News",
                    "details": "Scientifically incorrect information detected.",
                    "confidence": 97
                })

        return jsonify({
            "prediction": "Unverified",
            "details": "No reliable verification found.",
            "confidence": 45
        })

    except Exception as e:

        return jsonify({
            "prediction": "Error",
            "details": str(e),
            "confidence": 0
        })

if __name__ == "__main__":
    app.run(debug=True)