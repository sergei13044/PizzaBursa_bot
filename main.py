import asyncio
import os

from aiohttp import web

async def healthcheck(request):
    return web.Response(text="I’m alive ✅")

def main():
    app = web.Application()
    app.router.add_get("/", healthcheck)   # для UptimeRobot
    app.router.add_post("/webhook", handle_webhook)  # твой Telegram webhook
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

from aiogram import Bot, Dispatcher, types

# Твой токен из переменных окружения Koyeb
TOKEN = os.getenv("BOT_TOKEN")

# Адрес, куда Telegram будет слать апдейты
WEBHOOK_HOST = "https://empty-flora-bursa-b920ea75.koyeb.app"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Привет! Ты написал: {message.text}")


async def on_startup(app):
    # Удаляем старый вебхук и ставим новый с таймаутом
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL, request_timeout=60)


async def on_shutdown(app):
    await bot.session.close()


async def handle(request):
    update = types.Update(**await request.json())
    await dp.feed_update(bot, update)
    return web.Response()


def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))


if __name__ == "__main__":
    main()
