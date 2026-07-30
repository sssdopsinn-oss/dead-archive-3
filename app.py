from flask import Flask, render_template_string, request, jsonify, redirect
import json
import os
import time

app = Flask(__name__)
app.secret_key = 'dead_archive_secret_key_2026'

# Хранилище заказов
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
    {"id": 1, "name": "ФУТБОЛКА VET@MENTS ANTISOCIAL", "category": "tshirts", "price_eur": 60, "price_uah": 3050, "images": ["https://kappa.lol/zlEwzv"], "description": "Оверсайз силуэт. Тяжелый премиальный хлопок. Архивный графический принт на груди.", "sizes": ["S", "M", "L", "XL"]},
    {"id": 2, "name": "ФУТБОЛКА VET@MENTS.COM", "category": "tshirts", "price_eur": 60, "price_uah": 3050, "images": ["https://kappa.lol/34ieZw", "https://kappa.lol/gJtShU", "https://kappa.lol/nrpVrs", "https://kappa.lol/xtkDjf"], "description": "Классический свободный крой. Дистресс-эффект с потертостями по краям. Фирменная вышивка на спине.", "sizes": ["S", "M", "L"]},
    {"id": 3, "name": "ФУТБОЛКА VET@MENTS VITAL EXISTENCE", "category": "tshirts", "price_eur": 60, "price_uah": 3050, "images": ["https://kappa.lol/61Hm4e"], "description": "Готический шрифтовой принт. Заниженная линия плеча, плотный воротник.", "sizes": ["M", "L", "XL"]},
    {"id": 4, "name": "ФУТБОЛКА VET@MENTS I GOT LUCKY", "category": "tshirts", "price_eur": 60, "price_uah": 3050, "images": ["https://kappa.lol/wZhp55"], "description": "Лимитированное издание. Необработанный сырой край подола.", "sizes": ["S", "M", "L", "XL"]},
    {"id": 9, "name": "ХУДИ VET@MENTS OVERSIZED METAL", "category": "outerwear", "price_eur": 110, "price_uah": 5300, "images": ["https://picsum.photos/id/338/800/800"], "description": "Супер-тяжелый френч терри хлопок (700г/м²). Металлический шрифтовой принт, глубокий капюшон-балаклава.", "sizes": ["M", "L", "XL"]},
    {"id": 10, "name": "ЛОНГСЛИВ ANTISOCIAL ZIP", "category": "tshirts", "price_eur": 70, "price_uah": 3400, "images": ["https://picsum.photos/id/684/800/800"], "description": "Удлиненные рукава с потайными металлическими молниями YKK. Двойной воротник, архивные швы наружу.", "sizes": ["S", "M", "L"]},
    {"id": 11, "name": "ФУТБОЛКА VET@MENTS TOTAL DARKNESS", "category": "tshirts", "price_eur": 65, "price_uah": 3150, "images": ["https://picsum.photos/id/222/800/800"], "description": "Эффект сильной стирки (acid wash) до винтажного графитового оттенка. Ручные прорези и дыры на плечах.", "sizes": ["M", "L", "XL", "XXL"]},
    {"id": 5, "name": "СЕРЕБРЯНАЯ ЦЕПЬ С КРЕСТОМ", "category": "accessories", "price_eur": 85, "price_uah": 4100, "images": ["https://picsum.photos/id/180/800/800"], "description": "Массивное серебро .925 пробы. Детализированный авангардный крест в готическом стиле.", "sizes": ["ONE SIZE"]},
    {"id": 6, "name": "КЕПКА DEATH RITUAL", "category": "accessories", "price_eur": 75, "price_uah": 3600, "images": ["https://picsum.photos/id/107/800/800"], "description": "Плотный вареный хлопок черного цвета. Вышитая ритуальная графика. Металлическая застежка.", "sizes": ["ONE SIZE"]},
    {"id": 7, "name": "КОЖАНАЯ РУБАШКА GRAVE", "category": "outerwear", "price_eur": 135, "price_uah": 6500, "images": ["https://picsum.photos/id/201/800/800"], "description": "Премиальная эко-кожа повышенной плотности с эффектом естественного старения. Укороченный boxy-крой.", "sizes": ["M", "L"]},
    {"id": 8, "name": "КОЛЬЦО CHROME HEART", "category": "accessories", "price_eur": 120, "price_uah": 5800, "images": ["https://picsum.photos/id/133/800/800"], "description": "Тяжелый ювелирный сплав. Детальная гравировка в виде геральдических крестов.", "sizes": ["ONE SIZE"]},
    {"id": 12, "name": "СЕРЕБРЯНЫЙ БРАСЛЕТ OPIUM LINK", "category": "accessories", "price_eur": 95, "price_uah": 4600, "images": ["https://picsum.photos/id/435/800/800"], "description": "Плетение из массивных якорных звеньев с чернением. Замок-тогл с выгравированной готической символикой.", "sizes": ["ONE SIZE"]},
]

app.products_data = products

lookbooks = [
    {
        "id": "look-01",
        "title": "LOOK // 01: HEAVY METAL OPIUM",
        "concept": "Многослойный брутальный авангард с уклоном в оверсайз и массивный металлический обвес.",
        "image": "https://picsum.photos/id/1059/800/1000",
        "item_ids": [9, 1, 5, 8]
    },
    {
        "id": "look-02",
        "title": "LOOK // 02: GRAVE LEATHER DIRT",
        "concept": "Сочетание состаренной кожи, дистресс-хлопка и темной ритуальной символики.",
        "image": "https://picsum.photos/id/1062/800/1000",
        "item_ids": [7, 2, 6, 12]
    },
    {
        "id": "look-03",
        "title": "LOOK // 03: TOTAL DARKNESS ARCHIVE",
        "concept": "Темный монохромный силуэт для ночного мегаполиса с акцентом на фактуру стираного хлопка.",
        "image": "https://picsum.photos/id/1025/800/1000",
        "item_ids": [11, 10, 5]
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
    body { font-family: 'Inter', sans-serif; background:#020202; color:#e4e4e7; }
    .gothic { font-family:'Cinzel', serif; font-weight: 900; }
    
    /* ПРЕМИАЛЬНАЯ АНИМАЦИЯ КРОВАВОГО ЛОГОТИПА */
    .blood-logo {
      position: relative;
      transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .blood-logo:hover {
      color: #ef4444 !important;
      text-shadow: 
        0 0 10px rgba(239, 68, 68, 0.8),
        0 0 20px rgba(220, 38, 38, 0.6),
        0 0 40px rgba(153, 27, 27, 0.4);
    }
    .blood-logo::after {
      content: '';
      position: absolute;
      bottom: -6px;
      left: 0;
      width: 100%;
      height: 6px;
      background: radial-gradient(ellipse at center, rgba(220,38,38,0.9) 0%, rgba(153,27,27,0) 75%);
      opacity: 0;
      transform: scaleX(0.4);
      transition: all 0.4s ease;
      pointer-events: none;
    }
    .blood-logo:hover::after {
      opacity: 1;
      transform: scaleX(1);
    }

    /* Динамические капли крови */
    .blood-drop {
      position: absolute;
      width: 4px;
      background: linear-gradient(180deg, #ef4444 0%, #991b1b 100%);
      border-radius: 0 0 4px 4px;
      box-shadow: 0 0 8px #dc2626;
      opacity: 0;
      top: 90%;
      pointer-events: none;
    }

    .blood-logo:hover .drop-1 {
      left: 12%;
      animation: drip 1.4s infinite cubic-bezier(0.55, 0.085, 0.68, 0.53) 0.1s;
    }
    .blood-logo:hover .drop-2 {
      left: 38%;
      animation: drip 1.8s infinite cubic-bezier(0.55, 0.085, 0.68, 0.53) 0.4s;
    }
    .blood-logo:hover .drop-3 {
      left: 65%;
      animation: drip 1.5s infinite cubic-bezier(0.55, 0.085, 0.68, 0.53) 0.25s;
    }
    .blood-logo:hover .drop-4 {
      left: 88%;
      animation: drip 1.6s infinite cubic-bezier(0.55, 0.085, 0.68, 0.53) 0.5s;
    }

    @keyframes drip {
      0% {
        height: 0px;
        transform: translateY(0);
        opacity: 0;
      }
      30% {
        height: 14px;
        opacity: 1;
      }
      80% {
        height: 22px;
        transform: translateY(28px);
        opacity: 0.8;
      }
      100% {
        height: 2px;
        transform: translateY(40px);
        opacity: 0;
      }
    }

    .fade-in { animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    .spinner {
      border: 3px solid rgba(255, 255, 255, 0.1);
      border-radius: 50%;
      border-top: 3px solid #fff;
      width: 22px;
      height: 22px;
      animation: spin 0.6s linear infinite;
      display: inline-block;
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #020202; }
    ::-webkit-scrollbar-thumb { background: #18181b; border: 1px solid #27272a; }

    .cart-bounce {
      animation: cartBounce 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    @keyframes cartBounce {
      0% { transform: scale(1); }
      50% { transform: scale(1.18); border-color: #ef4444; }
      100% { transform: scale(1); }
    }
  </style>
</head>
<body class="antialiased select-none">
  <nav class="fixed top-0 w-full bg-[#020202]/90 backdrop-blur-xl py-6 border-b border-zinc-900 z-50">
    <div class="max-w-7xl mx-auto px-6 flex justify-between items-center">
      <div onclick="location.href='/'" class="blood-logo inline-block cursor-pointer py-1">
        <h1 class="text-2xl md:text-3xl gothic tracking-[0.3em] text-zinc-50 transition-colors">DEAD ARCHIVE</h1>
        <span class="blood-drop drop-1"></span>
        <span class="blood-drop drop-2"></span>
        <span class="blood-drop drop-3"></span>
        <span class="blood-drop drop-4"></span>
      </div>
      <div class="flex gap-4 md:gap-8 text-xs font-bold items-center text-zinc-400 tracking-widest">
        <div class="hidden sm:flex items-center gap-2 bg-zinc-950 border border-zinc-800/80 px-3 py-1.5 rounded-full text-[10px] text-zinc-400">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span>ОНЛАЙН: <span id="online-counter" class="text-zinc-100 font-mono font-black">1</span></span>
        </div>
        <a href="/shop" class="hover:text-zinc-50 transition-colors uppercase">МАГАЗИН</a>
        <a href="/lookbook" class="hover:text-zinc-50 transition-colors uppercase text-red-500 font-black">LOOKBOOK</a>
        <a href="/history" class="hover:text-zinc-50 transition-colors uppercase text-zinc-300">ИСТОРИЯ ЗАКАЗОВ</a>
        <button id="cart-nav-btn" onclick="toggleCart()" class="text-xs font-bold hover:text-zinc-50 transition-all flex items-center gap-3 bg-zinc-900 border border-zinc-800 px-4 py-2.5 rounded-sm">
          КОРЗИНА // <span class="text-zinc-100" id="count">0</span>
        </button>
      </div>
    </div>
  </nav>
"""

HTML_FOOTER = """
  <div id="cart-modal" class="hidden fixed inset-0 bg-black/98 flex items-center justify-center z-50 backdrop-blur-md">
    <div class="bg-[#09090b] w-full max-w-xl p-10 border border-zinc-800 max-h-[90vh] overflow-auto relative">
      <button onclick="toggleCart()" class="absolute top-6 right-6 text-zinc-500 hover:text-zinc-100 text-2xl transition-colors">✕</button>
      <div id="cart-main-view">
        <h2 class="text-xl font-black mb-8 tracking-[0.2em] text-center text-zinc-50 uppercase">ВЫБРАННЫЕ АРТИКУЛЫ</h2>
        <div id="cart-items" class="space-y-8"></div>
        <div class="mt-10 border-t border-zinc-900 pt-8">
          <button onclick="openCheckoutForm()" id="checkout-btn" class="w-full py-5 bg-zinc-100 text-black text-xs font-black tracking-[0.2em] hover:bg-black hover:text-white hover:border hover:border-zinc-700 transition-all duration-300 uppercase">
            ОФОРМИТЬ ЗАКАЗ СИСТЕМЫ
          </button>
        </div>
      </div>
      <div id="cart-checkout-view" class="hidden">
        <h2 class="text-xl font-black mb-2 tracking-[0.2em] text-center text-zinc-50 uppercase">ИДЕНТИФИКАЦИЯ</h2>
        <p class="text-zinc-500 text-center text-xs tracking-wider mb-8">Оставьте свои координаты для подтверждения заказа</p>
        <div class="space-y-6">
          <div>
            <label class="block text-[10px] font-black text-zinc-400 mb-2 tracking-widest uppercase">TELEGRAM USERNAME</label>
            <input type="text" id="cust-tg" placeholder="@OPIUM_CRW" class="w-full bg-zinc-950 border border-zinc-800 px-4 py-4 text-sm text-zinc-100 focus:outline-none focus:border-zinc-500 font-bold tracking-wider">
          </div>
          <div>
            <label class="block text-[10px] font-black text-zinc-400 mb-2 tracking-widest uppercase">НОМЕР ТЕЛЕФОНА</label>
            <input type="text" id="cust-phone" placeholder="+380..." class="w-full bg-zinc-950 border border-zinc-800 px-4 py-4 text-sm text-zinc-100 focus:outline-none focus:border-zinc-500 font-bold tracking-wider">
          </div>
        </div>
        <div class="mt-10 flex gap-4">
          <button onclick="backToCartItems()" class="w-1/3 py-4 border border-zinc-850 text-zinc-400 text-xs font-bold hover:text-white hover:border-zinc-600 transition-all uppercase">
            НАЗАД
          </button>
          <button onclick="submitOrder()" id="submit-order-btn" class="w-2/3 py-4 bg-zinc-100 text-black font-black text-xs tracking-[0.15em] hover:bg-black hover:text-white hover:border hover:border-zinc-700 transition-all duration-300 flex items-center justify-center gap-2 uppercase">
            ОТПРАВИТЬ ЗАПРОС
          </button>
        </div>
      </div>
      <div id="cart-success-view" class="hidden text-center py-12">
        <div class="mb-6 inline-flex items-center justify-center w-16 h-16 border border-zinc-700 bg-zinc-900 text-zinc-100 text-3xl animate-pulse font-sans">
          †
        </div>
        <h2 class="text-2xl font-black mb-4 tracking-[0.15em] text-zinc-50 fade-in uppercase">ТРАНЗАКЦИЯ ПРИНЯТА</h2>
        <div class="space-y-3 max-w-sm mx-auto">
          <p class="text-zinc-400 text-xs tracking-wider leading-relaxed fade-in" style="animation-delay: 0.15s;">
            Наш куратор перехватит ваш Telegram в ближайшее время для подтверждения отправки архива.
          </p>
          <p class="text-zinc-600 text-[10px] tracking-[0.2em] pt-6 border-t border-zinc-900 uppercase font-black fade-in" style="animation-delay: 0.3s;">
            DEAD ARCHIVE // SYSTEM OK
          </p>
        </div>
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
          if (el && data.online !== undefined) {
            el.textContent = data.online;
          }
        })
        .catch(() => {});
      }
      sendHeartbeat();
      setInterval(sendHeartbeat, 4000);
    }
    function playGlitchSound() {
      try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        oscillator.type = 'square';
        oscillator.frequency.setValueAtTime(120, audioCtx.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 0.08);
        gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        oscillator.start();
        oscillator.stop(audioCtx.currentTime + 0.08);
      } catch(e) {}
    }
    function updateCartUI() {
      const countEl = document.getElementById('count');
      if (countEl) countEl.textContent = cart.length;
      const container = document.getElementById('cart-items');
      if (!container) return;
      container.innerHTML = '';
      if (cart.length === 0) {
        container.innerHTML = '<p class="text-zinc-600 text-center py-12 text-xs font-bold tracking-widest">АРХИВНОЕ ХРАНИЛИЩЕ ПУСТО</p>';
        const btn = document.getElementById('checkout-btn');
        if(btn) btn.style.display = 'none';
        return;
      } else {
        const btn = document.getElementById('checkout-btn');
        if(btn) btn.style.display = 'block';
      }
      cart.forEach((item, i) => {
        const div = document.createElement('div');
        div.className = "flex gap-6 border-b border-zinc-900 pb-6 items-center fade-in";
        const imgUrl = (item.images && item.images.length > 0) ? item.images[0] : '';
        div.innerHTML = `
          <img src="${imgUrl}" class="w-16 h-20 object-cover border border-zinc-800 transition-all duration-500">
          <div class="flex-1 min-w-0">
            <p class="font-black text-xs tracking-wider text-zinc-100 truncate uppercase">${item.name || 'АРТИКУЛ'}</p>
            <p class="text-zinc-400 text-xs mt-1 font-bold">${item.price_eur || 0} EUR</p>
            <p class="text-[10px] text-zinc-500 tracking-wider mt-2 font-bold uppercase">РАЗМЕР // [${item.selectedSize || 'L'}]</p>
          </div>
          <button onclick="removeFromCart(${i})" class="text-zinc-600 hover:text-zinc-200 text-xl transition-colors px-2">✕</button>
        `;
        container.appendChild(div);
      });
    }
    function toggleCart() {
      playGlitchSound();
      document.getElementById('cart-modal').classList.toggle('hidden');
      resetCartViews();
      updateCartUI();
    }
    function removeFromCart(i) {
      playGlitchSound();
      cart.splice(i, 1);
      localStorage.setItem('cart', JSON.stringify(cart));
      updateCartUI();
    }
    function openCheckoutForm() {
      playGlitchSound();
      if (cart.length === 0) return;
      document.getElementById('cart-main-view').classList.add('hidden');
      document.getElementById('cart-checkout-view').classList.remove('hidden');
    }
    function backToCartItems() {
      playGlitchSound();
      document.getElementById('cart-checkout-view').classList.add('hidden');
      document.getElementById('cart-main-view').classList.remove('hidden');
    }
    function resetCartViews() {
      document.getElementById('cart-success-view').classList.add('hidden');
      document.getElementById('cart-checkout-view').classList.add('hidden');
      document.getElementById('cart-main-view').classList.remove('hidden');
    }
    function submitOrder() {
      const tg = document.getElementById('cust-tg').value.trim();
      const phone = document.getElementById('cust-phone').value.trim();
      const btn = document.getElementById('submit-order-btn');
      if (!tg && !phone) return;
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner"></span> ШИФРОВАНИЕ СИСТЕМЫ...';
      playGlitchSound();
      fetch('/create_order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          items: cart,
          contacts: { telegram: tg, phone: phone }
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setTimeout(() => {
            let myOrders = JSON.parse(localStorage.getItem('my_orders')) || [];
            if (data.order_id) {
              myOrders.push(data.order_id);
              localStorage.setItem('my_orders', JSON.stringify(myOrders));
            }

            cart = [];
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartUI();
            document.getElementById('cust-tg').value = '';
            document.getElementById('cust-phone').value = '';
            btn.disabled = false;
            btn.innerText = 'ОТПРАВИТЬ ЗАПРОС';
            document.getElementById('cart-checkout-view').classList.add('hidden');
            document.getElementById('cart-success-view').classList.remove('hidden');
            playGlitchSound();
            setTimeout(playGlitchSound, 1500);
            setTimeout(() => {
              const modal = document.getElementById('cart-modal');
              if(!modal.classList.contains('hidden')) {
                toggleCart();
              }
            }, 4500);
          }, 1500);
        } else {
          alert(data.error || "Ошибка сохранения заказа");
          btn.disabled = false;
          btn.innerText = 'ОТПРАВИТЬ ЗАПРОС';
        }
      })
      .catch(error => {
        btn.disabled = false;
        btn.innerText = 'ОТПРАВИТЬ ЗАПРОС';
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
    online_count = get_real_online_count()
    return jsonify({"online": online_count})

@app.route('/')
def home():
    return render_template_string(HTML_HEADER + '''
  <section class="h-screen flex items-center justify-center bg-cover bg-center relative" style="background-image: url('https://kappa.lol/1edKYn')">
    <div class="absolute inset-0 bg-black/90"></div>
    <div class="relative text-center z-10 px-6">
      <h1 class="text-4xl md:text-[6.5rem] gothic tracking-[0.25em] text-zinc-100 leading-none">DEAD ARCHIVE</h1>
      <p class="text-xs tracking-[0.4em] text-zinc-500 mt-10 font-black uppercase">ПРОТОКОЛ СИСТЕМЫ DE-2026 // ПРИВАТНЫЙ ДРОП</p>
      <div class="mt-20 flex flex-wrap justify-center gap-6">
        <a href="/shop" onclick="playGlitchSound()" class="px-12 py-5 border border-zinc-800 hover:border-zinc-300 hover:bg-zinc-100 hover:text-black text-xs tracking-[0.3em] transition-all duration-500 text-zinc-100 font-black uppercase">ВОЙТИ В МАГАЗИН</a>
        <a href="/lookbook" onclick="playGlitchSound()" class="px-12 py-5 bg-red-950/40 border border-red-900 hover:bg-red-900 hover:text-white text-xs tracking-[0.3em] transition-all duration-500 text-zinc-200 font-black uppercase">LOOKBOOK // СТАЙЛИНГ</a>
      </div>
    </div>
  </section>
''' + HTML_FOOTER)

@app.route('/shop')
def shop():
    return render_template_string(HTML_HEADER + '''
  <section class="pt-40 pb-24 px-6 max-w-7xl mx-auto">
    <h2 class="text-2xl gothic text-center mb-16 tracking-[0.3em] text-zinc-100">КОЛЛЕКЦИЯ</h2>
    <div class="flex justify-center gap-6 mb-16 flex-wrap text-[10px] tracking-[0.25em] font-black uppercase">
      <button onclick="filterCategory('all')" id="btn-all" class="category-btn pb-2 border-b-2 border-zinc-100 text-zinc-100 transition-all">ВСЕ ПРЕДМЕТЫ</button>
      <button onclick="filterCategory('tshirts')" id="btn-tshirts" class="category-btn pb-2 border-b-2 border-transparent text-zinc-500 hover:text-zinc-200 transition-all">ФУТБОЛКИ</button>
      <button onclick="filterCategory('outerwear')" id="btn-outerwear" class="category-btn pb-2 border-b-2 border-transparent text-zinc-500 hover:text-zinc-200 transition-all">ВЕРХНЯЯ ОДЕЖДА</button>
      <button onclick="filterCategory('accessories')" id="btn-accessories" class="category-btn pb-2 border-b-2 border-transparent text-zinc-500 hover:text-zinc-200 transition-all">АКСЕССУАРЫ</button>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-6 gap-y-12" id="grid"></div>
  </section>
  <script>
    const products = {{ products|tojson|safe }};
    let currentCategory = 'all';
    const selectedSizes = {};

    function selectSize(productId, size, btn) {
      selectedSizes[productId] = size;
      document.querySelectorAll('.size-btn-' + productId).forEach(b => {
        b.classList.remove('bg-zinc-100', 'text-black', 'border-zinc-100');
        b.classList.add('bg-zinc-900', 'text-zinc-400', 'border-zinc-800');
      });
      btn.classList.remove('bg-zinc-900', 'text-zinc-400', 'border-zinc-800');
      btn.classList.add('bg-zinc-100', 'text-black', 'border-zinc-100');
      
      const sizeWarn = document.getElementById('size-warn-' + productId);
      if (sizeWarn) sizeWarn.classList.add('hidden');
    }

    function renderProducts() {
      const grid = document.getElementById('grid');
      grid.innerHTML = '';
      const filtered = currentCategory === 'all' ? products : products.filter(p => p.category === currentCategory);
      if(filtered.length === 0) {
        grid.innerHTML = '<p class="text-zinc-600 text-center col-span-4 py-20 text-xs font-bold tracking-widest">СЕГМЕНТ КОЛЛЕКЦИИ ПУСТ</p>';
        return;
      }
      filtered.forEach(p => {
        const div = document.createElement('div');
        div.className = "group relative cursor-pointer flex flex-col justify-between bg-zinc-950 border border-zinc-900 p-4 fade-in transition-all duration-500 hover:shadow-[0_0_20px_rgba(127,29,29,0.45)] hover:border-red-950";
        
        let sizesHtml = '<div class="flex gap-1.5 mt-3 flex-wrap" onclick="event.stopPropagation()">';
        p.sizes.forEach(sz => {
          sizesHtml += `<button type="button" onclick="selectSize(${p.id}, '${sz}', this)" class="size-btn-${p.id} px-2.5 py-1 text-[9px] font-black border border-zinc-800 bg-zinc-900 text-zinc-400 hover:border-zinc-500 transition-all uppercase">${sz}</button>`;
        });
        sizesHtml += '</div>';

        div.innerHTML = `
          <div>
            <div class="overflow-hidden bg-[#0a0a0a] aspect-[3/4] border border-zinc-900">
              <img src="${p.images[0]}" class="w-full h-full object-cover group-hover:brightness-75 group-hover:scale-110 transition-all duration-700 ease-out">
            </div>
            <div class="mt-4 space-y-1">
              <h3 class="text-xs font-black tracking-wider text-zinc-300 uppercase group-hover:text-zinc-50 transition-colors">${p.name}</h3>
              <p class="text-xs text-zinc-500 font-bold">${p.price_eur} EUR</p>
              <p class="text-[10px] text-zinc-500 leading-relaxed pt-2 border-t border-zinc-900/60 font-medium">${p.description || ''}</p>
            </div>
            <div class="mt-3">
              <p class="text-[9px] font-black text-zinc-500 uppercase tracking-wider">ВЫБЕРИТЕ РАЗМЕР:</p>
              ${sizesHtml}
              <p id="size-warn-${p.id}" class="hidden text-[9px] text-red-500 font-bold mt-1.5 uppercase tracking-wider">! ВЫБЕРИТЕ РАЗМЕР</p>
            </div>
          </div>
          <button onclick="event.stopPropagation(); addToCart(${p.id}, this)" class="mt-6 w-full py-3.5 border border-zinc-900 text-zinc-400 group-hover:border-red-900 group-hover:text-zinc-100 transition-all duration-500 text-[10px] font-black tracking-[0.2em] uppercase">
            ДОБАВИТЬ В КОРЗИНУ
          </button>
        `;
        grid.appendChild(div);
      });
    }

    function addToCart(productId, btnElement) {
      const item = products.find(p => p.id === productId);
      const chosenSize = selectedSizes[productId];

      if (!chosenSize) {
        playGlitchSound();
        const sizeWarn = document.getElementById('size-warn-' + productId);
        if (sizeWarn) sizeWarn.classList.remove('hidden');
        return;
      }

      if (item) {
        playGlitchSound();

        if (btnElement) {
          const origText = btnElement.innerText;
          btnElement.innerText = '✓ ДОБАВЛЕНО В КОРЗИНУ';
          btnElement.classList.add('bg-zinc-100', 'text-black', 'border-zinc-100');
          setTimeout(() => {
            btnElement.innerText = origText;
            btnElement.classList.remove('bg-zinc-100', 'text-black', 'border-zinc-100');
          }, 1200);
        }

        const navCartBtn = document.getElementById('cart-nav-btn');
        if (navCartBtn) {
          navCartBtn.classList.remove('cart-bounce');
          void navCartBtn.offsetWidth;
          navCartBtn.classList.add('cart-bounce');
        }

        cart.push({ ...item, selectedSize: chosenSize });
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartUI();
      }
    }

    function filterCategory(cat) {
      playGlitchSound();
      currentCategory = cat;
      document.querySelectorAll('.category-btn').forEach(b => {
        b.classList.remove('border-zinc-100', 'text-zinc-100');
        b.classList.add('border-transparent', 'text-zinc-500');
      });
      const activeBtn = document.getElementById('btn-' + cat);
      if(activeBtn) {
        activeBtn.classList.add('border-zinc-100', 'text-zinc-100');
        activeBtn.classList.remove('border-transparent', 'text-zinc-500');
      }
      renderProducts();
    }
    window.addEventListener('DOMContentLoaded', renderProducts);
  </script>
''' + HTML_FOOTER, products=app.products_data)

@app.route('/lookbook')
def lookbook():
    return render_template_string(HTML_HEADER + '''
  <section class="pt-40 pb-24 px-6 max-w-7xl mx-auto">
    <div class="text-center max-w-3xl mx-auto mb-20">
      <span class="text-[10px] font-black tracking-[0.3em] text-red-600 uppercase">LIVE ACTIVITY STATUS // STYLING PROTOCOL</span>
      <h2 class="text-3xl md:text-5xl gothic tracking-[0.2em] text-zinc-100 mt-4 mb-6">LOOKBOOK // СТАЙЛИНГ</h2>
      <p class="text-xs text-zinc-500 tracking-widest leading-relaxed uppercase">
        Авангардные комбинации предметов из архива 2026 года.
      </p>
    </div>
    <div class="space-y-32">
      {% for lb in lookbooks %}
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center bg-zinc-950/60 border border-zinc-900 p-8">
        <div class="lg:col-span-6 overflow-hidden border border-zinc-800">
          <img src="{{ lb.image }}" class="w-full h-[600px] object-cover hover:scale-105 transition-all duration-700">
        </div>
        <div class="lg:col-span-6 space-y-8">
          <div>
            <span class="text-[10px] text-zinc-500 font-black tracking-widest uppercase">[ ГОТОВЫЙ СЕТ // ARCHIVE SET ]</span>
            <h3 class="text-2xl font-black text-zinc-100 tracking-wider uppercase mt-2">{{ lb.title }}</h3>
            <p class="text-xs text-zinc-400 mt-4 tracking-wider leading-relaxed font-medium">{{ lb.concept }}</p>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </section>
''' + HTML_FOOTER, lookbooks=lookbooks, products=app.products_data)

@app.route('/history')
def history():
    return render_template_string(HTML_HEADER + '''
  <section class="pt-40 pb-24 px-6 max-w-5xl mx-auto min-h-screen">
    <div class="text-center max-w-2xl mx-auto mb-16">
      <h2 class="text-3xl gothic tracking-[0.25em] text-zinc-100 mb-3">ИСТОРИЯ ЗАКАЗОВ</h2>
      <p class="text-xs text-zinc-500 tracking-widest uppercase font-bold">Статус транзакций твоего аккаунта</p>
    </div>

    <div id="history-container" class="space-y-8">
      <p class="text-center text-xs text-zinc-600 font-bold tracking-widest py-12 uppercase">ЗАГРУЗКА ДАННЫХ ИЗ СИСТЕМЫ...</p>
    </div>
  </section>

  <script>
    function loadOrderHistory() {
      const container = document.getElementById('history-container');
      const myOrderIds = JSON.parse(localStorage.getItem('my_orders')) || [];

      if (myOrderIds.length === 0) {
        container.innerHTML = `
          <div class="bg-zinc-950 border border-zinc-900 p-12 text-center">
            <p class="text-xs text-zinc-600 font-black tracking-widest uppercase">У ВАС ПОКА НЕТ АКТИВНЫХ ИЛИ СТАРЫХ ЗАКАЗОВ</p>
            <a href="/shop" class="inline-block mt-6 px-8 py-3 bg-zinc-900 border border-zinc-800 text-zinc-200 text-[10px] font-black tracking-widest hover:bg-zinc-100 hover:text-black transition-all uppercase">ПЕРЕЙТИ В МАГАЗИН</a>
          </div>
        `;
        return;
      }

      fetch('/get_user_orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ids: myOrderIds })
      })
      .then(res => res.json())
      .then(orders => {
        if (!orders || orders.length === 0) {
          container.innerHTML = `
            <div class="bg-zinc-950 border border-zinc-900 p-12 text-center">
              <p class="text-xs text-zinc-600 font-black tracking-widest uppercase">ЗАКАЗЫ НЕ НАЙДЕНЫ В БАЗЕ СЕРВЕРА</p>
              <p class="text-[10px] text-zinc-700 mt-2 font-bold uppercase">(Сервер был перезапущен и временная память очистилась)</p>
            </div>
          `;
          return;
        }

        container.innerHTML = '';
        orders.reverse().forEach(order => {
          const div = document.createElement('div');
          div.className = "bg-zinc-950 border border-zinc-800 p-6 md:p-8 space-y-6 fade-in";
          
          let itemsHtml = '';
          (order.items || []).forEach(item => {
            itemsHtml += `
              <div class="flex justify-between items-center text-xs border-b border-zinc-900/80 pb-2">
                <span class="text-zinc-300 font-bold uppercase">${item.name} <span class="text-zinc-500">([${item.selectedSize || 'L'}])</span></span>
                <span class="text-zinc-400 font-mono">${item.price_eur} EUR</span>
              </div>
            `;
          });

          const tgVal = (order.contacts && order.contacts.telegram) ? order.contacts.telegram : '—';
          const phoneVal = (order.contacts && order.contacts.phone) ? order.contacts.phone : '—';

          div.innerHTML = `
            <div class="flex flex-col md:flex-row justify-between md:items-center gap-4 border-b border-zinc-900 pb-4">
              <div>
                <span class="text-xs font-black bg-zinc-800 text-zinc-200 px-3 py-1">ЗАКАЗ #${order.id}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-[10px] text-zinc-500 font-black uppercase tracking-wider">СТАТУС:</span>
                <span class="text-xs font-black uppercase tracking-widest px-3 py-1 bg-red-950/40 border border-red-900 text-red-200">${order.status || 'В обработке'}</span>
              </div>
            </div>

            <div class="space-y-3">
              <p class="text-[10px] text-zinc-500 font-black uppercase tracking-wider">АРТИКУЛЫ В ЗАКАЗЕ:</p>
              ${itemsHtml}
            </div>

            <div class="flex justify-between items-center pt-4 border-t border-zinc-900">
              <div class="text-[10px] text-zinc-500 uppercase font-bold">
                TG: ${tgVal} // ТЕЛ: ${phoneVal}
              </div>
              <div class="text-sm font-black text-zinc-100 tracking-wider">
                ИТОГО: ${order.total} EUR
              </div>
            </div>
          `;
          container.appendChild(div);
        });
      })
      .catch(() => {
        container.innerHTML = '<p class="text-center text-xs text-red-500 font-bold uppercase">ОШИБКА ЗАГРУЗКИ ИСТОРИИ</p>';
      });
    }

    window.addEventListener('DOMContentLoaded', loadOrderHistory);
  </script>
''' + HTML_FOOTER)

@app.route('/create_order', methods=['POST'])
def create_order():
    try:
        data = request.get_json(silent=True) or {}
        items = data.get('items', [])
        contacts = data.get('contacts', {})
        
        if not items:
            return jsonify({"success": False, "error": "Корзина пуста"}), 400
            
        total_price = 0
        for item in items:
            if isinstance(item, dict):
                price = item.get('price_eur', 0)
                try:
                    total_price += int(price)
                except (ValueError, TypeError):
                    pass
        
        order_id = len(app.orders_data) + 1
        new_order = {
            "id": order_id,
            "items": items,
            "contacts": contacts,
            "total": total_price,
            "status": "В обработке",
            "timestamp": time.time()
        }
        
        app.orders_data.append(new_order)
        return jsonify({"success": True, "order_id": order_id})
    except Exception as e:
        print(f"CRITICAL ORDER ERROR: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/get_user_orders', methods=['POST'])
def get_user_orders():
    data = request.get_json(silent=True) or {}
    ids = data.get('ids', [])
    user_orders = [o for o in app.orders_data if o.get('id') in ids]
    return jsonify(user_orders)

# Регистрация админки
try:
    from admin_routes import admin_bp
    app.register_blueprint(admin_bp)
except Exception as e:
    print(f"Ошибка загрузки админ-панели: {e}")

if __name__ == '__main__':
    app.run(debug=True)
