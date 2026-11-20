from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Vaqtinchalik ma'lumotlar bazasi (xotirada)
talabalar = [
    {"id": 1, "ism": "Ali Valiyev", "yonalish": "Axborot xavfsizligi"},
    {"id": 2, "ism": "Jasur Karimov", "yonalish": "Telekommunikatsiya"}
]

@app.route('/')
def home():
    return jsonify({
        "xabar": "Ilova bulutli infratuzilmada muvaffaqiyatli ishlamoqda!",
        "muhit": os.environ.get("CLOUD_ENV", "Lokal muhit (On-Premises)")
    })

@app.route('/talabalar', methods=['GET'])
def get_talabalar():
    return jsonify(talabalar)

@app.route('/talabalar', methods=['POST'])
def add_talaba():
    yangi_talaba = request.get_json()
    yangi_talaba["id"] = len(talabalar) + 1
    talabalar.append(yangi_talaba)
    return jsonify(yangi_talaba), 201

if __name__ == '__main__':
    # Bulutli platformalar PORT o'zgaruvchisini avtomatik beradi
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)