import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
import os

API_TOKEN = 'ТОКЕН'
PROMOCODE = "Ikona2t2"
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Память: кто ввёл промокод
authorized_users = set()

# Клавиатура
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text="Мануал №1")],
    [KeyboardButton(text="Поиск по номеру")],
    [KeyboardButton(text="Поиск по ФИО")],
    [KeyboardButton(text="Поиск баз данных")],
    [KeyboardButton(text="Мануал №5")],
    [KeyboardButton(text="Мануал №7")],
    [KeyboardButton(text="Как получить самый качественный мануал?")]
])

# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if message.from_user.id not in authorized_users:
        await message.answer("🔒 Введите промокод для доступа:")
    else:
        await message.answer("✅ Доступ разрешён. Выбери нужный мануал:", reply_markup=keyboard)

# Обработка всего остального
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if user_id not in authorized_users:
        if message.text.strip() == PROMOCODE:
            authorized_users.add(user_id)
            await message.answer("✅ Промокод принят. Доступ открыт!", reply_markup=keyboard)
        else:
            await message.answer("❌ Неверный промокод. Попробуйте снова.")
        return

    # Если уже авторизован — отправляем нужный мануал
    file_map = {
        "Мануал №1": "manual_1.txt",
        "Поиск по номеру": "search_number.txt",
        "Поиск по ФИО": "search_name.txt",
        "Поиск баз данных": "databases.txt",
        "Мануал №5": "manual_5.txt",
        "Мануал №7": "manual_7.txt",
        "Как получить самый качественный мануал?": "top_manual.txt"
    }

    file_name = file_map.get(message.text)
    if file_name:
        path = os.path.join("manuals", file_name)
        if os.path.exists(path):
            doc = FSInputFile(path)
            await message.answer_document(doc)
        else:
            await message.answer("Файл не найден. Убедись, что он есть в папке manuals.")
    else:
        await message.answer("Выбери опцию из меню.")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())