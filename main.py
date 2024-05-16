import os
import asyncio
from aiogram import Bot, Dispatcher

from handlers import router

TOKEN = os.getenv("TELEGRAM_API_TOKEN")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
