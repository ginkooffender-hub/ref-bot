import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = os.getenv("8043005903:AAFhvV-I7GPkWs5hVFlHYJVXy-6Rvx0QXA0")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Напиши запрос для поиска референсов 👁")

@dp.message()
async def search(message: types.Message):
    photos = [
        "https://picsum.photos/500/500?1",
        "https://picsum.photos/500/500?2",
        "https://picsum.photos/500/500?3",
        "https://picsum.photos/500/500?4",
        "https://picsum.photos/500/500?5",
        "https://picsum.photos/500/500?6",
    ]

    media = [types.InputMediaPhoto(media=p) for p in photos]
    await message.answer_media_group(media)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
