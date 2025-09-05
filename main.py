import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import os

# токен лучше хранить в переменной окружения
API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message()
async def echo(message: Message):
    await message.answer(f"Привет! Ты написал: {message.text}")

async def main():
    # запуск через polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
