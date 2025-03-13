import logging
import asyncio
from openai import OpenAI
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
OPENAI_API_KEY = "OpenAI key"  # Ключ OpenAI API
TELEGRAM_BOT_TOKEN = "Token Telegram bot"  # Токен Telegram бота

# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Функция для создания клавиатуры
def get_keyboard():
    keyboard = [
        ['Написать рецензию', 'Написать отзыв'],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Функция для разбиения текста на части
def split_text(text: str, max_length: int = 4096) -> list:
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

# Хранение истории диалогов
user_context = {}

# Асинхронная функция для взаимодействия с OpenAI API
async def call_openai_api(messages: list) -> str:
    try:
        # Используем модель GPT-3.5-turbo
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=False
            )
        )
        # Возвращаем ответ от модели
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI API: {e}")
        return "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже."

# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name

    # Инициализация контекста пользователя
    user_context[user_id] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    greeting = (
        f"Здравствуйте, {first_name}! Я электронный помощник ОСПО (отдела сопровождения платного обучения) "
        "УУНиТ (Уфимского университета науки и технологий). Буду рад оказать помощь в отношении платного обучения, "
        "предоставляю Вам основную информацию. Выберите интересующий Вас вопрос и нажмите на соответствующую кнопку."
    )
    await update.message.reply_text(greeting, reply_markup=get_keyboard())

# Обработка текстовых сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_id = user.id
    user_message = update.message.text

    # Добавляем сообщение пользователя в контекст
    if user_id not in user_context:
        user_context[user_id] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    user_context[user_id].append({"role": "user", "content": user_message})

    # Обработка нажатия кнопок
    if user_message == 'Написать рецензию':
        response = "Пожалуйста, опишите, о чем вы хотите написать рецензию."
    elif user_message == 'Написать отзыв':
        response = "Пожалуйста, опишите, о чем вы хотите написать отзыв."
    else:
        # Если текст не совпадает с кнопками, отправляем его в OpenAI API
        logger.info(f"Пользователь отправил сообщение: {user_message}")
        response = await call_openai_api(user_context[user_id])
        logger.info(f"Ответ от OpenAI: {response}")

        # Добавляем ответ бота в контекст
        user_context[user_id].append({"role": "assistant", "content": response})

    # Разбиваем ответ на части, если он слишком длинный
    response_parts = split_text(response)
    for part in response_parts:
        await update.message.reply_text(part, reply_markup=get_keyboard())

# Обработка ошибок
async def error(update: Update, context: CallbackContext) -> None:
    logger.error(f'Ошибка: {context.error}')
    await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")

def main() -> None:
    # Проверка наличия токенов
    if not OPENAI_API_KEY or not TELEGRAM_BOT_TOKEN:
        logger.error("Не указаны OPENAI_API_KEY или TELEGRAM_BOT_TOKEN.")
        return

    # Создание приложения Telegram бота
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))

    # Регистрация обработчика текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Регистрация обработчика ошибок
    application.add_error_handler(error)

    # Запуск бота
    logger.info("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()