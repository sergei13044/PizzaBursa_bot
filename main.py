import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# токен берем из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
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
    "Дюшес": {"price": 315, "desc": "Сливочный сыр, жареный бекон, груша, мёд, соус 'Ранч', корица, сыр 'Моцарелла'"}
}

# --- Соусы ---
sauces = ["🧀 Сырный", "🍖 Барбекю", "🤔 Чесночный", "🥫 Кетчуп", "🍮 Кисло-сладкий", "🌭 Горчичный"]

# Хранилище для выбора пользователя
user_choice = {}

# --- Стартовое меню ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = [[KeyboardButton(text=pizza)] for pizza in pizzas.keys()]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Добро пожаловать в Pizza Bursa! 🍕\nВыберите пиццу:", reply_markup=keyboard)

# --- Обработка выбора пиццы ---
@dp.message(F.text.in_(pizzas.keys()))
async def choose_pizza(message: types.Message):
    pizza = message.text
    user_choice[message.from_user.id] = {"pizza": pizza}

    kb = [[KeyboardButton(text=sauce)] for sauce in sauces]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer(
        f"Вы выбрали пиццу <b>{pizza}</b> за {pizzas[pizza]['price']} руб.\n"
        f"Состав: {pizzas[pizza]['desc']}\n\nТеперь выберите соус (бесплатно):",
        parse_mode="HTML",
        reply_markup=keyboard
    )

# --- Обработка выбора соуса ---
@dp.message(F.text.in_(sauces))
async def choose_sauce(message: types.Message):
    sauce = message.text
    user_choice[message.from_user.id]["sauce"] = sauce

    pizza = user_choice[message.from_user.id]["pizza"]
    await message.answer(
        f"✅ Отличный выбор!\nВы заказали: <b>{pizza}</b> + {sauce}\n\nВаш заказ передан на кухню! 👨‍🍳",
        parse_mode="HTML"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
