import telebot

token = "7368988067:AAFXAjfn1Fr3WypgYEdXIunvzg6E8crUZzY"
bot = telebot.TeleBot(token, parse_mode='MarkdownV2')
admin_id = "7768655853"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width = 2)
    A = telebot.types.InlineKeyboardButton('Обращение', callback_data='Ra')
    B = telebot.types.InlineKeyboardButton('Сайт', url='https://t.me/m/lkYTC_YMZDFi')
    C = telebot.types.InlineKeyboardButton('Канал', url='https://t.me/nupizdetshe')
    markup.add(A, C, B)
    bot.send_message(message.chat.id, "Выберите дальнейшее действие", reply_markup=markup)


@bot.message_handler(commands=['cancel'])
def cancel_handler(message):
    bot.send_message(message.chat.id, 'Отмена')
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'Ra')
def ask_for_review_name(call):
    bot.send_message(call.message.chat.id, 'Имя ввел\\(а\\)')
    bot.register_next_step_handler(call.message, ask_for_review)
    bot.answer_callback_query(call.id)

def ask_for_review(message):
    if message.text.lower() == '/cancel':
        cancel_handler(message)
        return
    name = message.text
    bot.send_message(message.chat.id, 'Обращение оставил\\(а\\)')
    bot.register_next_step_handler(message, save_review, name)
    return

def save_review(message, name):
    if message.text.lower() == '/cancel':
        cancel_handler(message)
        return
    review = message.text
    user_id = message.from_user.id
    username = message.from_user.username

    # Ensure proper encoding when writing to file
    with open('reviews.txt', 'a', encoding='utf-8') as file:
        file.write(f"Имя: {name}\nВысказывания: {review}\n\nID: {user_id}\nUsername: @{username}\n\n")

    bot.send_message(message.chat.id, 'Спасибо, счастливо\\!')
    bot.send_message(admin_id, f"Высказывания.\nИмя: {name}\nВысказывания: {review}\nID: {user_id}\nUsername: @{username}", parse_mode='HTML')

bot.polling(none_stop=True)