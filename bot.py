import logging
from dotenv import load_dotenv
import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters
)
from functools import wraps

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота из переменных окружения
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Декоратор для обработки ошибок
def error_handler(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            return await func(update, context)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            if update and update.effective_message:
                try:
                    await update.effective_message.reply_text(
                        "⚠️ Произошла ошибка. Пожалуйста, попробуйте позже.",
                        disable_web_page_preview=True
                    )
                except Exception as send_error:
                    logger.error(f"Failed to send error message: {send_error}")

    return wrapper


# Команда /start
@error_handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")

    keyboard = [
        ["📱 О eSIM", "🌍 Страны"],
        ["💳 Тарифы", "🛒 Купить"],
        ["❓ Помощь", "📞 Контакты"],
        ["⚙️ Инструкция"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_html(
        f"Привет, {user.mention_html()}!\n\n"
        "Я бот-помощник по eSIM — современной цифровой сим-карте.\n\n"
        "Данная сим-карта устанавливается один раз и может использоваться в разных поездках по всему миру!!!\n\n"
        "Выберите раздел в меню ниже:",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


# Раздел "О eSIM"
@error_handler
async def about_esim(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.id} requested about esim")
    text = """
📱 <b>Что такое eSIM?</b>

eSIM — это встроенная сим-карта, которая:
• Не требует физической карты
• Активируется через QR-код
• Сохраняет Ваш основной номер
• Экономит место в устройстве
• Идеальна для путешественников
• Использование eSIM от TravelConnect <b>Выгоднее до 10 раз</b> по сравнению с местными операторами  

Поддержка eSIM есть в:
• iPhone X и новее
• Google Pixel 3 и новее
• Samsung Galaxy А56 и новее
• И других современных устройствах
    """
    await update.message.reply_html(text, disable_web_page_preview=True)


# Раздел "Покрытие"
@error_handler
async def coverage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.id} requested coverage")
    text = """
🌍 <b>Глобальное покрытие</b>

Наша eSIM работает в 200+ странах мира!
Ниже перечислены цены на основные направления:

• Турция — от 145₽ за 1 ГБ
• Египет — от 347₽ за 1 ГБ
• Таиланд — от 120₽ за 1 ГБ
• ОАЭ — от 285₽ за 1 ГБ
• Китай — от 120₽ за 1 ГБ
• Вьетнам — от 158₽ за 1 ГБ
• Мальдивы — от 440₽ за 1 ГБ
• Индия — от 453₽ за 1 ГБ
• Шри-Ланка — от 240₽ за 1 ГБ
• Грузия — от 249₽ за 1 ГБ
• Армения — от 184₽ за 1 ГБ
    """
    await update.message.reply_text(
        text=text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🌐 Все страны и тарифы ЗДЕСЬ!!!", url="https://travelconnect.online/?p=312")
        ]]),
        disable_web_page_preview=True
    )


# Раздел "Тарифы"
@error_handler
async def tariffs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.id} requested tariffs")
    keyboard = [
        [
            InlineKeyboardButton("🇪🇺 Европа", callback_data="eu_tariff"),
            InlineKeyboardButton("🌍 Африка", callback_data="africa_tariff"),
        ],
        [
            InlineKeyboardButton("🌏 Азия", callback_data="asia_tariff"),
            InlineKeyboardButton("🌎 Америка", callback_data="us_tariff"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "💳 <b>Выберите регион для просмотра тарифов:</b>",
        parse_mode="HTML",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


# Обработчик инлайн-кнопок тарифов И других callback
@error_handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Если это тарифы
    if query.data in ["eu_tariff", "africa_tariff", "asia_tariff", "us_tariff"]:
        logger.info(f"User {query.from_user.id} selected tariff: {query.data}")

        tariffs_data = {
            "eu_tariff": {
                "name": "Европа",
                "prices": "• 1 ГБ — от 356₽\n• 3 ГБ — от 807₽\n• 10 ГБ — от 1180₽\nи другие"
            },
            "africa_tariff": {
                "name": "Африка",
                "prices": "• 1 ГБ — от 661₽\n• 3 ГБ — от 1881₽\n• 10 ГБ — от 6153₽\nи другие"
            },
            "asia_tariff": {
                "name": "Азия",
                "prices": "• 1 ГБ — от 120₽\n• 3 ГБ — от 292₽\n• 10 ГБ — от 808₽\nи другие"
            },
            "us_tariff": {
                "name": "Америка",
                "prices": "• 1 ГБ — от 148₽\n• 3 ГБ — от 341₽\n• 10 ГБ — от 1016₽\nи другие"
            }
        }

        selected = tariffs_data.get(query.data)
        if not selected:
            await query.edit_message_text(
                "Тариф не найден. Пожалуйста, выберите снова.",
                disable_web_page_preview=True
            )
            return

        text = f"🌍 <b>Тарифы для {selected['name']}:</b>\n\n{selected['prices']}"

        await query.edit_message_text(
            text=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🛒 Купить", url="https://travelconnect.online/?p=312")
            ]]),
            disable_web_page_preview=True
        )

    # Если callback_data = "help" - обрабатываем помощь
    elif query.data == "help":
        # Отправляем новое сообщение с помощью
        await send_help_message(query.message)

    # Если неизвестный callback
    else:
        await query.edit_message_text(
            "Команда не распознана. Пожалуйста, выберите снова.",
            disable_web_page_preview=True
        )


# Раздел "Купить"
@error_handler
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.id} requested buy info")
    text = """
🛒 <b>Как приобрести eSIM:</b>

1. Выберите тариф на нашем сайте
2. Пройдите простую процедуру регистрации
3. Оплатите любым удобным для Вас способом
4. Получите QR-код
5. Отсканируйте QR-код или установите eSIM вручную по инструкции
6. По прибытии в выбранную страну eSIM активируется автоматически
7. Купили один раз!!!! Используете установленную eSIM просто меняя тариф

💡 <i>Активация занимает менее 5 минут</i>
    """

    # Создаем клавиатуру с несколькими кнопками
    keyboard = [
        [InlineKeyboardButton("🛒 Оформить заказ", url="https://travelconnect.online/?p=312")],
        [InlineKeyboardButton("🌍 Посмотреть тарифы", url="https://travelconnect.online/?p=312")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_html(
        text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


# Функция для отправки сообщения помощи
async def send_help_message(message):
    text = """
❓ <b>Частые вопросы:</b>

<b>Вопрос:</b> Как проверить поддержку eSIM?
<b>Ответ:</b> Проверьте настройки телефона: Настройки → Сотовая связь → Добавить тариф/добавить eSIM

<b>Вопрос:</b> Можно ли использовать два номера одновременно?
<b>Ответ:</b> Да, если устройство поддерживает Dual SIM с eSIM

<b>Вопрос:</b> Сколько времени занимает активация?
<b>Ответ:</b> Обычно менее 5 минут после сканирования QR-кода

<b>Вопрос:</b> Как установить eSIM?
<b>Ответ:</b> Используйте кнопку меню: ⚙️ Инструкция

<b>Вопрос:</b> Как пополнить eSIM?
<b>Ответ:</b> Зайти на сайт под своей учетной записью, выбрать страну и интересующий пакет интернета, произвести оплату

• 📱 О eSIM - узнайте о технологии
• 🌍 Покрытие - страны и цены
• 💳 Тарифы - подробные тарифы по регионам
• 🛒 Купить - инструкция по покупке
• 📞 Контакты - свяжитесь с нами
• ⚙️ Инструкция - как использовать eSIM
    """
    await message.reply_html(text, disable_web_page_preview=True)


# Раздел "Помощь" - обработчик для команды /help
@error_handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.id} requested help")
    await send_help_message(update.message)


# Раздел "Контакты"
@error_handler
async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.id} requested contacts")
    text = """
📞 <b>Контакты</b>

• Сайт: http:&#8203;//travelconnect&#8203;.online

• Станьте клиентом после быстрой регистрации — и получите 
<b>персональную поддержку 24/7.</b>

⏰ <i><b>Забота о вас — наш приоритет</b></i>
    """

    keyboard = [
        [InlineKeyboardButton("🌐 Перейти на сайт: travelconnect.online", url="https://travelconnect.online/?p=312")]
    ]

    await update.message.reply_text(
        text=text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )


# Раздел "Инструкция"
@error_handler
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.id} requested instructions")
    text = """
⚙️ <b>Инструкция</b>

• <b>Удостоверьтись, что Ваше устройство поддерживает eSIM:</b>

•Наберите на своем телефоне (в режиме набора номера) команду: <b>*#06#</b>

•Устройство поддерживает eSIM если появиться номер <b>EID</b>

• Какие 2 простых действия необходимо сделать, чтобы сим карта предоставила доступ к интернету в роуминге:

• <b>iPhone (Apple)</b>

1. Включите роуминг на добавленной eSIM:
    Откройте меню Настройки: → Сотовая связь → нажмите на добавленную eSIM → Роуминг данных и включите его 

2. Установите данную eSIM в качестве используемой для сотовых данных:
    Откройте меню Настройки: → Сотовая связь → Сотовые данные и поставьте отметку напротив установленной eSIM

• <b>Android/Samsung</b>

1. Включите роуминг на добавленной eSIM:
    Откройте меню Настройки: →Подключения →Мобильные сети → Роуминг данных и включите его на нашей eSIM 

2. Установите данную eSIM в качестве используемой для сотовых данных:
    Откройте меню Настройки: →Подключения →Диспетчер SIM карт →Мобильные данные и выберите добавленную eSIM в качестве используемой для мобильных данных

    """
    await update.message.reply_html(text, disable_web_page_preview=True)


# Команда /status для проверки работы бота
@error_handler
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.id} checked status")
    await update.message.reply_text(
        "✅ Бот работает нормально",
        disable_web_page_preview=True
    )


# Улучшенный обработчик текстовых сообщений
@error_handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower().strip()
    logger.info(f"User {update.effective_user.id} sent message: '{text}'")

    # Сопоставление текста с обработчиками
    handler_mapping = {
        "📱 о esim": about_esim,
        "🌍 страны": coverage,
        "💳 тарифы": tariffs,
        "🛒 купить": buy,
        "❓ помощь": help_command,
        "📞 контакты": contacts,
        "⚙️ инструкция": settings
    }

    # Удаляем эмодзи для более надежного сопоставления
    clean_text = text.replace("📱", "").replace("🌍", "").replace("💳", "").replace("🛒", "").replace("❓", "").replace("📞",
                                                                                                                   "").replace(
        "⚙️", "").strip()

    # Создаем словарь для сопоставления без эмодзи
    clean_mapping = {
        "о esim": about_esim,
        "страны": coverage,
        "тарифы": tariffs,
        "купить": buy,
        "помощь": help_command,
        "контакты": contacts,
        "инструкция": settings
    }

    # Сначала проверяем точное совпадение с оригинальным текстом
    if text in handler_mapping:
        await handler_mapping[text](update, context)
        return

    # Затем проверяем совпадение без эмодзи
    if clean_text in clean_mapping:
        await clean_mapping[clean_text](update, context)
        return

    # Если не нашли точного совпадения, ищем частичное
    handler_found = False
    for clean_key, handler in clean_mapping.items():
        if clean_key in clean_text:
            await handler(update, context)
            handler_found = True
            break

    if not handler_found:
        await update.message.reply_text(
            "Пожалуйста, используйте меню для навигации. "
            "Если у вас есть вопросы, нажмите '❓ Помощь'",
            disable_web_page_preview=True
        )


# Обработчик неизвестных команд
@error_handler
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.id} sent unknown command: {update.message.text}")
    await update.message.reply_text(
        "Неизвестная команда. Используйте /start для отображения меню "
        "или /help для получения справки.",
        disable_web_page_preview=True
    )


# Глобальный обработчик ошибок
async def error_handler_global(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f'Update "{update}" caused error "{context.error}"')

    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "Произошла непредвиденная ошибка. Пожалуйста, попробуйте еще раз.",
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")


def main() -> None:
    # Проверка наличия токена
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set!")
        print("Ошибка: Переменная окружения TELEGRAM_BOT_TOKEN не установлена!")
        print("Пожалуйста, установите токен:")
        print("export TELEGRAM_BOT_TOKEN='ваш_токен'")
        return

    # Создаем Application
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд в порядке приоритета
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Обработчик ошибок
    application.add_error_handler(error_handler_global)

    # Запуск бота
    logger.info("Bot is starting...")
    print("Бот запускается...")

    try:
        application.run_polling(
            poll_interval=1.0,
            timeout=20,
            drop_pending_updates=True
        )
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"Ошибка запуска бота: {e}")
    finally:
        logger.info("Bot has stopped.")
        print("Бот остановлен.")


if __name__ == "__main__":
    main()