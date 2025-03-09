import logging
from openai import OpenAI  # Импортируем новый клиент OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваш API ключ от DeepSeek
DEEPSEEK_API_KEY = "sk-6e9d97038c104c549e5df40bce59cc9d"  # Замените на ваш ключ DeepSeek
DEEPSEEK_API_URL = "https://api.deepseek.com"  # Базовый URL DeepSeek API

# Инициализация клиента OpenAI с указанием базового URL DeepSeek API
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_API_URL
)

# Функция для взаимодействия с DeepSeek API
def call_deepseek_api(text: str) -> str:
    try:
        # Используем модель DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",  # Укажите модель DeepSeek
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text}
            ],
            stream=False
        )
        # Возвращаем ответ от модели
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Ошибка при запросе к DeepSeek API: {e}")
        return f"Ошибка при запросе к DeepSeek API: {e}"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот, который использует DeepSeek API. Отправь мне текст для анализа.')

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    response = call_deepseek_api(user_text)  # Синхронный вызов
    await update.message.reply_text(response)

# Обработка ошибок
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

def main() -> None:
    # Вставьте сюда ваш токен от Telegram бота
    application = Application.builder().token("7093297396:AAEKVFllfoh7fGwUp1n3FEOQOiIQmZY6HQc").build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))

    # Регистрация обработчика текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Регистрация обработчика ошибок
    application.add_error_handler(error)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()