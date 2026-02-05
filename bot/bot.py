from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Импорт конфигурации
from config.config import bot_config, backend_config, webapp_config

# Инициализация бота
BOT_TOKEN = bot_config.token
if not BOT_TOKEN:
    raise ValueError("Необходимо указать TELEGRAM_BOT_TOKEN в файле .env")

# URL бэкенд-сервера
BACKEND_URL = backend_config.url

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Классы для FSM (Finite State Machine)
class VPNStates(StatesGroup):
    choosing_server = State()

# Функция для получения статуса пользователя с бэкенда
async def get_user_status(user_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BACKEND_URL}/api/users/{user_id}/status") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except Exception as e:
        print(f"Ошибка при получении статуса пользователя: {e}")
        return None

# Функция для подключения пользователя к VPN
async def connect_user(user_id: int, server: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BACKEND_URL}/api/users/{user_id}/connect",
                                   json={'server': server}) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except Exception as e:
        print(f"Ошибка при подключении пользователя: {e}")
        return None

# Функция для отключения пользователя от VPN
async def disconnect_user(user_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BACKEND_URL}/api/users/{user_id}/disconnect") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except Exception as e:
        print(f"Ошибка при отключении пользователя: {e}")
        return None

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    # Создание фирменного баннера
    welcome_banner = """🚀 Добро пожаловать в VPN-сервис!

🔒 Защитите свою конфиденциальность в интернете
⚡ Ускорьте соединение
🌍 Получите доступ к заблокированному контенту"""

    # Создание клавиатуры с кнопкой открытия Mini App
    keyboard = InlineKeyboardBuilder()

    # URL для открытия Mini App (должен быть HTTPS!)
    # Для локальной разработки используйте localtunnel: lt --port 5000
    # URL берется из конфигурации
    mini_app_url = webapp_config.url

    keyboard.row(InlineKeyboardButton(text="📱 Открыть приложение", web_app=types.WebAppInfo(url=mini_app_url)))
    keyboard.row(InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help"))
    keyboard.row(InlineKeyboardButton(text="📊 Статус", callback_data="status"))

    # Отправка сообщения с баннером и кнопками
    await message.answer(welcome_banner + "\n\nДля управления VPN используйте команды:\n/connect - Подключиться к VPN\n/disconnect - Отключиться от VPN\n/status - Проверить статус подключения", reply_markup=keyboard.as_markup())

# Обработчик команды /help
@dp.message(Command("help"))
async def send_help(message: types.Message):
    help_text = """📖 <b>Справка по командам:</b>

/start - Главное меню
/help - Показать это сообщение
/status - Проверить статус VPN-подключения
/connect - Подключиться к VPN
/disconnect - Отключиться от VPN

<i>Для полного функционала используйте наше приложение!</i>"""
    await message.answer(help_text, parse_mode='HTML')

# Обработчик команды /status
@dp.message(Command("status"))
async def check_status(message: types.Message):
    user_id = message.from_user.id
    status_data = await get_user_status(user_id)

    if status_data:
        if status_data.get('connected', False):
            status_msg = f"""📊 <b>Статус VPN-подключения:</b>

Подключен: ✅ Да
Сервер: {status_data.get('server', 'N/A')}
Время подключения: {status_data.get('connection_time', 'N/A')}
IP-адрес: {status_data.get('ip_address', 'N/A')}"""
        else:
            status_msg = "📊 <b>Статус VPN-подключения:</b>\n\nПодключен: ❌ Нет"
    else:
        status_msg = "⚠️ Не удалось получить статус подключения"

    await message.answer(status_msg, parse_mode='HTML')

# Обработчик команды /connect
@dp.message(Command("connect"))
async def connect_vpn(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Получаем статус пользователя
    status_data = await get_user_status(user_id)

    if status_data and status_data.get('connected', False):
        await message.answer("⚠️ Вы уже подключены к VPN!")
        return

    # Отправляем сообщение о выборе сервера
    await message.answer("🌐 Выберите сервер для подключения:",
                         reply_markup=get_server_keyboard())

    # Устанавливаем состояние
    await state.set_state(VPNStates.choosing_server)

# Обработчик команды /disconnect
@dp.message(Command("disconnect"))
async def disconnect_vpn(message: types.Message):
    user_id = message.from_user.id

    # Получаем статус пользователя
    status_data = await get_user_status(user_id)

    if not status_data or not status_data.get('connected', False):
        await message.answer("⚠️ Вы не подключены к VPN!")
        return

    # Отключаем пользователя
    result = await disconnect_user(user_id)

    if result and result.get('success'):
        await message.answer("✅ Успешно отключено от VPN!")
    else:
        await message.answer("❌ Не удалось отключиться от VPN")

# Функция для получения клавиатуры с серверами
def get_server_keyboard():
    keyboard = InlineKeyboardBuilder()

    # В реальном приложении получаем список серверов с бэкенда
    servers = [
        {"id": "US-East", "name": "US-East (Нью-Йорк)"},
        {"id": "US-West", "name": "US-West (Лос-Анджелес)"},
        {"id": "Europe", "name": "Europe (Франкфурт)"},
        {"id": "Asia", "name": "Asia (Токио)"},
        {"id": "Australia", "name": "Australia (Сидней)"}
    ]

    for server in servers:
        keyboard.row(InlineKeyboardButton(text=server["name"],
                                         callback_data=f"server_{server['id']}"))

    return keyboard.as_markup()

# Обработчик нажатий на кнопки с серверами
@dp.callback_query(lambda c: c.data.startswith('server_'))
async def process_server_selection(callback_query: types.CallbackQuery, state: FSMContext):
    if await state.get_state() != VPNStates.choosing_server.state:
        return

    server_id = callback_query.data.split('_')[1]
    user_id = callback_query.from_user.id

    # Подключаем пользователя к выбранному серверу
    result = await connect_user(user_id, server_id)

    if result and result.get('success'):
        await callback_query.message.edit_text(
            f"""✅ <b>Успешно подключено к VPN!</b>

Сервер: {result.get('server', 'N/A')}
IP-адрес: {result.get('ip_address', 'N/A')}
Время подключения: {result.get('connection_time', 'N/A')}""",
            parse_mode='HTML'
        )
    else:
        await callback_query.message.edit_text("❌ Не удалось подключиться к VPN")

    # Сбрасываем состояние
    await state.clear()

# Обработчик inline-кнопок
@dp.callback_query(lambda c: c.data in ['help', 'status'])
async def handle_inline_buttons(callback_query: types.CallbackQuery):
    if callback_query.data == 'help':
        await send_help(callback_query.message)
    elif callback_query.data == 'status':
        await check_status(callback_query.message)

    # Ответ на callback
    await callback_query.answer()

# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: types.Message):
    response = """🤖 <b>VPN-бот</b>

Доступные команды:
• /start - Главное меню
• /help - Справка
• /status - Статус подключения
• /connect - Подключиться к VPN
• /disconnect - Отключиться от VPN

Для полного функционала откройте приложение!
"""
    await message.answer(response, parse_mode='HTML')

# Запуск бота
async def main():
    print("Запуск Telegram-бота...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())