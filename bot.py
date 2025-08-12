# 1. Импорт библиотек
import logging
from logging.handlers import RotatingFileHandler
import os
import re

from dotenv import find_dotenv, load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message  # ловим все обновления этого типа
from aiogram.filters.command import Command  # обработка команд /start, /help и др.

# 2.Инициализация объектов
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен бота не найден!")

bot = Bot(token=TOKEN)
print("Бот инициализирован (токен не выводится)")

dp = Dispatcher()

# Настройки логгера
def setup_logging():
    LOG_DIR = os.path.join(os.getcwd(), "logs")
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Фильтр для скрытия токенов
    class SecretsFilter(logging.Filter):
        def filter(self, record):
            if hasattr(record, 'msg'):
                # Скрываем токены (пример: 123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11)
                record.msg = re.sub(r'\d{9,10}:[A-Za-z0-9_-]{35}', '***BOT_TOKEN***', str(record.msg))
            return True

    # Форматтер с временем и информацией о месте вызова
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

    # Базовые настройки
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            # Вращающийся файловый обработчик (5 МБ, 3 файла)
            RotatingFileHandler(
                filename=os.path.join(LOG_DIR, 'bot.log'),
                maxBytes=5*1024*1024,
                backupCount=3,
                encoding='utf-8'
            ),
            # Вывод в консоль
            logging.StreamHandler()
        ],
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Применяем фильтр ко всем обработчикам
    for handler in logging.root.handlers:
        handler.addFilter(SecretsFilter())

# Инициализация логгера
setup_logging()
logger = logging.getLogger(__name__)

# 3. Обработка команды start
@dp.message(Command(commands=["start"]))
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text1 = f"Приветствую, {user_name}!"
    text2 = "Введите ФИО для транслитерации."
    logging.info(f"{user_name} {user_id} запустил бота")
    await bot.send_message(chat_id=user_id, text=text1)
    await bot.send_message(chat_id=user_id, text=text2)


# 4. Обработка всех сообщений
@dp.message()
async def transliterate_it(message: Message):
    dict_letters = {
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "G",
        "Д": "D",
        "Е": "E",
        "Ё": "E",
        "Ж": "ZH",
        "З": "Z",
        "И": "I",
        "Й": "I",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "KH",
        "Ц": "TS",
        "Ч": "CH",
        "Ш": "SH",
        "Щ": "SHCH",
        "Ы": "Y",
        "Ъ": "IE",
        "Ь": "",
        "Э": "E",
        "Ю": "IU",
        "Я": "IA",
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ы": "y",
        "ъ": "ie",
        "ь": "",
        "э": "e",
        "ю": "iu",
        "я": "ia",
    }
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text
    new_text = ""
    check = True
    for ch in text:
        if ch.isalpha():
            if ch in dict_letters.keys():
                new_text += dict_letters[ch]
            else:
                check = False
        else:
            new_text += ch
    logging.info(f"{user_name} {user_id}: {text} - {new_text}")
    if check:
        await message.answer(f"Результат транслитерации: \n{new_text}")
    else:
        await message.answer(
            "ФИО содержит буквы не из русского алфавита.\nПроверьте исходные данные."
        )


# 5. Запуск процесса пуллинга
if __name__ == "__main__":
    dp.run_polling(bot)
