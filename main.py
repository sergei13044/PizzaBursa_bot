import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "pizzabursa")  # ключ безопасности
APP_URL = os.getenv("APP_URL")  # твой домен с Koyeb (например https://pizza-bot.koyeb.app)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# обработчик сообщений
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Привет! Ты написал: {message.text}")


# обработчик входящих запросов от Telegram
async def handle(request: web.Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response()


async def on_startup(app):
    # Устанавливаем webhook
    await bot.set_webhook(f"{APP_URL}/{WEBHOOK_SECRET}")


async def on_shutdown(app):
    await bot.delete_webhook()


def main():
    app = web.Application()
    app.router.add_post(f"/{WEBHOOK_SECRET}", handle)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))


if __name__ == "__main__":
    main()
