import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types

# Логирование (чтобы видеть ошибки)
logging.basicConfig(level=logging.INFO)

# Токен берем из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Не найден BOT_TOKEN в переменных окружения")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Привет! Ты написал: {message.text}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
