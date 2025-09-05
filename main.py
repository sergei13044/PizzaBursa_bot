import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://{os.getenv('KOYEB_APP_NAME')}.koyeb.app{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# --- Хэндлеры ---
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я твой PizzaBursa бот 🍕")


@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")


# --- Webhook ---
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()


async def handle_webhook(request):
    update = types.Update(**await request.json())
    await dp.feed_update(bot, update)
    return web.Response()


def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))


if __name__ == "__main__":
    main()
