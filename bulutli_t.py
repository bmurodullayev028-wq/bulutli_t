from flask import Flask, jsonify, request, render_template_string
import os

app = Flask(__name__)

yozuvlar = [
    {"id": 1, "sarlavha": "Lokal muhit (On-Premises)", "holat": "Bajarildi"},
    {"id": 2, "sarlavha": "Bulutli joylashtirish (PaaS / Render)", "holat": "Faol"}
]

HTML_SHABLON = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>1-mustaqil ish — Murodullayev Bekzod</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, sans-serif; }
        body {
            background: linear-gradient(135deg, #090d16, #172033, #0f172a);
            color: #f8fafc;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 24px;
        }
        .container {
            background: rgba(23, 32, 51, 0.92);
            border: 1px solid #334155;
            border-radius: 18px;
            padding: 36px;
            max-width: 720px;
            width: 100%;
            box-shadow: 0 24px 50px rgba(0, 0, 0, 0.55);
        }
        .badge {
            display: inline-block;
            background: rgba(16, 185, 129, 0.14);
            color: #34d399;
            border: 1px solid #059669;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 18px;
        }
        .main-title {
            font-size: 20px;
            line-height: 1.5;
            color: #cbd5e1;
            font-weight: 500;
            margin-bottom: 24px;
        }
        .highlight-mustaqil {
            font-size: 34px;
            font-weight: 800;
            color: #38bdf8;
            letter-spacing: 0.4px;
            display: inline-block;
            margin: 0 4px;
            text-shadow: 0 0 18px rgba(56, 189, 248, 0.28);
        }
        .form-group {
            display: flex;
            gap: 10px;
            margin-bottom: 22px;
            flex-wrap: wrap;
        }
        input {
            flex: 1;
            min-width: 180px;
            padding: 11px 14px;
            border-radius: 9px;
            border: 1px solid #475569;
            background: #0b1120;
            color: #fff;
            outline: none;
        }
        input:focus { border-color: #38bdf8; }
        button {
            background: #0284c7;
            color: white;
            border: none;
            padding: 11px 20px;
            border-radius: 9px;
            cursor: pointer;
            font-weight: 600;
            transition: 0.2s;
        }
        button:hover { background: #0369a1; }
        table { width: 100%; border-collapse: collapse; margin-top: 8px; }
        th, td { text-align: left; padding: 12px; border-bottom: 1px solid #293548; }
        th { color: #38bdf8; font-size: 13px; text-transform: uppercase; }
        tr:hover { background: rgba(51, 65, 85, 0.35); }
        .footer {
            margin-top: 22px;
            font-size: 12px;
            color: #94a3b8;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="badge">● Muhit: {{ muhit }}</div>

<h1 class="main-title">
            Murodullayev Bekzodning bulutli texnologiyalar fanidan 1-<span class="highlight-mustaqil">mustaqil ishi</span>
        </h1>
        <div class="form-group">
            <input type="text" id="sarlavha" placeholder="Yangi bosqich yoki izoh...">
            <input type="text" id="holat" placeholder="Holati (masalan: Tekshirildi)">
            <button onclick="qoshish()">+ Qo‘shish</button>
        </div>

        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Bosqich / Izoh</th>
                    <th>Holat</th>
                </tr>
            </thead>
            <tbody>
                {% for y in yozuvlar %}
                <tr>
                    <td>{{ y.id }}</td>
                    <td>{{ y.sarlavha }}</td>
                    <td>{{ y.holat }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="footer">
            JSON ma’lumot manzili: <a href="/malumotlar" style="color:#38bdf8;">/malumotlar</a>
        </div>
    </div>

    <script>
        async function qoshish() {
            const sarlavha = document.getElementById('sarlavha').value.trim();
            const holat = document.getElementById('holat').value.trim();
            if (!sarlavha || !holat) return alert("Iltimos, ikkala maydonni ham to‘ldiring!");

            const res = await fetch('/malumotlar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sarlavha, holat })
            });
            if (res.ok) location.reload();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    muhit = os.environ.get("CLOUD_ENV", "Lokal muhit (On-Premises)")
    return render_template_string(HTML_SHABLON, muhit=muhit, yozuvlar=yozuvlar)

@app.route('/malumotlar', methods=['GET'])
def get_malumotlar():
    return jsonify(yozuvlar)

@app.route('/malumotlar', methods=['POST'])
def add_malumot():
    yangi = request.get_json()
    yangi["id"] = len(yozuvlar) + 1
    yozuvlar.append(yangi)
    return jsonify(yangi), 201

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
