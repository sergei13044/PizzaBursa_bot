import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = f"https://empty-flora-bursa-b920ea75.koyeb.app/webhook"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Хэндлеры сообщений ---
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Привет! Ты написал: {message.text}")

# --- Webhook handler ---
async def handle_webhook(request: web.Request):
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    return web.Response()

# --- Healthcheck для UptimeRobot ---
async def healthcheck(request):
    return web.Response(text="I’m alive ✅")

# --- Startup & Shutdown ---
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

# --- MAIN ---
def main():
    app = web.Application()
    app.router.add_get("/", healthcheck)   # проверка для UptimeRobot
    app.router.add_post("/webhook", handle_webhook)  # Telegram webhook
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

if __name__ == "__main__":
    main()
