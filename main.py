# main.py
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в переменных окружения")

# --- BOT SETUP ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Меню пицц ---
pizzas = {
    "Маргарита": {"price": 195, "desc": "Пицца-соус, много сыра 'Моцарелла', орегано"},
    "Гавайская": {"price": 295, "desc": "Пицца-соус, ананас, ветчина, сыр 'Моцарелла'"},
    "Цыплёнок Барбекю": {"price": 295, "desc": "Соус барбекю, красный лук, цыпленок, бекон, сыр 'Моцарелла'"},
    "Грибная": {"price": 250, "desc": "Чесночный соус, шампиньоны, ветчина, сыр 'Моцарелла'"},
    "Сырная курочка": {"price": 315, "desc": "Сырный соус, Цыпленок, много сыра 'Моцарелла', кунжутные бортики"},
    "Пепперони": {"price": 295, "desc": "Пицца-соус, колбаски 'Пепперони', много сыра 'Моцарелла'"},
    "Фирменная Prosto": {"price": 295, "desc": "Пицца-соус, шампиньоны, сладкий перец, красный лук, маслины, цыпленок, колбаски 'Пепперони', сыр 'Моцарелла'"},
    "Двойная Пепперони": {"price": 315, "desc": "Пицца-соус, сыр Моцарелла, колбаски Пепперони"},
    "Кантри": {"price": 315, "desc": "Соус Сырный, ветчина, омлет, шампиньоны, томаты, сыр Моцарелла, бекон"},
    "Средиземная": {"price": 335, "desc": "Пицца-соус, томаты, шампиньоны, сладкий перец, красный лук, орегано, сыр 'Фета', маслины, сыр 'Моцарелла'"},
    "Чикен Ранч": {"price": 315, "desc": "Соус 'Ранч', Томаты, Чеснок, Цыпленок, Ветчина, Сыр 'Моцарелла'"},
    "Четыре сыра": {"price": 315, "desc": "Пицца-соус, сыр 'Фета', Сливочный сыр, Пармезан, сыр 'Моцарелла'"},
    "Мясная": {"price": 315, "desc": "Пицца-соус, колбаски 'Пепперони', говядина, ветчина, бекон, Сыр 'Моцарелла'"},
    "Бьянка": {"price": 335, "desc": "Чесночный соус, шпинат, шампиньоны, цыпленок, сливочный сыр, Пармезан, сыр 'Моцарелла'"},
    "Техас": {"price": 335, "desc": "Пицца-соус, томаты, сладкий перец, красный лук, острые перчики Халапеньо, говядина, сыр 'Моцарелла'"},
    "Морская": {"price": 335, "desc": "Соус 'Ранч', красный лук, маслины, 'снежный краб', креветка, сыр 'Моцарелла'"},
    "Чизбургер": {"price": 335, "desc": "Сырный соус, томаты, красный лук, маринованные огурчики, говядина, бекон, сыр 'Моцарелла', кунжутные бортики"},
    "Альма": {"price": 315, "desc": "Чесночный соус, соус 'Пармеджано', цыпленок, шпинат, цветная капуста, сыр 'Моцарелла'"},
    "Дюшес": {"price": 315, "desc": "Сливочный сыр, жареный бекон, груша, мёд, соус 'Ранч', корица, сыр 'Моцарелла'"},
}

# --- Соусы ---
sauces = ["🧀 Сырный", "🍖 Барбекю", "🤔 Чесночный", "🥫 Кетчуп", "🍮 Кисло-сладкий", "🌭 Горчичный"]

# Временное in-memory хранилище заказов (поменять на БД позже)
user_orders = {}

# --- Утилиты — клавиатуры ---
def pizza_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for name in pizzas.keys():
        kb.add(KeyboardButton(text=name))
    return kb

def sauce_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for s in sauces:
        kb.add(KeyboardButton(text=s))
    return kb

# --- HANDLERS ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = "👋 Привет! Добро пожаловать в PizzaBursa.\n\nВыберите пиццу из списка или напишите /menu"
    await message.answer(text, reply_markup=pizza_keyboard())

@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    # Покажем короткий список + клавиатуру выбора
    text = "🍕 Вы можете заказать следующие пиццы:\n\n"
    for name, v in pizzas.items():
        text += f"{name} — {v['price']} ₽\nСостав: {v['desc']}\n\n"
    text += "Выберите из меню ниже или напишите название пиццы."
    await message.answer(text, reply_markup=pizza_keyboard())

# Выбор пиццы (сообщение текстом совпадающее с ключом словаря)
@dp.message(F.text.in_(pizzas.keys()))
async def on_choose_pizza(message: types.Message):
    user_id = message.from_user.id
    pizza_name = message.text
    user_orders[user_id] = {"pizza": pizza_name}
    info = pizzas[pizza_name]
    await message.answer(
        f"Вы выбрали: *{pizza_name}* — {info['price']} ₽\n\nСостав: {info['desc']}\n\n"
        "Теперь выберите соус (идёт бесплатно):",
        parse_mode="Markdown",
        reply_markup=sauce_keyboard()
    )

# Выбор соуса
@dp.message(F.text.in_(sauces))
async def on_choose_sauce(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_orders or "pizza" not in user_orders[user_id]:
        await message.answer("Сначала выберите пиццу. Напишите /menu", reply_markup=ReplyKeyboardRemove())
        return

    sauce = message.text
    user_orders[user_id]["sauce"] = sauce
    pizza = user_orders[user_id]["pizza"]
    price = pizzas[pizza]["price"]

    # Формируем подтверждение заказа (потом можно отправлять админу и в БД)
    await message.answer(
        f"✅ Заказ принят!\n\n🍕 Пицца: *{pizza}* — {price} ₽\n🥫 Соус: {sauce}\n\n"
        "Спасибо! Ваш заказ передан на сборку. Если хотите ещё — /menu",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )

# Ловим все остальные тексты (необязательно)
@dp.message()
async def fallback(message: types.Message):
    await message.answer("Не понял. Напишите /menu чтобы открыть список пицц.", reply_markup=pizza_keyboard())

# --- Healthcheck (для Koyeb) ---
async def handle_health(request):
    return web.Response(text="OK")

async def start_health_server():
    app = web.Application()
    app.router.add_get("/health", handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info("Health server started on port %s", port)

# --- MAIN ---
async def main():
    # Удаляем старый webhook (если остался) — это важно, чтобы избежать конфликтов
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Old webhook deleted (if existed).")
    except Exception as e:
        logger.warning("Не удалось удалить webhook: %s", e)

    # Запускаем health-server (Koyeb будет видеть, что сервис жив)
    await start_health_server()

    # Запускаем polling (всё остальное работает в фоне)
    logger.info("Start polling")
    # start_polling будет работать в текущем loop и не мешает aiohttp серверу
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        logger.info("Shutting down")
