import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = "8043005903:AAFhvV-I7GPkWs5hVFlHYJVXy-6Rvx0QXA0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище лимитов
user_limits = {}

FREE_LIMIT = 10  # 10 запросов
PHOTOS_PER_REQUEST = 5  # 5 фото за раз

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "👁 Отправь запрос для поиска референсов.\n\n"
        "Бесплатно: 10 запросов по 5 фото."
    )

@dp.message()
async def search(message: types.Message):
    user_id = message.from_user.id

    # Если пользователя нет в словаре
    if user_id not in user_limits:
        user_limits[user_id] = 0

    # Проверка лимита
    if user_limits[user_id] >= FREE_LIMIT:
        await message.answer(
            "🚫 Лимит бесплатных запросов закончился.\n\n"
            "Чтобы продолжить — купи PRO ⭐"
        )
        return

    # Увеличиваем счётчик
    user_limits[user_id] += 1

    photos = [
        f"https://picsum.photos/500/500?random={i}"
        for i in range(PHOTOS_PER_REQUEST)
    ]

    media = [types.InputMediaPhoto(media=p) for p in photos]
    await message.answer_media_group(media)

    remaining = FREE_LIMIT - user_limits[user_id]
    await message.answer(
        f"Осталось бесплатных запросов: {remaining}"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
