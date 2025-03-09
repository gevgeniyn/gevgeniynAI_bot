from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    # Получаем имя пользователя
    user = update.message.from_user
    first_name = user.first_name  # Имя пользователя

    # Создаем клавиатуру с кнопками
    keyboard = [
        ['Написать рецензию', 'Написать отзыв'],
        
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Адресное приветствие
    greeting = f"Здравствуйте, {first_name}! Я электронный помощник ОСПО (отдела сопровождения платного обучения) УУНиТ (Уфимского университета науки и технологий). Буду рад оказать помощь в отношении платного обучения, предоставляю Вам основную информацию. Выберите интерсующий Вас вопрос и нажмите на соответствующую кнопку"
    
    # Отправляем сообщение с клавиатурой
    await update.message.reply_text(greeting, reply_markup=reply_markup)

async def handle_message(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    first_name = user.first_name  # Имя пользователя
    user_message = update.message.text
    
    # Обрабатываем нажатие кнопки и формируем адресный ответ
    if user_message == 'Написать рецензию':
        response = f"{first_name},чтобы мне написать рецензию попрошу вас ответить на несколько вопросов"
    elif user_message == 'Написать отзыв':
        response = f"{first_name}, чтобы мне написать отзыв попрошу вас ответить на несколько вопросов"
    else:
        response = f"{first_name}, пока не могу ответить на это сообщение, извините"

    # Создаем новую клавиатуру
    keyboard = [
        ['Написать рецензию', 'Написать отзыв'],
        
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Отправляем ответ с клавиатурой
    await update.message.reply_text(response, reply_markup=reply_markup)

def main() -> None:
    # Укажите ваш токен
    application = Application.builder().token("7093297396:AAEKVFllfoh7fGwUp1n3FEOQOiIQmZY6HQc").build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()