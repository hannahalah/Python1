import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('6722880952:AAF0cplnU1DiRnOVKYRk2Kr1uKXaQJrrchk')

upper = 0
lower = 0


@bot.message_handler(commands=['start'])
def start(message):
    sti = open('sti/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}\nЭтот бот '
                                      f'может помочь найти вам подарок на любой вкус и цвет!')


@bot.message_handler(commands=['end'])
def end(message):
    sti = open('sti/sticker3.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)


@bot.message_handler()
def info(message):
    global lower
    global upper
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == '/search':
        bot.send_message(message.chat.id, 'Введите нижний порог цены: ')
    elif message.text.isdigit() and lower == 0:
        lower = message.text.strip()
        bot.send_message(message.chat.id, 'Введите верхний порог цены: ')
    elif message.text.isdigit() and lower != 0 and upper == 0:
        upper = message.text.strip()
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Список подарков', callback_data='presents'))
        bot.send_message(message.chat.id, f'Вот что мы для вас нашли!{lower}, {upper}', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Я еще не знаю такой команды!{lower}, {upper}')


@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    global lower
    global upper
    conn = sqlite3.connect('identifier.sqlite')
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM gifts WHERE price_down > {lower} and price_up < {upper}')
    presents = cur.fetchall()

    info = ''
    for element in presents:
        info += f'Название: {element[1]}\n Цена: {element[2]} - {element[3]}$\n\n'
    cur.close()
    conn.close()

    if info != '':
        sti = open('sti/sticker1.webp', 'rb')
        bot.send_sticker(call.message.chat.id, sti)
        bot.send_message(call.message.chat.id, info)
        lower = 0
        upper = 0
    else:
        sti = open('sti/sticker2.webp', 'rb')
        bot.send_sticker(call.message.chat.id, sti)
        bot.send_message(call.message.chat.id, 'Пусто!')
        lower = 0
        upper = 0


bot.polling(none_stop=True)
