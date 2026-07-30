from flask import Flask, render_template_string, request, jsonify, redirect, url_for, session
import time

app = Flask(__name__)
app.secret_key = 'dead_archive_secret_key_2026'

# Глобальные защищенные хранилища данных
GLOBAL_ORDERS = []
ACTIVE_SESSIONS = {}
ONLINE_TIMEOUT = 10

GLOBAL_PRODUCTS = [
    {
        "id": 1, 
        "name": "ФУТБОЛКА VET@MENTS ANTISOCIAL", 
        "category": "tshirts", 
        "price_eur": 60, 
        "price_uah": 3050, 
        "images": [
            "https://kappa.lol/zlEwzv",
            "https://kappa.lol/34ieZw",
            "https://kappa.lol/gJtShU"
        ], 
        "description": "Оверсайз силуэт. Тяжелый премиальный хлопок. Архивный графический принт на груди.", 
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "id": 2, 
        "name": "ФУТБОЛКА VET@MENTS.COM", 
        "category": "tshirts", 
        "price_eur": 60, 
        "price_uah": 3050, 
        "images": [
            "https://kappa.lol/34ieZw", 
            "https://kappa.lol/gJtShU", 
            "https://kappa.lol/nrpVrs", 
            "https://kappa.lol/xtkDjf"
        ], 
        "description": "Классический свободный крой. Дистресс-эффект с потертостями по краям. Фирменная вышивка на спине.", 
        "sizes": ["S", "M", "L"]
    },
    {
        "id": 3, 
        "name": "ФУТБОЛКА VET@MENTS VITAL EXISTENCE", 
        "category": "tshirts", 
        "price_eur": 60, 
        "price_uah": 3050, 
        "images": [
            "https://kappa.lol/61Hm4e",
            "https://kappa.lol/wZhp55"
        ], 
        "description": "Готический шрифтовой принт. Заниженная линия плеча, плотный воротник.", 
        "sizes": ["M", "L", "XL"]
    },
    {
        "id": 4, 
        "name": "ФУТБОЛКА VET@MENTS I GOT LUCKY", 
        "category": "tshirts", 
        "price_eur": 60, 
        "price_uah": 3050, 
        "images": [
            "https://kappa.lol/wZhp55",
            "https://kappa.lol/61Hm4e"
        ], 
        "description": "Лимитированное издание. Необработанный сырой край подола.", 
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "id": 9, 
        "name": "ХУДИ VET@MENTS OVERSIZED METAL", 
        "category": "outerwear", 
        "price_eur": 110, 
        "price_uah": 5300, 
        "images": [
            "https://picsum.photos/id/338/800/800",
            "https://picsum.photos/id/339/800/800",
            "https://picsum.photos/id/340/800/800"
        ], 
        "description": "Супер-тяжелый френч терри хлопок (700г/м²). Металлический шрифтовой принт, глубокий капюшон-балаклава.", 
        "sizes": ["M", "L", "XL"]
    },
    {
        "id": 10, 
        "name": "ЛОНГСЛИВ ANTISOCIAL ZIP", 
        "category": "tshirts", 
        "price_eur": 70, 
        "price_uah": 3400, 
        "images": [
            "https://picsum.photos/id/684/800/800",
            "https://picsum.photos/id/685/800/800"
        ], 
        "description": "Удлиненные рукава с потайными металлическими молниями YKK. Двойной воротник, архивные швы наружу.", 
        "sizes": ["S", "M", "L"]
    },
    {
        "id": 11, 
        "name": "ФУТБОЛКА VET@MENTS TOTAL DARKNESS", 
        "category": "tshirts", 
        "price_eur": 65, 
        "price_uah": 3150, 
        "images": [
            "https://picsum.photos/id/222/800/800",
            "https://picsum.photos/id/223/800/800"
        ], 
        "description": "Эффект сильной стирки (acid wash) до винтажного графитового оттенка. Ручные прорези и дыры на плечах.", 
        "sizes": ["M", "L", "XL", "XXL"]
    },
    {
        "id": 5, 
        "name": "СЕРЕБРЯНАЯ ЦЕПЬ С КРЕСТОМ", 
        "category": "accessories", 
        "price_eur": 85, 
        "price_uah": 4100, 
        "images": [
            "https://picsum.photos/id/180/800/800",
            "https://picsum.photos/id/181/800/800"
        ], 
        "description": "Массивное серебро .925 пробы. Детализированный авангардный крест в готическом стиле.", 
        "sizes": ["ONE SIZE"]
    },
    {
        "id": 6, 
        "name": "КЕПКА DEATH RITUAL", 
        "category": "accessories", 
        "price_eur": 75, 
        "price_uah": 3600, 
        "images": [
            "https://picsum.photos/id/107/800/800",
            "https://picsum.photos/id/108/800/800"
        ], 
        "description": "Плотный вареный хлопок черного цвета. Вышитая ритуальная графика. Металлическая застежка.", 
        "sizes": ["ONE SIZE"]
    },
    {
        "id": 7, 
        "name": "КОЖАНАЯ РУБАШКА GRAVE", 
        "category": "outerwear", 
        "price_eur": 135, 
        "price_uah": 6500, 
        "images": [
            "https://picsum.photos/id/201/800/800",
            "https://picsum.photos/id/202/800/800",
            "https://picsum.photos/id/203/800/800"
        ], 
        "description": "Премиальная эко-кожа повышенной плотности с эффектом естественного старения. Укороченный boxy-крой.", 
        "sizes": ["M", "L"]
    },
    {
        "id": 8, 
        "name": "КОЛЬЦО CHROME HEART", 
        "category": "accessories", 
        "price_eur": 120, 
        "price_uah": 5800, 
        "images": [
            "https://picsum.photos/id/133/800/800",
            "https://picsum.photos/id/134/800/800"
        ], 
        "description": "Тяжелый ювелирный сплав. Детальная гравировка в виде геральдических крестов.", 
        "sizes": ["ONE SIZE"]
    },
    {
        "id": 12, 
        "name": "СЕРЕБРЯНЫЙ БРАСЛЕТ OPIUM LINK", 
        "category": "accessories", 
        "price_eur": 95, 
        "price_uah": 4600, 
        "images": [
            "https://picsum.photos/id/435/800/800",
            "https://picsum.photos/id/436/800/800"
        ], 
        "description": "Плетение из массивных якорных звеньев с чернением. Замок-тогл с выгравированной готической символикой.", 
        "sizes": ["ONE SIZE"]
    },
]

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

def get_real_online_count():
    now = time.time()
    expired_clients = [cid for cid, last_seen in ACTIVE_SESSIONS.items() if now - last_seen > ONLINE_TIMEOUT]
    for cid in expired_clients:
        del ACTIVE_SESSIONS[cid]
    return len(ACTIVE_SESSIONS)

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

    .blood-logo:hover .drop-1 { left: 12%; animation: drip 1.4s infinite cubic-bezier(0.55, 0.085, 0.68, 0.53) 0.1s; }
    .blood-logo:hover .drop-2 { left: 38%; animation: drip 1.8s infinite cubic-bezier(0.55, 0.085, 0.68, 0.53) 0.4s; }
    .blood-logo:hover .drop-3 { left: 65%; animation: drip 1.5s infinite cubic-bezier(0.55, 0.085, 0.68, 0.53) 0.25s; }
    .blood-logo:hover .drop-4 { left: 88%; animation: drip 1.6s infinite cubic-bezier(0.55, 0.085, 0.68, 0.53) 0.5s; }

    @keyframes drip {
      0% { height: 0px; transform: translateY(0); opacity: 0; }
      30% { height: 14px; opacity: 1; }
      80% { height: 22px; transform: translateY(28px); opacity: 0.8; }
      100% { height: 2px; transform: translateY(40px); opacity: 0; }
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
    ::-webkit-scrollbar { width: 6px; height: 6px; }
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

    function switchProductImage(productId, imgUrl, thumbElement) {
      const mainImg = document.getElementById('zoom-img-' + productId);
      if (mainImg) {
        mainImg.src = imgUrl;
      }
      const thumbContainer = thumbElement.parentElement;
      thumbContainer.querySelectorAll('img').forEach(img => {
        img.classList.remove('border-zinc-100', 'opacity-100');
        img.classList.add('border-zinc-800', 'opacity-60');
      });
      thumbElement.classList.remove('border-zinc-800', 'opacity-60');
      thumbElement.classList.add('border-zinc-100', 'opacity-100');
    }

    function handleImageZoom(e, id) {
      const container = document.getElementById('zoom-container-' + id);
      const img = document.getElementById('zoom-img-' + id);
      const rect = container.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / container.offsetWidth) * 100;
      const y = ((e.clientY - rect.top) / container.offsetHeight) * 100;
      
      img.style.transformOrigin = `${x}% ${y}%`;
      img.style.transform = "scale(2.2)";
    }

    function resetImageZoom(id) {
      const img = document.getElementById('zoom-img-' + id);
      img.style.transformOrigin = "center center";
      img.style.transform = "scale(1)";
    }

    function handleWheelZoom(event, id) {
      event.preventDefault();
      const img = document.getElementById('zoom-img-' + id);
      let currentScale = parseFloat(img.style.transform.replace('scale(', '').replace(')', '')) || 1;
      
      if (event.deltaY < 0) {
        currentScale += 0.2;
      } else {
        currentScale -= 0.2;
      }
      
      currentScale = Math.min(Math.max(1, currentScale), 3.5);
      img.style.transform = `scale(${currentScale})`;
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
        if (p.sizes && p.sizes.length > 0) {
          p.sizes.forEach(sz => {
            sizesHtml += `<button type="button" onclick="selectSize(${p.id}, '${sz}', this)" class="size-btn-${p.id} px-2.5 py-1 text-[9px] font-black border border-zinc-800 bg-zinc-900 text-zinc-400 hover:border-zinc-500 transition-all uppercase">${sz}</button>`;
          });
        }
        sizesHtml += '</div>';

        let thumbsHtml = '';
        if (p.images && p.images.length > 1) {
          thumbsHtml = '<div class="flex gap-2 mt-2 overflow-x-auto py-1" onclick="event.stopPropagation()">';
          p.images.forEach((imgUrl, index) => {
            const activeClass = index === 0 ? 'border-zinc-100 opacity-100' : 'border-zinc-800 opacity-60';
            thumbsHtml += `<img src="${imgUrl}" onclick="switchProductImage(${p.id}, '${imgUrl}', this)" class="w-10 h-12 object-cover border cursor-pointer hover:opacity-100 transition-all flex-shrink-0 ${activeClass}">`;
          });
          thumbsHtml += '</div>';
        }

        const mainImgUrl = (p.images && p.images.length > 0) ? p.images[0] : '';

        div.innerHTML = `
          <div>
            <div class="overflow-hidden bg-[#0a0a0a] aspect-[3/4] border border-zinc-900 relative cursor-crosshair flex items-center justify-center" 
                 id="zoom-container-${p.id}" 
                 onmousemove="handleImageZoom(event, ${p.id})" 
                 onmouseleave="resetImageZoom(${p.id})"
                 onwheel="handleWheelZoom(event, ${p.id})">
              <img src="${mainImgUrl}" id="zoom-img-${p.id}" class="max-w-full max-h-full object-cover transition-transform duration-100 ease-out select-none" style="transform: scale(1);">
              <div class="absolute bottom-2 right-2 bg-black/80 border border-zinc-800 text-[9px] text-zinc-400 px-1.5 py-0.5 uppercase tracking-widest pointer-events-none">
                ZOOM // WHEEL
              </div>
            </div>
            ${thumbsHtml}
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
''' + HTML_FOOTER, products=GLOBAL_PRODUCTS)

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
''' + HTML_FOOTER, lookbooks=lookbooks, products=GLOBAL_PRODUCTS)

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
      .then(data => {
        if (!data.orders || data.orders.length === 0) {
          container.innerHTML = '<p class="text-center text-xs text-zinc-600 font-bold tracking-widest py-12 uppercase">НЕТ ДАННЫХ О ТРАНЗАКЦИЯХ В БАЗЕ</p>';
          return;
        }

        container.innerHTML = '';
        data.orders.forEach(ord => {
          let itemsHtml = '';
          if (ord.items) {
            ord.items.forEach(it => {
              itemsHtml += `
                <div class="flex justify-between items-center text-xs border-b border-zinc-900/60 pb-3">
                  <span class="text-zinc-300 font-bold uppercase">${it.name} <span class="text-[10px] text-zinc-500">[${it.selectedSize || 'L'}]</span></span>
                  <span class="text-zinc-400 font-mono">${it.price_eur} EUR</span>
                </div>
              `;
            });
          }

          const div = document.createElement('div');
          div.className = "bg-zinc-950 border border-zinc-900 p-6 space-y-4 fade-in";
          div.innerHTML = `
            <div class="flex justify-between items-center pb-4 border-b border-zinc-900">
              <span class="text-xs font-mono font-black text-zinc-400">ЗАКАЗ #${ord.id}</span>
              <span class="text-[10px] px-2.5 py-1 bg-zinc-900 border border-zinc-800 text-zinc-300 font-black uppercase tracking-wider">${ord.status || 'В ОБРАБОТКЕ'}</span>
            </div>
            <div class="space-y-3 py-2">
              ${itemsHtml}
            </div>
            <div class="flex justify-between items-center pt-2 text-xs font-bold text-zinc-400">
              <span>КОНТАКТ: ${(ord.contacts && (ord.contacts.telegram || ord.contacts.phone)) || '—'}</span>
              <span class="text-zinc-100 font-mono font-black">${ord.total_eur} EUR</span>
            </div>
          `;
          container.appendChild(div);
        });
      })
      .catch(() => {
        container.innerHTML = '<p class="text-center text-xs text-red-500 font-bold tracking-widest py-12 uppercase">ОШИБКА СВЯЗИ С СИСТЕМОЙ</p>';
      });
    }

    window.addEventListener('DOMContentLoaded', loadOrderHistory);
  </script>
''' + HTML_FOOTER)

# --- УДОБНАЯ И СОВРЕМЕННАЯ АДМИН-ПАНЕЛЬ ---

@app.route('/admin/', methods=['GET', 'POST'])
def admin_dashboard():
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'dead2026':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'НЕВЕРНЫЙ ПАРОЛЬ ДОСТУПА'

    if not session.get('admin_logged_in'):
        return render_template_string(HTML_HEADER + '''
          <section class="h-screen flex items-center justify-center px-6">
            <div class="bg-zinc-950 border border-zinc-900 p-10 max-w-md w-full space-y-6 shadow-2xl">
              <div class="text-center">
                <span class="text-[10px] text-red-500 font-black tracking-widest uppercase">RESTRICTED AREA</span>
                <h2 class="text-2xl gothic tracking-[0.2em] text-zinc-100 mt-2">АДМИНИСТРАТИВНЫЙ ДОСТУП</h2>
              </div>
              {% if error %}
              <div class="bg-red-950/40 border border-red-900 text-red-400 text-xs text-center py-3 font-bold tracking-wider uppercase">
                {{ error }}
              </div>
              {% endif %}
              <form method="POST" class="space-y-4">
                <div>
                  <label class="block text-[9px] font-black text-zinc-500 uppercase mb-2">ПАРОЛЬ СИСТЕМЫ</label>
                  <input type="password" name="password" required class="w-full bg-zinc-900 border border-zinc-800 px-4 py-3 text-sm text-zinc-100 focus:outline-none focus:border-zinc-500 tracking-widest">
                </div>
                <button type="submit" class="w-full py-4 bg-zinc-100 text-black text-xs font-black tracking-widest uppercase hover:bg-black hover:text-white hover:border hover:border-zinc-700 transition-all">ВОЙТИ В ПАНЕЛЬ</button>
              </form>
            </div>
          </section>
        ''' + HTML_FOOTER, error=error)

    # Вычисляем общую выручку для дашборда
    total_revenue = sum(ord.get('total_eur', 0) for ord in GLOBAL_ORDERS)

    # Проверяем, передан ли ID товара для редактирования
    edit_id = request.args.get('edit', type=int)
    product_to_edit = None
    if edit_id:
        for p in GLOBAL_PRODUCTS:
            if p['id'] == edit_id:
                product_to_edit = p
                break

    return render_template_string(HTML_HEADER + '''
  <section class="pt-32 pb-24 px-6 max-w-7xl mx-auto min-h-screen">
    <!-- Шапка панели управления -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 border-b border-zinc-900 pb-6 gap-4">
      <div>
        <span class="text-[10px] text-red-500 font-black tracking-widest uppercase">CONTROL PANEL // ADMIN SYSTEM v2.7</span>
        <h2 class="text-3xl gothic tracking-[0.2em] text-zinc-100 mt-1">ЦЕНТР УПРАВЛЕНИЯ</h2>
      </div>
      <div class="flex flex-wrap gap-3">
        <a href="/admin/export_orders" class="px-5 py-2.5 bg-zinc-900 border border-zinc-800 text-xs font-black tracking-widest text-zinc-300 hover:text-white hover:border-zinc-600 transition-all uppercase">ЭКСПОРТ JSON</a>
        <a href="/admin/logout" class="px-5 py-2.5 bg-red-950/40 border border-red-900 text-xs font-black tracking-widest text-red-400 hover:bg-red-900 hover:text-white transition-all uppercase">ВЫЙТИ</a>
      </div>
    </div>

    <!-- Статистика (Дашборд) -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-12">
      <div class="bg-zinc-950 border border-zinc-900 p-6">
        <p class="text-[10px] text-zinc-500 font-black tracking-widest uppercase">ВСЕГО ЗАКАЗОВ</p>
        <p class="text-3xl font-mono font-black text-zinc-100 mt-2">{{ orders|length }}</p>
      </div>
      <div class="bg-zinc-950 border border-zinc-900 p-6">
        <p class="text-[10px] text-zinc-500 font-black tracking-widest uppercase">ОБЩАЯ ВЫРУЧКА</p>
        <p class="text-3xl font-mono font-black text-zinc-100 mt-2">{{ total_revenue }} EUR</p>
      </div>
      <div class="bg-zinc-950 border border-zinc-900 p-6">
        <p class="text-[10px] text-zinc-500 font-black tracking-widest uppercase">ТОВАРОВ В КАТАЛОГЕ</p>
        <p class="text-3xl font-mono font-black text-zinc-100 mt-2">{{ products|length }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
      
      <!-- Секция заказов (Занимает 7 колонок) -->
      <div class="lg:col-span-7 space-y-6">
        <div class="flex justify-between items-center">
          <h3 class="text-sm font-black tracking-widest text-zinc-300 uppercase flex items-center gap-2">
            <span class="inline-block w-2 h-2 bg-red-600"></span> ЗАКАЗЫ КЛИЕНТОВ
          </h3>
        </div>

        <div class="space-y-4">
          {% for ord in orders %}
          <div class="bg-zinc-950 border border-zinc-900 p-6 space-y-4 transition-all hover:border-zinc-700">
            <div class="flex flex-wrap justify-between items-center pb-3 border-b border-zinc-900 gap-2">
              <div>
                <span class="text-xs font-mono font-black text-zinc-200">ЗАКАЗ ID: #{{ ord.id }}</span>
                <span class="text-[10px] text-zinc-500 ml-2 font-mono">{{ ord.total_eur }} EUR</span>
              </div>
              <form action="/admin/update_order_status" method="POST" class="flex gap-2 items-center">
                <input type="hidden" name="order_id" value="{{ ord.id }}">
                <select name="status" class="bg-zinc-900 border border-zinc-800 text-[10px] text-zinc-300 px-2.5 py-1.5 uppercase font-bold focus:outline-none focus:border-zinc-500">
                  <option value="ПРИНЯТ В ОБРАБОТКУ" {% if ord.status == 'ПРИНЯТ В ОБРАБОТКУ' %}selected{% endif %}>В ОБРАБОТКЕ</option>
                  <option value="СОБРАН И ОТПРАВЛЕН" {% if ord.status == 'СОБРАН И ОТПРАВЛЕН' %}selected{% endif %}>ОТПРАВЛЕН</option>
                  <option value="ОТМЕНЕН" {% if ord.status == 'ОТМЕНЕН' %}selected{% endif %}>ОТМЕНЕН</option>
                </select>
                <button type="submit" class="px-3 py-1.5 bg-zinc-100 text-black text-[10px] font-black uppercase hover:bg-black hover:text-white hover:border hover:border-zinc-600 transition-all">ИЗМЕНИТЬ</button>
              </form>
            </div>

            <div class="text-xs space-y-1 bg-zinc-900/40 p-3 border border-zinc-900">
              <p class="text-zinc-400 font-bold">TELEGRAM / ТЕЛЕФОН: <span class="text-zinc-100 font-mono">{{ (ord.contacts and (ord.contacts.telegram or ord.contacts.phone)) or '—' }}</span></p>
            </div>

            <div class="space-y-2 pt-1">
              <p class="text-[10px] font-black text-zinc-500 uppercase tracking-widest">СОСТАВ ЗАКАЗА:</p>
              {% if ord.items %}
                <div class="space-y-1.5">
                  {% for it in ord.items %}
                  <div class="text-xs flex justify-between items-center text-zinc-300 bg-zinc-900/60 px-3 py-2 border border-zinc-900">
                    <span class="uppercase font-bold truncate max-w-[280px]">{{ it.name }} <span class="text-zinc-500 text-[10px]">[{{ it.selectedSize or 'L' }}]</span></span>
                    <span class="font-mono text-zinc-400">{{ it.price_eur }} EUR</span>
                  </div>
                  {% endfor %}
                </div>
              {% endif %}
            </div>
          </div>
          {% else %}
          <div class="bg-zinc-950 border border-zinc-900 p-12 text-center">
            <p class="text-xs text-zinc-600 font-bold tracking-widest uppercase">АКТИВНЫХ ЗАКАЗОВ В БАЗЕ НЕТ</p>
          </div>
          {% endfor %}
        </div>
      </div>

      <!-- Секция товаров, добавления и редактирования (Занимает 5 колонок) -->
      <div class="lg:col-span-5 space-y-8">
        
        <!-- Форма добавления или редактирования товара -->
        <div class="bg-zinc-950 border border-zinc-900 p-6 space-y-4 shadow-xl">
          {% if product_to_edit %}
          <div class="flex justify-between items-center">
            <h3 class="text-xs font-black tracking-widest text-zinc-300 uppercase flex items-center gap-2">
              <span class="inline-block w-2 h-2 bg-yellow-500"></span> РЕДАКТИРОВАНИЕ ТОВАРА #{{ product_to_edit.id }}
            </h3>
            <a href="/admin/" class="text-[10px] text-zinc-500 hover:text-zinc-300 uppercase underline">ОТМЕНА</a>
          </div>
          <form action="/admin/edit_product" method="POST" class="space-y-4">
            <input type="hidden" name="product_id" value="{{ product_to_edit.id }}">
            <div>
              <label class="block text-[9px] font-black text-zinc-500 uppercase mb-1">НАЗВАНИЕ ТОВАРА</label>
              <input type="text" name="name" value="{{ product_to_edit.name }}" required class="w-full bg-zinc-900 border border-zinc-800 px-3 py-2.5 text-xs text-zinc-100 focus:outline-none focus:border-zinc-500 uppercase">
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-[9px] font-black text-zinc-500 uppercase mb-1">КАТЕГОРИЯ</label>
                <select name="category" class="w-full bg-zinc-900 border border-zinc-800 px-3 py-2.5 text-xs text-zinc-100 uppercase font-bold">
                  <option value="tshirts" {% if product_to_edit.category == 'tshirts' %}selected{% endif %}>ФУТБОЛКИ</option>
                  <option value="outerwear" {% if product_to_edit.category == 'outerwear' %}selected{% endif %}>ВЕРХНЯЯ ОДЕЖДА</option>
                  <option value="accessories" {% if product_to_edit.category == 'accessories' %}selected{% endif %}>АКСЕССУАРЫ</option>
                </select>
              </div>
              <div>
                <label class="block text-[9px] font-black text-zinc-500 uppercase mb-1">ЦЕНА (EUR)</label>
                <input type="number" name="price_eur" value="{{ product_to_edit.price_eur }}" required class="w-full bg-zinc-900 border border-zinc-800 px-3 py-2.5 text-xs text-zinc-100 font-mono">
              </div>
            </div>
            <div>
              <label class="block text-[9px] font-black text-zinc-500 uppercase mb-1">ССЫЛКИ НА ФОТО (ЧЕРЕЗ ЗАПЯТУЮ)</label>
              <input type="text" name="images" value="{{ ', '.join(product_to_edit.images) }}" required class="w-full bg-zinc-900 border border-zinc-800 px-3 py-2.5 text-xs text-zinc-100 font-mono">
            </div>
            <div>
              <label class="block text-[9px] font-black text-zinc-500 uppercase mb-1">ОПИСАНИЕ</label>
              <textarea name="description" rows="2" class="w-full bg-zinc-900 border border-zinc-800 px-3 py-2 text-xs text-zinc-100 focus:outline-none focus:border-zinc-500">{{ product_to_edit.description }}</textarea>
            </div>
            <button type="submit" class="w-full py-3.5 bg-yellow-500 text-black text-[10px] font-black tracking-widest uppercase hover:bg-yellow-400 transition-all">СОХРАНИТЬ ИЗМЕНЕНИЯ</button>
          </form>
          {% else %}
          <h3 class="text-xs font-black tracking-widest text-zinc-300 uppercase flex items-center gap-2">
            <span class="inline-block w-2 h-2 bg-zinc-100"></span> ДОБАВИТЬ ПРЕДМЕТ В АРХИВ
          </h3>
          <form action="/admin/add_product" method="POST" class="space-y-4">
            <div>
              <label class="block text-[9px] font-black text-zinc-500 uppercase mb-1">НАЗВАНИЕ ТОВАРА</label>
              <input type="text" name="name" required placeholder="НАПРИМЕР: ХУДИ OPIUM" class="w-full bg-zinc-900 border border-zinc-800 px-3 py-2.5 text-xs text-zinc-100 focus:outline-none focus:border-zinc-500 uppercase">
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-[9px] font-black text-zinc-500 uppercase mb-1">КАТЕГОРИЯ</label>
                <select name="category" class="w-full bg-zinc-900 border border-zinc-800 px-3 py-2.5 text-xs text-zinc-100 uppercase font-bold">
                  <option value="tshirts">ФУТБОЛКИ</option>
                  <option value="outerwear">ВЕРХНЯЯ ОДЕЖДА</option>
                  <option value="accessories">АКСЕССУАРЫ</option>
                </select>
              </div>
              <div>
                <label class="block text-[9px] font-black text-zinc-500 uppercase mb-1">ЦЕНА (EUR)</label>
                <input type="number" name="price_eur" required placeholder="65" class="w-full bg-zinc-900 border border-zinc-800 px-3 py-2.5 text-xs text-zinc-100 font-mono">
              </div>
            </div>
            <div>
              <label class="block text-[9px] font-black text-zinc-500 uppercase mb-1">ССЫЛКИ НА ФОТО (ЧЕРЕЗ ЗАПЯТУЮ)</label>
              <input type="text" name="images" placeholder="https://..., https://..." required class="w-full bg-zinc-900 border border-zinc-800 px-3 py-2.5 text-xs text-zinc-100 font-mono">
            </div>
            <div>
              <label class="block text-[9px] font-black text-zinc-500 uppercase mb-1">ОПИСАНИЕ</label>
              <textarea name="description" rows="2" placeholder="Оверсайз крой, плотный материал..." class="w-full bg-zinc-900 border border-zinc-800 px-3 py-2 text-xs text-zinc-100 focus:outline-none focus:border-zinc-500"></textarea>
            </div>
            <button type="submit" class="w-full py-3.5 bg-zinc-100 text-black text-[10px] font-black tracking-widest uppercase hover:bg-black hover:text-white hover:border hover:border-zinc-700 transition-all">ДОБАВИТЬ В КАТАЛОГ</button>
          </form>
          {% endif %}
        </div>

        <!-- Список товаров в каталоге с кнопками изменения и удаления -->
        <div class="bg-zinc-950 border border-zinc-900 p-6 space-y-4">
          <h3 class="text-xs font-black tracking-widest text-zinc-300 uppercase flex items-center justify-between">
            <span>АРХИВНЫЕ ТОВАРЫ</span>
            <span class="text-zinc-500 font-mono text-[10px]">{{ products|length }} ШТ.</span>
          </h3>
          <div class="space-y-3 max-h-[450px] overflow-auto pr-2">
            {% for p in products %}
            <div class="bg-zinc-900/40 border border-zinc-900 p-3 flex gap-3 items-center justify-between">
              <div class="flex items-center gap-3 min-w-0">
                <img src="{{ p.images[0] if p.images and p.images|length > 0 else '' }}" class="w-10 h-12 object-cover border border-zinc-800 flex-shrink-0">
                <div class="min-w-0">
                  <h4 class="text-xs font-black text-zinc-200 uppercase truncate">{{ p.name }}</h4>
                  <p class="text-[10px] text-zinc-500 font-mono mt-0.5">{{ p.price_eur }} EUR // {{ p.category }}</p>
                </div>
              </div>
              <div class="flex items-center gap-2 flex-shrink-0">
                <a href="/admin/?edit={{ p.id }}" class="px-2.5 py-2 border border-zinc-700 bg-zinc-900 text-zinc-300 hover:bg-zinc-100 hover:text-black text-[10px] font-black transition-all uppercase" title="Изменить товар">ИЗМЕНИТЬ</a>
                <form action="/admin/delete_product" method="POST" onsubmit="return confirm('Удалить товар из архива?');">
                  <input type="hidden" name="product_id" value="{{ p.id }}">
                  <button type="submit" class="p-2 border border-red-950 text-red-500 hover:bg-red-950 hover:text-white text-[10px] font-black transition-all" title="Удалить товар">✕</button>
                </form>
              </div>
            </div>
            {% endfor %}
          </div>
        </div>

      </div>

    </div>
  </section>
''' + HTML_FOOTER, orders=GLOBAL_ORDERS, products=GLOBAL_PRODUCTS, total_revenue=total_revenue, product_to_edit=product_to_edit)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update_order_status', methods=['POST'])
def update_order_status():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    try:
        order_id = int(request.form.get('order_id', 0))
    except ValueError:
        order_id = 0
    new_status = request.form.get('status', 'ПРИНЯТ В ОБРАБОТКУ')
    for ord in GLOBAL_ORDERS:
        if ord['id'] == order_id:
            ord['status'] = new_status
            break
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_product', methods=['POST'])
def delete_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    try:
        product_id = int(request.form.get('product_id', 0))
    except ValueError:
        product_id = 0
    global GLOBAL_PRODUCTS
    GLOBAL_PRODUCTS = [p for p in GLOBAL_PRODUCTS if p['id'] != product_id]
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_product', methods=['POST'])
def add_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    name = request.form.get('name')
    category = request.form.get('category')
    try:
        price_eur = int(request.form.get('price_eur', 0))
    except ValueError:
        price_eur = 0
        
    images_raw = request.form.get('images', '')
    images = [img.strip() for img in images_raw.split(',') if img.strip()]
    description = request.form.get('description', '')
    
    new_id = max([p['id'] for p in GLOBAL_PRODUCTS], default=0) + 1
    new_item = {
        "id": new_id,
        "name": name,
        "category": category,
        "price_eur": price_eur,
        "price_uah": price_eur * 50,
        "images": images if images else ["https://picsum.photos/id/10/800/800"],
        "description": description,
        "sizes": ["S", "M", "L", "XL"]
    }
    GLOBAL_PRODUCTS.append(new_item)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit_product', methods=['POST'])
def edit_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    try:
        product_id = int(request.form.get('product_id', 0))
    except ValueError:
        product_id = 0

    name = request.form.get('name')
    category = request.form.get('category')
    try:
        price_eur = int(request.form.get('price_eur', 0))
    except ValueError:
        price_eur = 0
        
    images_raw = request.form.get('images', '')
    images = [img.strip() for img in images_raw.split(',') if img.strip()]
    description = request.form.get('description', '')

    for p in GLOBAL_PRODUCTS:
        if p['id'] == product_id:
            p['name'] = name
            p['category'] = category
            p['price_eur'] = price_eur
            p['price_uah'] = price_eur * 50
            if images:
                p['images'] = images
            p['description'] = description
            break

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/export_orders')
def export_orders():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    return jsonify(GLOBAL_ORDERS)

@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json() or {}
    items = data.get('items', [])
    contacts = data.get('contacts', {})
    
    if not items:
        return jsonify({"success": False, "error": "Корзина пуста"})
    
    order_id = int(time.time())
    total_eur = sum(item.get('price_eur', 0) for item in items)
    
    order_record = {
        "id": order_id,
        "items": items,
        "contacts": contacts,
        "total_eur": total_eur,
        "status": "ПРИНЯТ В ОБРАБОТКУ"
    }
    
    GLOBAL_ORDERS.append(order_record)
    return jsonify({"success": True, "order_id": order_id})

@app.route('/get_user_orders', methods=['POST'])
def get_user_orders():
    data = request.get_json() or {}
    ids = data.get('ids', [])
    found = [o for o in GLOBAL_ORDERS if o['id'] in ids]
    return jsonify({"orders": found})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
