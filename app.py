from flask import Flask, render_template_string, request, jsonify, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import time

app = Flask(__name__)
app.secret_key = 'dead_archive_secret_key_2026'

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модели базы данных
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price_eur = db.Column(db.Integer, nullable=False)
    price_uah = db.Column(db.Integer, nullable=False)
    images_str = db.Column(db.Text, nullable=False)  # Ссылки через запятую или JSON
    colors_str = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    sizes_str = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price_eur": self.price_eur,
            "price_uah": self.price_uah,
            "images": [i.strip() for i in self.images_str.split(',') if i.strip()],
            "colors": [c.strip() for c in self.colors_str.split(',') if c.strip()],
            "description": self.description or "",
            "sizes": [s.strip() for s in self.sizes_str.split(',') if s.strip()]
        }

class Order(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    items_json = db.Column(db.Text, nullable=False)
    contacts_json = db.Column(db.Text, nullable=False)
    time_str = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        import json
        return {
            "id": self.id,
            "items": json.loads(self.items_json),
            "contacts": json.loads(self.contacts_json),
            "time": self.time_str
        }

# Создаем таблицы и дефолтные товары, если база пустая
with app.app_context():
    db.create_all()
    if Product.query.count() == 0:
        p1 = Product(
            name="ФУТБОЛКА VET@MENTS ANTISOCIAL",
            category="tshirts",
            price_eur=60,
            price_uah=3050,
            images_str="https://kappa.lol/zlEwzv, https://picsum.photos/id/1015/800/800",
            colors_str="Черный, Серый",
            description="Оверсайз силуэт. Тяжелый премиальный хлопок. Архивный графический принт на груди.",
            sizes_str="S, M, L, XL"
        )
        p2 = Product(
            name="ФУТБОЛКА VET@MENTS.COM",
            category="tshirts",
            price_eur=60,
            price_uah=3050,
            images_str="https://kappa.lol/34ieZw, https://kappa.lol/gJtShU",
            colors_str="Черный",
            description="Классический свободный крой. Дистресс-эффект с потертостями по краям. Фирменная вышивка на спине.",
            sizes_str="S, M, L"
        )
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()

ACTIVE_SESSIONS = {}
ONLINE_TIMEOUT = 10

def get_real_online_count():
    now = time.time()
    expired_clients = [cid for cid, last_seen in ACTIVE_SESSIONS.items() if now - last_seen > ONLINE_TIMEOUT]
    for cid in expired_clients:
        del ACTIVE_SESSIONS[cid]
    return len(ACTIVE_SESSIONS)

lookbooks = [
    {
        "id": "look-01",
        "title": "LOOK // 01: HEAVY METAL OPIUM",
        "concept": "Многослойный брутальный авангард с уклоном в оверсайз и массивный металлический обвес.",
        "image": "https://picsum.photos/id/1059/800/1000",
    },
    {
        "id": "look-02",
        "title": "LOOK // 02: GRAVE LEATHER DIRT",
        "concept": "Сочетание состаренной кожи, дистресс-хлопка и темной ритуальной символики.",
        "image": "https://picsum.photos/id/1062/800/1000",
    }
]

HTML_HEADER = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>DEAD ARCHIVE // 2026</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Inter:wght@400;500;700;900&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; background:#020202; color:#e4e4e7; position: relative; }
    .gothic { font-family:'Cinzel', serif; font-weight: 900; }
    .blood-logo { position: relative; transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
    .blood-logo:hover { color: #ef4444 !important; text-shadow: 0 0 12px rgba(239, 68, 68, 0.9); }
    .fade-in { animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #020202; }
    ::-webkit-scrollbar-thumb { background: #18181b; border: 1px solid #27272a; }
  </style>
</head>
<body class="antialiased select-none">
  <nav class="fixed top-0 w-full bg-[#020202]/95 backdrop-blur-xl py-6 border-b border-zinc-900 z-50">
    <div class="max-w-7xl mx-auto px-6 flex justify-between items-center">
      <div onclick="location.href='/'" class="blood-logo inline-block cursor-pointer py-1">
        <h1 class="text-2xl md:text-3xl gothic tracking-[0.3em] text-zinc-50 transition-colors">DEAD ARCHIVE</h1>
      </div>
      <div class="flex gap-4 md:gap-8 text-xs font-bold items-center text-zinc-400 tracking-widest">
        <div class="hidden sm:flex items-center gap-2 bg-zinc-950 border border-zinc-800/80 px-3 py-1.5 rounded-full text-[11px] text-zinc-400">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span>ОНЛАЙН: <span id="online-counter" class="text-zinc-100 font-mono font-black text-xs">1</span></span>
        </div>
        <a href="/shop" class="hover:text-zinc-50 transition-colors uppercase text-sm">МАГАЗИН</a>
        <a href="/lookbook" class="hover:text-zinc-50 transition-colors uppercase text-red-500 font-black text-sm">LOOKBOOK</a>
        <button id="cart-nav-btn" onclick="toggleCart()" class="text-xs font-bold hover:text-zinc-50 transition-all flex items-center gap-3 bg-zinc-900 border border-zinc-800 px-4 py-2.5 rounded-sm">
          КОРЗИНА // <span class="text-zinc-100 text-sm" id="count">0</span>
        </button>
      </div>
    </div>
  </nav>
"""

HTML_FOOTER = """
  <div id="cart-modal" class="hidden fixed inset-0 bg-black/98 flex items-center justify-center z-[9999] backdrop-blur-md">
    <div class="bg-[#09090b] w-full max-w-xl p-10 border border-zinc-800 max-h-[90vh] overflow-auto relative">
      <button onclick="toggleCart()" class="absolute top-6 right-6 text-zinc-500 hover:text-zinc-100 text-2xl transition-colors">✕</button>
      <div id="cart-main-view">
        <h2 class="text-xl font-black mb-8 tracking-[0.2em] text-center text-zinc-50 uppercase">ВЫБРАННЫЕ АРТИКУЛЫ</h2>
        <div id="cart-items" class="space-y-8"></div>
        <div class="mt-10 border-t border-zinc-900 pt-8">
          <button onclick="openCheckoutForm()" id="checkout-btn" class="w-full py-5 bg-zinc-100 text-black text-xs font-black tracking-[0.2em] hover:bg-black hover:text-white hover:border hover:border-zinc-700 transition-all uppercase">
            ОФОРМИТЬ ЗАКАЗ
          </button>
        </div>
      </div>
      <div id="cart-checkout-view" class="hidden">
        <h2 class="text-xl font-black mb-2 tracking-[0.2em] text-center text-zinc-50 uppercase">ИДЕНТИФИКАЦИЯ</h2>
        <div class="space-y-6">
          <div>
            <label class="block text-[11px] font-black text-zinc-400 mb-2 tracking-widest uppercase">TELEGRAM USERNAME</label>
            <input type="text" id="cust-tg" placeholder="@OPIUM_CRW" class="w-full bg-zinc-950 border border-zinc-800 px-4 py-4 text-sm text-zinc-100 focus:outline-none focus:border-zinc-500 font-bold tracking-wider">
          </div>
          <div>
            <label class="block text-[11px] font-black text-zinc-400 mb-2 tracking-widest uppercase">НОМЕР ТЕЛЕФОНА</label>
            <input type="text" id="cust-phone" placeholder="+380..." class="w-full bg-zinc-950 border border-zinc-800 px-4 py-4 text-sm text-zinc-100 focus:outline-none focus:border-zinc-500 font-bold tracking-wider">
          </div>
        </div>
        <div class="mt-10 flex gap-4">
          <button onclick="backToCartItems()" class="w-1/3 py-4 border border-zinc-800 text-zinc-300 text-xs font-bold uppercase">НАЗАД</button>
          <button onclick="submitOrder()" id="submit-order-btn" class="w-2/3 py-4 bg-zinc-100 text-black font-black text-xs tracking-[0.15em] uppercase">ОТПРАВИТЬ ЗАПРОС</button>
        </div>
      </div>
      <div id="cart-success-view" class="hidden text-center py-12">
        <h2 class="text-2xl font-black mb-4 tracking-[0.15em] text-zinc-50 uppercase">ТРАНЗАКЦИЯ ПРИНЯТА</h2>
      </div>
    </div>
  </div>

  <script>
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    function initRealOnlineCounter() {
      let clientId = sessionStorage.getItem('da_client_id');
      if (!clientId) {
        clientId = 'usr_' + Math.random().toString(36).substring(2, 9) + '_' + Date.now();
        sessionStorage.setItem('da_client_id', clientId);
      }
      function sendHeartbeat() {
        fetch('/api/heartbeat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ client_id: clientId })
        })
        .then(res => res.json())
        .then(data => {
          const el = document.getElementById('online-counter');
          if (el && data.online !== undefined) el.textContent = data.online;
        }).catch(() => {});
      }
      sendHeartbeat();
      setInterval(sendHeartbeat, 4000);
    }
    function updateCartUI() {
      const countEl = document.getElementById('count');
      if (countEl) countEl.textContent = cart.length;
      const container = document.getElementById('cart-items');
      if (!container) return;
      container.innerHTML = '';
      if (cart.length === 0) {
        container.innerHTML = '<p class="text-zinc-600 text-center py-12 text-xs font-bold tracking-widest">АРХИВ ПУСТ</p>';
        if(document.getElementById('checkout-btn')) document.getElementById('checkout-btn').style.display = 'none';
        return;
      } else {
        if(document.getElementById('checkout-btn')) document.getElementById('checkout-btn').style.display = 'block';
      }
      cart.forEach((item, i) => {
        const div = document.createElement('div');
        div.className = "flex gap-6 border-b border-zinc-900 pb-6 items-center fade-in";
        div.innerHTML = `
          <img src="${item.images && item.images[0] ? item.images[0] : ''}" class="w-16 h-20 object-cover border border-zinc-800">
          <div class="flex-1 min-w-0">
            <p class="font-black text-sm tracking-wider text-zinc-100 truncate uppercase">${item.name}</p>
            <p class="text-zinc-300 text-sm mt-1 font-bold">${item.price_eur} EUR</p>
            <p class="text-xs text-zinc-400 tracking-wider mt-1 font-bold uppercase">РАЗМЕР // [${item.selectedSize}]</p>
            ${item.selectedColor ? `<p class="text-xs text-zinc-400 tracking-wider mt-0.5 font-bold uppercase">ЦВЕТ // [${item.selectedColor}]</p>` : ''}
          </div>
          <button onclick="removeFromCart(${i})" class="text-zinc-500 hover:text-zinc-100 text-2xl px-2">✕</button>
        `;
        container.appendChild(div);
      });
    }
    function toggleCart() {
      document.getElementById('cart-modal').classList.toggle('hidden');
      updateCartUI();
    }
    function removeFromCart(i) {
      cart.splice(i, 1);
      localStorage.setItem('cart', JSON.stringify(cart));
      updateCartUI();
    }
    function openCheckoutForm() {
      if (cart.length === 0) return;
      document.getElementById('cart-main-view').classList.add('hidden');
      document.getElementById('cart-checkout-view').classList.remove('hidden');
    }
    function backToCartItems() {
      document.getElementById('cart-checkout-view').classList.add('hidden');
      document.getElementById('cart-main-view').classList.remove('hidden');
    }
    function submitOrder() {
      const tg = document.getElementById('cust-tg').value.trim();
      const phone = document.getElementById('cust-phone').value.trim();
      if (!tg && !phone) return;
      fetch('/create_order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: cart, contacts: { telegram: tg, phone: phone } })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          cart = [];
          localStorage.setItem('cart', JSON.stringify(cart));
          updateCartUI();
          document.getElementById('cart-checkout-view').classList.add('hidden');
          document.getElementById('cart-success-view').classList.remove('hidden');
          setTimeout(() => toggleCart(), 2000);
        }
      });
    }
    window.addEventListener('DOMContentLoaded', () => {
      updateCartUI();
      initRealOnlineCounter();
    });
  </script>
</body>
</html>
"""

@app.route('/api/heartbeat', methods=['POST'])
def heartbeat():
    data = request.get_json() or {}
    client_id = data.get('client_id')
    if client_id:
        ACTIVE_SESSIONS[client_id] = time.time()
    return jsonify({"online": get_real_online_count()})

@app.route('/')
def home():
    return render_template_string(HTML_HEADER + '''
  <section class="h-screen flex items-center justify-center bg-cover bg-center relative" style="background-image: url('https://kappa.lol/1edKYn')">
    <div class="absolute inset-0 bg-black/90"></div>
    <div class="relative text-center z-10 px-6">
      <h1 class="text-4xl md:text-[6.5rem] gothic tracking-[0.25em] text-zinc-100 leading-none">DEAD ARCHIVE</h1>
      <p class="text-sm tracking-[0.4em] text-zinc-400 mt-10 font-black uppercase">ПРОТОКОЛ СИСТЕМЫ DE-2026 // ПРИВАТНЫЙ ДРОП</p>
      <div class="mt-20 flex flex-wrap justify-center gap-6">
        <a href="/shop" class="px-12 py-5 border border-zinc-700 hover:bg-zinc-100 hover:text-black text-xs tracking-[0.3em] transition-all text-zinc-100 font-black uppercase">ВОЙТИ В МАГАЗИН</a>
      </div>
    </div>
  </section>
''' + HTML_FOOTER)

@app.route('/shop')
def shop():
    products = [p.to_dict() for p in Product.query.all()]
    return render_template_string(HTML_HEADER + '''
  <section class="pt-40 pb-24 px-6 max-w-7xl mx-auto">
    <h2 class="text-3xl gothic text-center mb-16 tracking-[0.3em] text-zinc-100">КОЛЛЕКЦИЯ</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-6 gap-y-12" id="grid"></div>
  </section>
  <script>
    const products = {{ products|tojson|safe }};
    const selectedSizes = {};
    const selectedColors = {};
    const currentImageIndices = {};
    
    function selectSize(id, sz, btn) {
      selectedSizes[id] = sz;
      const errEl = document.getElementById('error-' + id);
      if (errEl) errEl.classList.add('hidden');

      document.querySelectorAll('.size-btn-' + id).forEach(b => {
        b.classList.remove('bg-zinc-100', 'text-black', 'border-zinc-100');
        b.classList.add('bg-zinc-900', 'text-zinc-300', 'border-zinc-700');
      });
      btn.classList.remove('bg-zinc-900', 'text-zinc-300', 'border-zinc-700');
      btn.classList.add('bg-zinc-100', 'text-black', 'border-zinc-100');
    }

    function selectColor(id, col, btn) {
      selectedColors[id] = col;
      document.querySelectorAll('.color-btn-' + id).forEach(b => {
        b.classList.remove('bg-zinc-100', 'text-black', 'border-zinc-100');
        b.classList.add('bg-zinc-900', 'text-zinc-300', 'border-zinc-700');
      });
      btn.classList.remove('bg-zinc-900', 'text-zinc-300', 'border-zinc-700');
      btn.classList.add('bg-zinc-100', 'text-black', 'border-zinc-100');
    }

    function changeImage(id, index) {
      currentImageIndices[id] = index;
      const p = products.find(x => x.id === id);
      if (p && p.images[index]) {
        const imgEl = document.getElementById('product-img-' + id);
        if (imgEl) imgEl.src = p.images[index];
      }
    }

    function renderProducts() {
      const grid = document.getElementById('grid');
      grid.innerHTML = '';
      products.forEach(p => {
        currentImageIndices[p.id] = 0;
        const div = document.createElement('div');
        div.className = "bg-zinc-950 border border-zinc-800 p-5 flex flex-col justify-between";
        
        let sizesHtml = '<div class="flex flex-wrap gap-2 mt-3">';
        if (p.sizes && p.sizes.length > 0) {
          p.sizes.forEach(sz => {
            sizesHtml += `<button onclick="selectSize(${p.id}, '${sz}', this)" class="size-btn-${p.id} px-3 py-1 text-xs border border-zinc-700 bg-zinc-900 text-zinc-300 transition-colors">${sz}</button>`;
          });
        }
        sizesHtml += '</div>';

        let colorsHtml = '';
        if (p.colors && p.colors.length > 0) {
          colorsHtml += '<div class="flex flex-wrap gap-2 mt-3"><span class="w-full text-[10px] font-bold text-zinc-500 uppercase">Цвет:</span>';
          p.colors.forEach(col => {
            colorsHtml += `<button onclick="selectColor(${p.id}, '${col}', this)" class="color-btn-${p.id} px-3 py-1 text-xs border border-zinc-700 bg-zinc-900 text-zinc-300 transition-colors uppercase">${col}</button>`;
          });
          colorsHtml += '</div>';
        }

        let thumbsHtml = '';
        if (p.images && p.images.length > 1) {
          thumbsHtml += '<div class="flex gap-2 mt-2">';
          p.images.forEach((img, idx) => {
            thumbsHtml += `<img src="${img}" onclick="changeImage(${p.id}, ${idx})" class="w-10 h-12 object-cover border border-zinc-800 cursor-pointer hover:border-zinc-400 transition-all">`;
          });
          thumbsHtml += '</div>';
        }

        div.innerHTML = `
          <div>
            <img id="product-img-${p.id}" src="${p.images && p.images[0] ? p.images[0] : ''}" class="w-full h-80 object-cover border border-zinc-800">
            ${thumbsHtml}
            <h3 class="text-sm font-black mt-4 text-zinc-100 uppercase">${p.name}</h3>
            <p class="text-sm text-zinc-300 mt-1 font-bold">${p.price_eur} EUR</p>
            <p class="text-xs text-zinc-400 mt-2">${p.description || ''}</p>
            ${colorsHtml}
            ${sizesHtml}
            <p id="error-${p.id}" class="text-red-500 text-[10px] font-bold mt-2 hidden uppercase tracking-wider">⚠ ВЫБЕРИТЕ РАЗМЕР</p>
          </div>
          <button onclick="addToCart(${p.id})" class="mt-6 w-full py-3 bg-zinc-900 border border-zinc-700 text-xs font-black uppercase text-zinc-200 hover:bg-zinc-100 hover:text-black transition-all">ДОБАВИТЬ</button>
        `;
        grid.appendChild(div);
      });
    }

    function addToCart(id) {
      const p = products.find(x => x.id === id);
      const sz = selectedSizes[id];
      const col = selectedColors[id] || (p.colors && p.colors[0] ? p.colors[0] : '');
      
      if (!sz && p.sizes && p.sizes.length > 0) {
        const errEl = document.getElementById('error-' + id);
        if (errEl) errEl.classList.remove('hidden');
        return;
      }

      cart.push({ ...p, selectedSize: sz || 'ONE SIZE', selectedColor: col });
      localStorage.setItem('cart', JSON.stringify(cart));
      updateCartUI();
      toggleCart();
    }

    window.addEventListener('DOMContentLoaded', renderProducts);
  </script>
''' + HTML_FOOTER, products=products)

@app.route('/lookbook')
def lookbook():
    return render_template_string(HTML_HEADER + '''
  <section class="pt-40 pb-24 px-6 max-w-7xl mx-auto">
    <h2 class="text-3xl gothic text-center mb-16 tracking-[0.3em] text-zinc-100">LOOKBOOK</h2>
    <div class="space-y-16">
      {% for lb in lookbooks %}
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 bg-zinc-950 border border-zinc-800 p-6 items-center">
        <img src="{{ lb.image }}" class="w-full h-[400px] object-cover">
        <div>
          <h3 class="text-xl font-black text-zinc-100">{{ lb.title }}</h3>
          <p class="text-sm text-zinc-400 mt-4">{{ lb.concept }}</p>
        </div>
      </div>
      {% endfor %}
    </div>
  </section>
''' + HTML_FOOTER, lookbooks=lookbooks)

@app.route('/create_order', methods=['POST'])
def create_order():
    import json
    data = request.get_json() or {}
    order_id = "ORD-" + str(int(time.time()))[-5:]
    
    new_order = Order(
        id=order_id,
        items_json=json.dumps(data.get("items", []), ensure_ascii=False),
        contacts_json=json.dumps(data.get("contacts", {}), ensure_ascii=False),
        time_str=time.strftime("%Y-%m-%d %H:%M:%S")
    )
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({"success": True, "order_id": order_id})

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "0879385")

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        pw = request.form.get('password')
        if pw == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = "НЕВЕРНЫЙ КОД ДОСТУПА"
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
      <meta charset="UTF-8">
      <title>ADMIN LOGIN // DEAD ARCHIVE</title>
      <script src="https://cdn.tailwindcss.com"></script>
      <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@400;900&display=swap" rel="stylesheet">
      <style>body { font-family: 'Inter', sans-serif; background:#020202; color:#e4e4e7; }</style>
    </head>
    <body class="flex items-center justify-center h-screen">
      <div class="bg-zinc-950 border border-zinc-800 p-8 w-full max-w-md">
        <h1 class="text-xl font-black tracking-[0.2em] text-center mb-6 text-zinc-100">АВТОРИЗАЦИЯ АДМИНА</h1>
        {% if error %}
        <p class="text-red-500 text-xs font-bold text-center mb-4 tracking-wider">{{ error }}</p>
        {% endif %}
        <form method="POST" class="space-y-4">
          <input type="password" name="password" placeholder="Пароль системы..." required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100 focus:outline-none focus:border-zinc-400">
          <button type="submit" class="w-full py-4 bg-zinc-100 text-black font-black text-xs tracking-widest hover:bg-black hover:text-white hover:border hover:border-zinc-700 transition-all uppercase">ВОЙТИ</button>
        </form>
      </div>
    </body>
    </html>
    ''', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/add_product', methods=['POST'])
def add_product():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    try:
        name = request.form.get('name')
        price_eur = int(request.form.get('price_eur', 0))
        price_uah = int(request.form.get('price_uah', 0))
        category = request.form.get('category')
        
        img1 = request.form.get('image_1', '').strip()
        img2 = request.form.get('image_2', '').strip()
        img3 = request.form.get('image_3', '').strip()
        images = [i for i in [img1, img2, img3] if i]
        if not images:
            images = ["https://picsum.photos/id/1015/800/800"]
        images_str = ", ".join(images)

        colors_str = request.form.get('colors', 'Черный')
        sizes_str = request.form.get('sizes', 'S, M, L, XL')
        description = request.form.get('description', '')

        new_item = Product(
            name=name,
            category=category,
            price_eur=price_eur,
            price_uah=price_uah,
            images_str=images_str,
            colors_str=colors_str,
            description=description,
            sizes_str=sizes_str
        )
        db.session.add(new_item)
        db.session.commit()
    except Exception as e:
        print("Error adding product:", e)

    return redirect(url_for('admin_panel', tab='products'))

@app.route('/admin/edit_product', methods=['POST'])
def edit_product():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    try:
        pid = int(request.form.get('id', 0))
        p = Product.query.get(pid)
        if p:
            p.name = request.form.get('name')
            p.price_eur = int(request.form.get('price_eur', 0))
            p.price_uah = int(request.form.get('price_uah', 0))
            p.category = request.form.get('category')
            
            img1 = request.form.get('image_1', '').strip()
            img2 = request.form.get('image_2', '').strip()
            img3 = request.form.get('image_3', '').strip()
            new_images = [i for i in [img1, img2, img3] if i]
            if new_images:
                p.images_str = ", ".join(new_images)

            colors_str = request.form.get('colors', '')
            if colors_str:
                p.colors_str = colors_str

            sizes_str = request.form.get('sizes', '')
            if sizes_str:
                p.sizes_str = sizes_str
                
            p.description = request.form.get('description', '')
            db.session.commit()
    except Exception as e:
        print("Error editing product:", e)

    return redirect(url_for('admin_panel', tab='products'))

@app.route('/admin/', methods=['GET'])
@app.route('/admin', methods=['GET'])
def admin_panel():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    products = [p.to_dict() for p in Product.query.all()]
    orders = [o.to_dict() for o in Order.query.all()]

    action = request.args.get('action')
    if action == 'del_product':
        pid = int(request.args.get('id', 0))
        p = Product.query.get(pid)
        if p:
            db.session.delete(p)
            db.session.commit()
        return redirect(url_for('admin_panel', tab='products'))
    elif action == 'del_order':
        oid = request.args.get('id')
        o = Order.query.get(oid)
        if o:
            db.session.delete(o)
            db.session.commit()
        return redirect(url_for('admin_panel', tab='orders'))

    tab = request.args.get('tab', 'orders')
    edit_id = request.args.get('edit_id', type=int)
    edit_product_obj = None
    if edit_id:
        p_db = Product.query.get(edit_id)
        if p_db:
            edit_product_obj = p_db.to_dict()
        
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
      <meta charset="UTF-8">
      <title>ADMIN PANEL // DEAD ARCHIVE</title>
      <script src="https://cdn.tailwindcss.com"></script>
      <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
      <style>
        body { font-family: 'Inter', sans-serif; background:#020202; color:#e4e4e7; }
        .gothic { font-family: 'Cinzel', serif; }
      </style>
    </head>
    <body class="p-8">
      <div class="max-w-6xl mx-auto">
        <div class="flex justify-between items-center mb-10 border-b border-zinc-800 pb-6">
          <h1 class="text-2xl gothic tracking-[0.2em] text-zinc-100">ПАНЕЛЬ УПРАВЛЕНИЯ АРХИВОМ</h1>
          <div class="flex gap-4">
            <a href="/shop" target="_blank" class="px-4 py-2 border border-zinc-700 text-xs font-bold text-zinc-300 hover:text-white uppercase">НА САЙТ</a>
            <a href="/admin/logout" class="px-4 py-2 bg-red-950/60 border border-red-800 text-xs font-bold text-red-200 uppercase">ВЫЙТИ</a>
          </div>
        </div>

        <div class="flex gap-4 mb-8">
          <a href="/admin?tab=orders" class="px-5 py-2.5 text-xs font-black tracking-widest uppercase border {{ 'bg-zinc-100 text-black border-zinc-100' if tab == 'orders' else 'bg-zinc-900 text-zinc-400 border-zinc-800' }}">ЗАКАЗЫ ({{ orders|length }})</a>
          <a href="/admin?tab=products" class="px-5 py-2.5 text-xs font-black tracking-widest uppercase border {{ 'bg-zinc-100 text-black border-zinc-100' if tab == 'products' else 'bg-zinc-900 text-zinc-400 border-zinc-800' }}">ТОВАРЫ ({{ products|length }})</a>
          <a href="/admin?tab=add" class="px-5 py-2.5 text-xs font-black tracking-widest uppercase border {{ 'bg-zinc-100 text-black border-zinc-100' if tab == 'add' else 'bg-zinc-900 text-zinc-400 border-zinc-800' }}">+ ДОБАВИТЬ ТОВАР</a>
        </div>

        {% if tab == 'orders' %}
          <h2 class="text-lg font-bold mb-6 text-zinc-200 tracking-wider">ВХОДЯЩИЕ ЗАКАЗЫ</h2>
          {% if not orders %}
            <p class="text-zinc-500 text-xs">Заказов пока нет.</p>
          {% else %}
            <div class="space-y-6">
              {% for o in orders %}
              <div class="bg-zinc-950 border border-zinc-800 p-6 flex flex-col md:flex-row justify-between gap-6">
                <div>
                  <div class="flex items-center gap-3">
                    <span class="text-xs font-black text-red-500 uppercase">{{ o.get('id', 'N/A') }}</span>
                    <span class="text-[11px] text-zinc-500">{{ o.get('time', '') }}</span>
                  </div>
                  <div class="mt-3 text-xs text-zinc-300 font-bold space-y-1">
                    <p>Telegram: <span class="text-zinc-100">{{ o.get('contacts', {}).get('telegram') or 'Не указан' }}</span></p>
                    <p>Телефон: <span class="text-zinc-100">{{ o.get('contacts', {}).get('phone') or 'Не указан' }}</span></p>
                  </div>
                  <div class="mt-4 border-t border-zinc-900 pt-3">
                    <p class="text-[10px] font-black text-zinc-500 uppercase mb-2">Состав заказа:</p>
                    <ul class="space-y-1 text-xs text-zinc-300">
                      {% for item in o.get('items', []) %}
                      <li>• {{ item.get('name', 'Товар') }} — <b>РАЗМЕР: {{ item.get('selectedSize', '-') }}</b> {% if item.get('selectedColor') %}| <b>ЦВЕТ: {{ item.get('selectedColor') }}</b>{% endif %} ({{ item.get('price_eur', 0) }} EUR)</li>
                      {% endfor %}
                    </ul>
                  </div>
                </div>
                <div>
                  <a href="/admin?tab=orders&action=del_order&id={{ o.get('id') }}" class="px-4 py-2 bg-red-950/40 border border-red-900 text-red-400 text-xs font-bold uppercase hover:bg-red-900 hover:text-white transition-all">УДАЛИТЬ ЗАКАЗ</a>
                </div>
              </div>
              {% endfor %}
            </div>
          {% endif %}

        {% elif tab == 'products' %}
          {% if edit_product_obj %}
            <div class="mb-10 bg-zinc-950 border border-red-900/50 p-8 max-w-2xl">
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-lg font-bold text-zinc-200 tracking-wider">РЕДАКТИРОВАНИЕ АРТИКУЛА #{{ edit_product_obj.id }}</h2>
                <a href="/admin?tab=products" class="text-xs text-zinc-500 hover:text-white uppercase font-bold">ОТМЕНИТЬ</a>
              </div>
              <form action="/admin/edit_product" method="POST" class="space-y-6">
                <input type="hidden" name="id" value="{{ edit_product_obj.id }}">
                <div>
                  <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Название товара</label>
                  <input type="text" name="name" value="{{ edit_product_obj.name }}" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100 focus:outline-none focus:border-zinc-400">
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Цена (EUR)</label>
                    <input type="number" name="price_eur" value="{{ edit_product_obj.price_eur }}" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100">
                  </div>
                  <div>
                    <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Цена (UAH)</label>
                    <input type="number" name="price_uah" value="{{ edit_product_obj.price_uah }}" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100">
                  </div>
                </div>
                <div>
                  <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Категория</label>
                  <select name="category" class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100">
                    <option value="tshirts" {% if edit_product_obj.category == 'tshirts' %}selected{% endif %}>Футболки (tshirts)</option>
                    <option value="outerwear" {% if edit_product_obj.category == 'outerwear' %}selected{% endif %}>Верхняя одежда (outerwear)</option>
                    <option value="accessories" {% if edit_product_obj.category == 'accessories' %}selected{% endif %}>Аксессуары (accessories)</option>
                  </select>
                </div>
                <div class="space-y-3">
                  <label class="block text-[11px] font-black text-zinc-400 uppercase">Ссылки на фотографии (до 3 штук)</label>
                  <input type="text" name="image_1" value="{{ edit_product_obj.images[0] if edit_product_obj.images|length > 0 else '' }}" placeholder="Фото 1 (Основная)" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-2.5 text-sm text-zinc-100">
                  <input type="text" name="image_2" value="{{ edit_product_obj.images[1] if edit_product_obj.images|length > 1 else '' }}" placeholder="Фото 2 (Необязательно)" class="w-full bg-zinc-900 border border-zinc-700 px-4 py-2.5 text-sm text-zinc-100">
                  <input type="text" name="image_3" value="{{ edit_product_obj.images[2] if edit_product_obj.images|length > 2 else '' }}" placeholder="Фото 3 (Необязательно)" class="w-full bg-zinc-900 border border-zinc-700 px-4 py-2.5 text-sm text-zinc-100">
                </div>
                <div>
                  <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Цвета (через запятую)</label>
                  <input type="text" name="colors" value="{{ edit_product_obj.colors|join(', ') if edit_product_obj.colors else 'Черный' }}" placeholder="Черный, Белый, Серый" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100">
                </div>
                <div>
                  <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Размеры (через запятую)</label>
                  <input type="text" name="sizes" value="{{ edit_product_obj.sizes|join(', ') }}" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100">
                </div>
                <div>
                  <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Описание</label>
                  <textarea name="description" rows="3" class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100">{{ edit_product_obj.description }}</textarea>
                </div>
                <button type="submit" class="w-full py-4 bg-zinc-100 text-black font-black text-xs tracking-widest hover:bg-black hover:text-white hover:border hover:border-zinc-700 transition-all uppercase">СОХРАНИТЬ ИЗМЕНЕНИЯ</button>
              </form>
            </div>
          {% endif %}

          <h2 class="text-lg font-bold mb-6 text-zinc-200 tracking-wider">УПРАВЛЕНИЕ ТОВАРАМИ</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            {% for p in products %}
            <div class="bg-zinc-950 border border-zinc-800 p-4 flex flex-col justify-between">
              <div>
                <img src="{{ p.images[0] if p.images else '' }}" class="w-full h-48 object-cover border border-zinc-800 mb-3">
                <h3 class="text-xs font-black text-zinc-100 uppercase">{{ p.name }}</h3>
                <p class="text-xs text-zinc-400 mt-1">{{ p.price_eur }} EUR</p>
                <p class="text-[11px] text-zinc-500 mt-1">Категория: {{ p.category }}</p>
                {% if p.colors %}
                <p class="text-[11px] text-zinc-400 mt-1">Цвета: {{ p.colors|join(', ') }}</p>
                {% endif %}
              </div>
              <div class="mt-6 flex gap-2">
                <a href="/admin?tab=products&edit_id={{ p.id }}" class="flex-1 text-center py-2 bg-zinc-100 text-black text-xs font-bold hover:bg-white uppercase">ИЗМЕНИТЬ</a>
                <a href="/admin?tab=products&action=del_product&id={{ p.id }}" class="px-3 py-2 bg-zinc-900 border border-zinc-700 text-xs font-bold text-red-400 hover:bg-red-950 uppercase">✕</a>
              </div>
            </div>
            {% endfor %}
          </div>

        {% elif tab == 'add' %}
          <h2 class="text-lg font-bold mb-6 text-zinc-200 tracking-wider">ДОБАВИТЬ НОВЫЙ ТОВАР</h2>
          <form action="/admin/add_product" method="POST" class="bg-zinc-950 border border-zinc-800 p-8 space-y-6 max-w-2xl">
            <div>
              <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Название товара</label>
              <input type="text" name="name" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100 focus:outline-none focus:border-zinc-400">
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Цена (EUR)</label>
                <input type="number" name="price_eur" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100">
              </div>
              <div>
                <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Цена (UAH)</label>
                <input type="number" name="price_uah" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100">
              </div>
            </div>
            <div>
              <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Категория</label>
              <select name="category" class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100">
                <option value="tshirts">Футболки (tshirts)</option>
                <option value="outerwear">Верхняя одежда (outerwear)</option>
                <option value="accessories">Аксессуары (accessories)</option>
              </select>
            </div>
            <div class="space-y-3">
              <label class="block text-[11px] font-black text-zinc-400 uppercase">Ссылки на фотографии (до 3 штук)</label>
              <input type="text" name="image_1" placeholder="Фото 1 URL (Основная)" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-2.5 text-sm text-zinc-100">
              <input type="text" name="image_2" placeholder="Фото 2 URL (Необязательно)" class="w-full bg-zinc-900 border border-zinc-700 px-4 py-2.5 text-sm text-zinc-100">
              <input type="text" name="image_3" placeholder="Фото 3 URL (Необязательно)" class="w-full bg-zinc-900 border border-zinc-700 px-4 py-2.5 text-sm text-zinc-100">
            </div>
            <div>
              <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Цвета (через запятую)</label>
              <input type="text" name="colors" value="Черный, Серый" placeholder="Черный, Белый" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100">
            </div>
            <div>
              <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Размеры (через запятую)</label>
              <input type="text" name="sizes" value="S, M, L, XL" required class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100">
            </div>
            <div>
              <label class="block text-[11px] font-black text-zinc-400 mb-2 uppercase">Описание</label>
              <textarea name="description" rows="3" class="w-full bg-zinc-900 border border-zinc-700 px-4 py-3 text-sm text-zinc-100"></textarea>
            </div>
            <button type="submit" class="w-full py-4 bg-zinc-100 text-black font-black text-xs tracking-widest hover:bg-black hover:text-white hover:border hover:border-zinc-700 transition-all uppercase">ДОБАВИТЬ В КАТАЛОГ</button>
          </form>
        {% endif %}

      </div>
    </body>
    </html>
    ''', tab=tab, orders=orders, products=products, edit_product_obj=edit_product_obj)

if __name__ == '__main__':
    app.run(debug=True)
