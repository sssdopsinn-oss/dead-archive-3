from flask import Flask, render_template_string, request, jsonify, redirect, session, url_for
import json
import os
import time

app = Flask(__name__)
app.secret_key = 'dead_archive_secret_key_2026'

# Временное хранилище в памяти
app.orders_data = []
ACTIVE_SESSIONS = {}
ONLINE_TIMEOUT = 10

def get_real_online_count():
    now = time.time()
    expired_clients = [cid for cid, last_seen in ACTIVE_SESSIONS.items() if now - last_seen > ONLINE_TIMEOUT]
    for cid in expired_clients:
        del ACTIVE_SESSIONS[cid]
    return len(ACTIVE_SESSIONS)

products = [
    {
        "id": 1,
        "name": "ФУТБОЛКА VET@MENTS ANTISOCIAL",
        "category": "tshirts",
        "price_eur": 60,
        "price_uah": 3050,
        "images": ["https://picsum.photos/id/1015/800/800"],
        "description": "Оверсайз силуэт. Тяжелый премиальный хлопок. Архивный графический принт на груди.",
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "id": 2,
        "name": "ХУДИ ARCHIVE 04 'DESTRUCTION'",
        "category": "hoodies",
        "price_eur": 120,
        "price_uah": 6100,
        "images": ["https://picsum.photos/id/1039/800/800"],
        "description": "Состаренный дизайн, потертости на манжетах, двойной капюшон.",
        "sizes": ["M", "L", "XL"]
    }
]

# Главная страница сайта
@app.route('/')
def index():
    return render_template_string(INDEX_HTML, products=products)

# Оформление заказа
@app.route('/api/order', methods=['POST'])
def create_order():
    data = request.json
    order = {
        "id": len(app.orders_data) + 1,
        "items": data.get("items", []),
        "total": data.get("total", 0),
        "customer": data.get("customer", {}),
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    app.orders_data.append(order)
    return jsonify({"success": True, "order_id": order["id"]})

# Админ-панель с нормальной формой входа
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == 'deadarchive2026':
            session['admin_logged'] = True
            return redirect(url_for('admin'))
        else:
            return render_template_string(LOGIN_HTML, error="Неверный пароль")
            
    if not session.get('admin_logged'):
        return render_template_string(LOGIN_HTML, error="")

    orders_html = ""
    for o in app.orders_data:
        orders_html += f"<li>Заказ #{o['id']} на сумму {o['total']} ({o['time']}) — Покупатель: {o['customer']}</li>"
    if not orders_html:
        orders_html = "<p>Пока нет ни одного заказа.</p>"

    return render_template_string(ADMIN_HTML, orders=orders_html, online=get_real_online_count())

# Пинг для подсчета онлайн пользователей
@app.route('/api/ping', methods=['POST'])
def ping():
    client_ip = request.remote_addr
    ACTIVE_SESSIONS[client_ip] = time.time()
    return jsonify({"online": get_real_online_count()})


# --- HTML ШАБЛОНЫ ---

INDEX_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>DEAD ARCHIVE</title>
    <style>
        body { background: #0a0a0a; color: #fff; font-family: monospace; margin: 0; padding: 20px; }
        h1 { text-align: center; letter-spacing: 3px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
        .card { background: #161616; border: 1px solid #333; padding: 15px; }
        .card img { width: 100%; height: 300px; object-fit: cover; }
        button { background: #fff; color: #000; border: none; padding: 10px; width: 100%; cursor: pointer; font-weight: bold; margin-top: 10px; }
        button:hover { background: #ccc; }
        #online-counter { position: fixed; bottom: 10px; right: 10px; background: #222; padding: 5px 10px; border: 1px solid #444; font-size: 12px; }
    </style>
</head>
<body>
    <h1>DEAD ARCHIVE</h1>
    <div class="grid">
        {% for p in products %}
        <div class="card">
            <img src="{{ p.images[0] }}" alt="{{ p.name }}">
            <h3>{{ p.name }}</h3>
            <p>{{ p.price_eur }} EUR / {{ p.price_uah }} UAH</p>
            <p>{{ p.description }}</p>
            <button onclick="buy({{ p.id }})">КУПИТЬ</button>
        </div>
        {% endfor %}
    </div>

    <div id="online-counter">Онлайн: <span id="count">1</span></div>

    <script>
        function buy(id) {
            fetch('/api/order', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({items: [id], total: 60, customer: "Тестовый покупатель"})
            })
            .then(res => res.json())
            .then(data => alert('Заказ #' + data.order_id + ' успешно оформлен!'));
        }

        setInterval(() => {
            fetch('/api/ping', {method: 'POST'})
                .then(res => res.json())
                .then(data => { document.getElementById('count').innerText = data.online; });
        }, 5000);
    </script>
</body>
</html>
"""

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Вход в админку | DEAD ARCHIVE</title>
    <style>
        body { background: #111; color: #fff; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background: #1a1a1a; padding: 30px; border: 1px solid #333; width: 300px; }
        input { width: 100%; padding: 10px; background: #000; border: 1px solid #444; color: #fff; margin-top: 10px; box-sizing: border-box; }
        button { background: #fff; color: #000; border: none; padding: 10px; width: 100%; font-weight: bold; margin-top: 15px; cursor: pointer; }
        .error { color: #ff5555; font-size: 12px; margin-top: 10px; text-align: center; }
    </style>
</head>
<body>
    <div class="login-box">
        <h3>ВХОД В АДМИНКУ</h3>
        <form method="POST">
            <input type="password" name="password" placeholder="Введите пароль" required>
            <button type="submit">ВОЙТИ</button>
            {% if error %}<div class="error">{{ error }}</div>{% endif %}
        </form>
    </div>
</body>
</html>
"""

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Админ-панель | DEAD ARCHIVE</title>
    <style>
        body { background: #111; color: #fff; font-family: monospace; padding: 30px; }
        h1 { color: #ff5555; }
        .box { background: #222; padding: 20px; border: 1px solid #444; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>Админ-панель DEAD ARCHIVE</h1>
    <div class="box">
        <h3>Статистика</h3>
        <p>Пользователей онлайн сейчас: <b>{{ online }}</b></p>
    </div>
    <div class="box">
        <h3>Список заказов</h3>
        <ul>
            {{ orders | safe }}
        </ul>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
