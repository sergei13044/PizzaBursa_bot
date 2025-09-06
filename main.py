import asyncio
import os
from aiogram import Bot, Dispatcher, types

# Получаем токен из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")

# Создаём экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик всех сообщений
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Привет! Ты написал: {message.text}")

# Главная функция запуска
async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
