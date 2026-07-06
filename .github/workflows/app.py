from flask import Flask, render_template_string, request, jsonify
import json
import os

app = Flask(__name__)

# Товары (добавил 12 штук)
products = [
    {"id": 1, "name": "Oversized Crucifix Hoodie", "price_eur": 185, "price_uah": 8900, "images": ["https://picsum.photos/id/1015/800/800"]},
    {"id": 2, "name": "Chrome Cross Leather Jacket", "price_eur": 420, "price_uah": 19900, "images": ["https://picsum.photos/id/106/800/800"]},
    {"id": 3, "name": "Black Mass T-Shirt", "price_eur": 95, "price_uah": 4500, "images": ["https://picsum.photos/id/201/800/800"]},
    {"id": 4, "name": "Opium Archive Pants", "price_eur": 220, "price_uah": 10500, "images": ["https://picsum.photos/id/133/800/800"]},
    {"id": 5, "name": "Silver Cross Chain", "price_eur": 85, "price_uah": 4100, "images": ["https://picsum.photos/id/180/800/800"]},
    {"id": 6, "name": "Death Ritual Cap", "price_eur": 75, "price_uah": 3600, "images": ["https://picsum.photos/id/107/800/800"]},
    {"id": 7, "name": "Grave Leather Shirt", "price_eur": 135, "price_uah": 6500, "images": ["https://picsum.photos/id/201/800/800"]},
    {"id": 8, "name": "Chrome Heart Ring", "price_eur": 120, "price_uah": 5800, "images": ["https://picsum.photos/id/133/800/800"]},
    {"id": 9, "name": "Black Ritual Jacket", "price_eur": 380, "price_uah": 17900, "images": ["https://picsum.photos/id/106/800/800"]},
    {"id": 10, "name": "Gothic Archive Bag", "price_eur": 190, "price_uah": 9100, "images": ["https://picsum.photos/id/1015/800/800"]},
    {"id": 11, "name": "Heavy Chain Necklace", "price_eur": 140, "price_uah": 6700, "images": ["https://picsum.photos/id/180/800/800"]},
    {"id": 12, "name": "Skull Patch Hoodie", "price_eur": 165, "price_uah": 7900, "images": ["https://picsum.photos/id/201/800/800"]},
]

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>DEAD ARCHIVE</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
  <style>
    body { background:#020202; color:#ddd; }
    .gothic { font-family:'Cinzel',serif; }
    .card { transition: all 0.6s ease; }
    .card:hover { transform: translateY(-15px); }
  </style>
</head>
<body>
  <nav class="fixed top-0 w-full bg-black/95 py-6 border-b border-white/10 z-50">
    <div class="max-w-7xl mx-auto px-6 flex justify-between items-center">
      <h1 onclick="location.href='/'" class="text-4xl gothic cursor-pointer">DEAD ARCHIVE</h1>
      <div class="flex gap-8 text-sm uppercase tracking-widest">
        <a href="/" class="hover:text-white">Главная</a>
        <a href="/about" class="hover:text-white">О Нас</a>
        <a href="/support" class="hover:text-white">Поддержка</a>
        <button onclick="toggleCart()" class="hover:text-white">Корзина (<span id="count">0</span>)</button>
      </div>
    </div>
  </nav>
  <!-- Интро -->
  <section class="h-screen flex items-center justify-center bg-cover bg-center relative" style="background-image: url('https://kappa.lol/1edKYn')">
    <div class="absolute inset-0 bg-black/70"></div>
    <div class="relative text-center z-10 px-6">
      <h1 class="text-8xl md:text-[9rem] gothic tracking-widest">DEAD ARCHIVE</h1>
      <p class="text-2xl gothic tracking-widest text-gray-400 mt-6">ARCHIVE OF FORGOTTEN LUXURY</p>
      <button onclick="document.getElementById('collection').scrollIntoView({behavior: 'smooth'})"
              class="mt-16 px-12 py-5 border border-white/40 hover:bg-white hover:text-black text-lg">ENTER THE ARCHIVE</button>
    </div>
  </section>
  <!-- Коллекция -->
  <section id="collection" class="py-20 px-6 max-w-7xl mx-auto">
    <h2 class="text-5xl gothic text-center mb-16">THE COLLECTION</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8" id="grid"></div>
  </section>
  <!-- Корзина -->
  <div id="cart-modal" class="hidden fixed inset-0 bg-black/90 flex items-center justify-center z-50">
    <div class="bg-zinc-950 w-full max-w-lg p-8 border border-white/20 max-h-[90vh] overflow-auto">
      <h2 class="gothic text-3xl mb-8">YOUR ARCHIVE</h2>
      <div id="cart-items" class="space-y-6"></div>
      <button onclick="showCheckout()" class="mt-10 w-full py-7 bg-white text-black text-lg">ОФОРМИТЬ ЗАКАЗ</button>
    </div>
  </div>
  <!-- НОРМАЛЬНОЕ ОФОРМЛЕНИЕ ЗАКАЗА -->
  <div id="checkout-modal" class="hidden fixed inset-0 bg-black/90 flex items-center justify-center z-[100]">
    <div class="bg-zinc-950 border border-white/20 w-full max-w-md p-8">
      <h2 class="gothic text-3xl mb-8">ОФОРМЛЕНИЕ ЗАКАЗА</h2>
      <input id="name" placeholder="Имя и фамилия" class="w-full p-4 mb-4 bg-transparent border border-white/30 focus:border-white rounded">
      <input id="phone" placeholder="Телефон" class="w-full p-4 mb-4 bg-transparent border border-white/30 focus:border-white rounded">
      <input id="address" placeholder="Полный адрес доставки" class="w-full p-4 mb-8 bg-transparent border border-white/30 focus:border-white rounded">
      <button onclick="submitOrder()" class="w-full py-7 bg-red-900 hover:bg-red-800 text-white text-lg">ЗАВЕРШИТЬ ЗАКАЗ</button>
      <button onclick="hideCheckout()" class="mt-4 w-full py-3 text-gray-400">Назад в корзину</button>
    </div>
  </div>
  <script>
    let cart = [];
    const products = {{ products|tojson|safe }};
    function renderProducts() {
      const grid = document.getElementById('grid');
      grid.innerHTML = '';
      products.forEach(p => {
        const div = document.createElement('div');
        div.className = "bg-zinc-950 border border-white/10 p-4 card cursor-pointer";
        div.innerHTML = `
          <img src="${p.images[0]}" class="w-full h-80 object-cover">
          <h3 class="mt-4">${p.name}</h3>
          <p class="text-xl">${p.price_eur} €</p>
          <button onclick="event.stopImmediatePropagation(); addToCart(${p.id});" class="mt-6 w-full py-4 border border-white/30 hover:bg-white hover:text-black">В КОРЗИНУ</button>
        `;
        div.onclick = () => location.href = `/product/${p.id}`;
        grid.appendChild(div);
      });
    }
    function addToCart(id) {
      const p = products.find(x => x.id === id);
      cart.push(p);
      document.getElementById('count').textContent = cart.length;
      const notif = document.createElement('div');
      notif.className = "fixed bottom-8 right-8 bg-green-900 px-8 py-4 rounded-xl border border-green-700";
      notif.textContent = p.name + " добавлен в корзину";
      document.body.appendChild(notif);
      setTimeout(() => notif.remove(), 2200);
    }
    function toggleCart() {
      document.getElementById('cart-modal').classList.toggle('hidden');
      updateCart();
    }
    function updateCart() {
      const container = document.getElementById('cart-items');
      container.innerHTML = '';
      cart.forEach((item, i) => {
        const div = document.createElement('div');
        div.className = "flex gap-4 border-b border-white/10 pb-4";
        div.innerHTML = `<img src="${item.images[0]}" class="w-20 h-20 object-cover"><div><p>${item.name}</p><p>${item.price_eur} €</p></div><button onclick="removeFromCart(${i})" class="ml-auto text-red-500">×</button>`;
        container.appendChild(div);
      });
    }
    function removeFromCart(i) {
      cart.splice(i, 1);
      updateCart();
      document.getElementById('count').textContent = cart.length;
    }
    function showCheckout() {
      toggleCart();
      document.getElementById('checkout-modal').classList.remove('hidden');
    }
    function hideCheckout() {
      document.getElementById('checkout-modal').classList.add('hidden');
    }
    function submitOrder() {
      const name = document.getElementById('name').value.trim();
      if (!name) return alert("Введите имя");
      alert("✅ Заказ успешно оформлен! Спасибо.");
      cart = [];
      document.getElementById('count').textContent = "0";
      hideCheckout();
    }
    window.onload = renderProducts;
  </script>
</body>
</html>
''', products=products)

@app.route('/product/<int:pid>')
def product_detail(pid):
    product = next((p for p in products if p['id'] == pid), None)
    if not product: return "Не найдено", 404
    return render_template_string('''
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{{ product.name }} — DEAD ARCHIVE</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>body { background:#020202; color:#ddd; }</style>
</head>
<body>
  <div class="max-w-6xl mx-auto p-8">
    <a href="/" class="text-gray-400">← Назад</a>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 mt-12">
      <div>
        {% for img in product.images %}
        <img src="{{ img }}" class="w-full mb-4 border border-white/10">
        {% endfor %}
      </div>
      <div>
        <h1 class="text-5xl">{{ product.name }}</h1>
        <p class="text-3xl mt-6">{{ product.price_eur }} € • {{ product.price_uah }} ₴</p>
        <button onclick="addToCart()" class="mt-16 w-full py-8 bg-white text-black text-xl">ДОБАВИТЬ В КОРЗИНУ</button>
      </div>
    </div>
  </div>
  <script>function addToCart(){ alert("Добавлено в корзину"); }</script>
</body>
</html>
''', product=product)

@app.route('/about')
def about():
    return render_template_string('''
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>О Нас — DEAD ARCHIVE</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
  <style>body { background:#020202; color:#bbb; }</style>
</head>
<body>
  <div class="max-w-4xl mx-auto px-6 py-32 text-center">
    <h1 class="text-7xl gothic mb-16">DEAD ARCHIVE</h1>
    <p class="text-xl max-w-2xl mx-auto leading-relaxed">Мы храним тьму, которую другие боятся носить. Забытая роскошь, кресты, хром и опиумный вайб — всё это здесь.</p>
    <a href="/" class="block mt-20 text-gray-400 hover:text-white">← Вернуться в Архив</a>
  </div>
</body>
</html>
''')

@app.route('/support')
def support():
    return render_template_string('''
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Поддержка — DEAD ARCHIVE</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
  <style>body { background:#020202; color:#bbb; }</style>
</head>
<body>
  <div class="max-w-4xl mx-auto px-6 py-32 text-center">
    <h1 class="text-7xl gothic mb-16">ПОДДЕРЖКА</h1>
    <p class="text-xl">Если что-то пошло не так — пиши нам.</p>
    <div class="mt-12 bg-zinc-950 border border-white/10 p-12">
      <p>Telegram: @deadarchive_support</p>
      <p class="mt-4">Email: shadow@deadarchive.ru</p>
    </div>
    <a href="/" class="block mt-20 text-gray-400 hover:text-white">← Вернуться в Архив</a>
  </div>
</body>
</html>
''')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)