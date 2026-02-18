import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = "8043005903:AAFhvV-I7GPkWs5hVFlHYJVXy-6Rvx0QXA0"
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_limits = {}
FREE_LIMIT = 10
PHOTOS_PER_REQUEST = 5


def search_photos(query):
    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": query,
        "per_page": PHOTOS_PER_REQUEST
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    photos = []
    for photo in data.get("photos", []):
        photos.append(photo["src"]["large"])

    return photos


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "👁 Напиши запрос для поиска референсов.\n\n"
        "Бесплатно: 10 запросов по 5 фото."
    )


@dp.message()
async def search(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_limits:
        user_limits[user_id] = 0

    if user_limits[user_id] >= FREE_LIMIT:
        await message.answer(
            "🚫 Лимит бесплатных запросов закончился.\n\n"
            "Купи PRO ⭐"
        )
        return

    user_limits[user_id] += 1

    photos = search_photos(message.text)

    if not photos:
        await message.answer("Ничего не найдено 😢")
        return

    media = [types.InputMediaPhoto(media=p) for p in photos]
    await message.answer_media_group(media)

    remaining = FREE_LIMIT - user_limits[user_id]
    await message.answer(f"Осталось бесплатных запросов: {remaining}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
