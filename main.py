import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик сообщений
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Привет! Ты написал: {message.text}")

# Health-check
async def health(request):
    return web.Response(text="OK")

async def main():
    # Запускаем aiogram polling в отдельной задаче
    asyncio.create_task(dp.start_polling(bot))

    # Поднимаем aiohttp сервер для health-check
    app = web.Application()
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8000)))
    await site.start()

    # Чтобы main не завершался
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
