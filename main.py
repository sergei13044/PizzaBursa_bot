import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_TOKEN = os.getenv("BOT_TOKEN")  # токен из переменных окружения

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Меню пицц ---
pizzas = {
    "Маргарита": "195 рублей\nСостав: Пицца-соус, много сыра 'Моцарелла', орегано",
    "Гавайская": "295 рублей\nСостав: Пицца-соус, ананас, ветчина, сыр 'Моцарелла'",
    "Цыплёнок Барбекю": "295 рублей\nСостав: Соус барбекю, красный лук, цыпленок, бекон, сыр 'Моцарелла'",
    "Грибная": "250 рублей\nСостав: Чесночный соус, шампиньоны, ветчина, сыр 'Моцарелла'",
    "Сырная курочка": "315 рублей\nСостав: Сырный соус, Цыпленок, много сыра 'Моцарелла', кунжутные бортики",
    "Пепперони": "295 рублей\nСостав: Пицца-соус, колбаски 'Пепперони', много сыра 'Моцарелла'",
    "Фирменная Prosto": "295 рублей\nСостав: Пицца-соус, шампиньоны, сладкий перец, красный лук, маслины, цыпленок, колбаски 'Пепперони', сыр 'Моцарелла'",
    "Двойная Пепперони": "315 рублей\nСостав: Пицца-соус, сыр Моцарелла, колбаски Пепперони",
    "Кантри": "315 рублей\nСостав: Соус Сырный, ветчина, омлет, шампиньоны, томаты, сыр Моцарелла, бекон",
    "Средиземная": "335 рублей\nСостав: Пицца-соус, томаты, шампиньоны, сладкий перец, красный лук, орегано, сыр 'Фета', маслины, сыр 'Моцарелла'",
    "Чикен Ранч": "315 рублей\nСостав: Соус 'Ранч', томаты, чеснок, цыпленок, ветчина, сыр 'Моцарелла'",
    "Четыре сыра": "315 рублей\nСостав: Пицца-соус, сыр 'Фета', сливочный сыр, Пармезан, сыр 'Моцарелла'",
    "Мясная": "315 рублей\nСостав: Пицца-соус, колбаски 'Пепперони', говядина, ветчина, бекон, сыр 'Моцарелла'",
    "Бьянка": "335 рублей\nСостав: Чесночный соус, шпинат, шампиньоны, цыпленок, сливочный сыр, Пармезан, сыр 'Моцарелла'",
    "Техас": "335 рублей\nСостав: Пицца-соус, томаты, сладкий перец, красный лук, острые перчики Халапеньо, говядина, сыр 'Моцарелла'",
    "Морская": "335 рублей\nСостав: Соус 'Ранч', красный лук, маслины, 'снежный краб', креветка, сыр 'Моцарелла'",
    "Чизбургер": "335 рублей\nСостав: Сырный соус, томаты, красный лук, маринованные огурчики, говядина, бекон, сыр 'Моцарелла', кунжутные бортики",
    "Альма": "315 рублей\nСостав: Чесночный соус, соус 'Пармеджано', цыпленок, шпинат, цветная капуста, сыр 'Моцарелла'",
    "Дюшес": "315 рублей\nСостав: Сливочный сыр, жареный бекон, груша, мёд, соус 'Ранч', корица, сыр 'Моцарелла'",
}

# --- Соусы ---
sauces = ["🧀 Сырный", "🍖 Барбекю", "🤔 Чесночный", "🥫 Кетчуп", "🍮 Кисло-сладкий", "🌭 Горчичный"]


@dp.message(commands=["start"])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for pizza in pizzas.keys():
        keyboard.add(InlineKeyboardButton(pizza, callback_data=f"pizza_{pizza}"))
    await message.answer("🍕 Вы можете заказать следующие пиццы из списка:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data.startswith("pizza_"))
async def choose_pizza(callback: types.CallbackQuery):
    pizza_name = callback.data.replace("pizza_", "")
    description = pizzas[pizza_name]

    # показать описание выбранной пиццы
    await callback.message.answer(
        f"✅ Вы выбрали пиццу: *{pizza_name}*\n\n{description}", parse_mode="Markdown"
    )

    # предложить соус
    keyboard = InlineKeyboardMarkup(row_width=2)
    for sauce in sauces:
        keyboard.add(InlineKeyboardButton(sauce, callback_data=f"sauce_{sauce}_{pizza_name}"))
    await callback.message.answer("Выберите бесплатный соус к пицце:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data.startswith("sauce_"))
async def choose_sauce(callback: types.CallbackQuery):
    _, sauce, pizza_name = callback.data.split("_", 2)
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Вернуться к меню", callback_data="back_to_menu"))
    await callback.message.answer(
        f"🎉 Заказ принят!\n\n🍕 Пицца: *{pizza_name}*\n🥫 Соус: *{sauce}*", 
        parse_mode="Markdown",
        reply_markup=keyboard
    )


@dp.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for pizza in pizzas.keys():
        keyboard.add(InlineKeyboardButton(pizza, callback_data=f"pizza_{pizza}"))
    await callback.message.answer("🍕 Вы вернулись в меню. Выберите пиццу:", reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
