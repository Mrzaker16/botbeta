
import telebot

from random import randint

from telebot import types
TOKEN = "1879808009:AAGJ05wcsZ0Vt5tSFs-lbp1BpmGiSp_XVXU"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😊 Как дела?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalal(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(randint(0,100)))
        elif message.text == '😊 Как дела?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Хорошо 😊', callback_data='good')
            item2 = types.InlineKeyboardButton('Плохо 😢', callback_data='bad')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично как сам?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Незнаю что ответить 😢')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Очень хорошо 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Грустно 😢')
            bot.edit_message_text(chat_id=call.message.chat.id, text='😊 Как дела?', reply_markup=None)

            bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
