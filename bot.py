import telebot
from telebot import types
from pymongo import MongoClient

# Ваш токен бота
API_TOKEN = '7109456325:AAEWS4JQ4pzthRQN7cj7nE29Wxedv_7c8PE'
MONGO_URI = 'mongodb+srv://romarioodeveloper:c3pn17H3nQYNvD3f@cluster0.a64gqsf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

bot = telebot.TeleBot(API_TOKEN)

# Подключение к MongoDB
client = MongoClient(MONGO_URI)
db = client.coffee_shop
users_collection = db.users
referrals_collection = db.referrals


# Главная функция для старта
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветственное сообщение
    welcome_text = f"Привет, {message.from_user.first_name}! 👋\nДобро пожаловать в нашу кофейню ☕️!\nВыберите опцию ниже, чтобы начать:"

    # Кнопки меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Получить скидку 🎁")
    btn2 = types.KeyboardButton("Реферальная программа 👫")
    btn3 = types.KeyboardButton("Бонусы 🎉")
    btn4 = types.KeyboardButton("Открыть WebApp 🌐")
    markup.add(btn1, btn2, btn3, btn4)

    # Проверка и добавление пользователя в базу данных
    user = users_collection.find_one({"user_id": message.from_user.id})
    if not user:
        users_collection.insert_one(
            {"user_id": message.from_user.id, "username": message.from_user.username, "bonuses": 0})

    # Отправка сообщения с кнопками
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


# Обработка кнопок
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Получить скидку 🎁":
        bot.send_message(message.chat.id, "Ваша скидка: 10% на следующий кофе! ☕️")
    elif message.text == "Реферальная программа 👫":
        bot.send_message(message.chat.id, "Пригласите друга и получите 20% скидки! 🎁")
    elif message.text == "Бонусы 🎉":
        user = users_collection.find_one({"user_id": message.from_user.id})
        bot.send_message(message.chat.id, f"Ваши бонусы: {user['bonuses']} бонусов на счету! 🎉")
    elif message.text == "Открыть WebApp 🌐":
        webapp_button = types.InlineKeyboardMarkup()
        webapp_button.add(
            types.InlineKeyboardButton("Перейти в WebApp", web_app=types.WebAppInfo(url="https://your-webapp-url.com")))
        bot.send_message(message.chat.id, "Нажмите кнопку ниже для перехода в WebApp:", reply_markup=webapp_button)


# Запуск бота
bot.polling(none_stop=True)
