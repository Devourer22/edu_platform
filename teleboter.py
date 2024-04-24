import telebot
from telebot import types
import parser_asu

# Указываем токен вашего бота
TOKEN = '6459628894:AAGB1JqgJRFWbwFY_cyEPM7UXRNTFcUnydQ'

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Ссылки на расписание для каждой группы
GROUP_URLS = {
    "Группа 505": "https://www.asu.ru/timetable/students/16/2129437402/",
    "Группа 506": "https://www.asu.ru/timetable/students/16/2129437403/"
}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Отправляем приветственное сообщение и кнопку
    bot.reply_to(message, "Привет! Нажми на кнопку для действия.", reply_markup=get_keyboard())


# Обработчик нажатий на кнопки для выбора группы
@bot.callback_query_handler(func=lambda call: call.data in GROUP_URLS.values())
def handle_group_choice(call):
    # Обрабатываем выбор группы
    url = call.data
    get_schedule_student(call.message, url)

# Обработчик нажатий на кнопки для выбора преподавателя
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # Получаем URL из колбэка
    url = call.data

    parsed_schedule = parser_asu.parsing(url)
    # Задаем желаемый день недели
    desired_day = 'все'

    # Выводим расписание
    new_schedule = parser_asu.search_schedule(parsed_schedule, desired_day)

    # Формируем текст для отправки
    response = ""
    for schedule_per_day in new_schedule:
        if len(schedule_per_day) != 3:
            response += schedule_per_day + "\n\n"  # Добавляем пустую строку между расписаниями разных дней

    # Отправляем расписание пользователю
    bot.reply_to(call.message, response)


# Обработчик нажатий на кнопку "Получить расписание"
@bot.message_handler(func=lambda message: message.text == 'Получить расписание')
def handle_get_schedule(message):
    bot.reply_to(message, "Выберите группу:", reply_markup=get_group_keyboard())


# Обработчик нажатий на кнопку "Получить расписание преподавателя"
@bot.message_handler(func=lambda message: message.text == 'Получить расписание преподавателя')
def handle_get_lecturer_schedule(message):
    bot.reply_to(message, "Вы выбрали получение расписания преподавателя.")
    handle_get_lect(message)


# Обработчик нажатий на кнопку "Получить оставшиеся занятия"
@bot.message_handler(func=lambda message: message.text == 'Получить оставшиеся занятия')
def handle_get_remaining_lessons(message):
    bot.reply_to(message, "Вы выбрали получение оставшихся занятий.")
    # Здесь нужно вызвать функцию или выполнить действие, связанное с получением оставшихся занятий


# Получение расписания студента
def get_schedule_student(message, url):
    parsed_schedule = parser_asu.parsing(url)

    # Задаем желаемый день недели
    desired_day = 'все'

    # Выводим расписание
    new_schedule = parser_asu.search_schedule(parsed_schedule, desired_day)

    # Формируем текст для отправки
    response = ""
    for schedule_per_day in new_schedule:
        if len(schedule_per_day) != 3:
            response += schedule_per_day + "\n\n"  # Добавляем пустую строку между расписаниями разных дней

    # Отправляем расписание пользователю
    bot.reply_to(message, response)


# Функция для создания клавиатуры с выбором группы
def get_group_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for group, url in GROUP_URLS.items():
        button = types.InlineKeyboardButton(text=group, callback_data=url)
        keyboard.add(button)
    return keyboard


# Функция для создания клавиатуры с основными действиями
def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_get_schedule_student = types.KeyboardButton(text='Получить расписание')
    button_get_schedule_lect = types.KeyboardButton(text="Получить расписание преподавателя")
    button_get_amount = types.KeyboardButton(text="Получить оставшиеся занятия")
    keyboard.add(button_get_schedule_student, button_get_schedule_lect, button_get_amount)
    return keyboard


def handle_get_lect(message):
    # Создаем объект клавиатуры
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    # Создаем кнопки с текстом и колбэком для каждого действия
    lecturers = {
        "Сеулеков А.В.": "https://www.asu.ru/timetable/lecturers/16/103/2122097082/",
        "Грязнов А.С.": "https://www.asu.ru/timetable/lecturers/16/103/2122097225/",
        "Белозерских В.В.": "https://www.asu.ru/timetable/lecturers/16/103/856/",
        "Матющенко Ю.Я.": "https://www.asu.ru/timetable/lecturers/16/103/850/",
        "Седалищев В.Н.": "https://www.asu.ru/timetable/lecturers/16/103/2122096013/",
        "Скурыдин Ю.Г.": "https://www.asu.ru/timetable/lecturers/16/103/2122095838/",
        "Калачев А.В.": "https://www.asu.ru/timetable/lecturers/16/103/1124351442/",
        "Шмаков И.А.": "https://www.asu.ru/timetable/lecturers/16/103/2122096175/",
        "Пашнев В.В.": "https://www.asu.ru/timetable/lecturers/16/103/843/"
    }

    for lecturer, url in lecturers.items():
        button = types.InlineKeyboardButton(text=lecturer, callback_data=url)
        keyboard.add(button)

    # Отправляем сообщение с клавиатурой
    bot.send_message(chat_id=message.chat.id, text="Выберите преподавателя:", reply_markup=keyboard)


# Запускаем бота
bot.polling()






