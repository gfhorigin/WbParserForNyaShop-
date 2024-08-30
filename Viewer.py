import telebot
from telebot import types
import json
import DBController as db
import Parser as p

boofer = {}

def ToInt(x):
    try:
        int(x)
        return True
    except:
        return False

bot = telebot.TeleBot('7121911975:AAF0zcjrXAnFvBmA3gSFkjOR2uhv3wMUh64')

@bot.message_handler(commands=["start"])
def start(message, res=False):

    telebot.types.ReplyKeyboardRemove()

    bot.send_message(message.chat.id, 'Здравствуйте - это бот парсер\n'
                                      'Скиньте сюда артикул с вб и заполните небольшую анкету, после чего товар автоматически появится на сайте NyaShop~')

    db.WBTable()

@bot.message_handler(content_types=["text"])
def handle_text(message,):
    with open('filters.json', 'r', encoding='utf-8') as f:  # открыли файл
        text = json.load(f)  # загнали все из файла в переменную

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if message.text in list(text.keys()):
        for i in list(text[message.text]) :
            item1 = types.KeyboardButton(i)
            markup.add(item1)
        bot.send_message(message.chat.id, 'Теперь выберите подкатегорию', reply_markup=markup)

        bot.register_next_step_handler(message, db.FillInfo, p.WbParser(boofer[message.chat.id]))
        print(boofer[message.chat.id])
        return

    if len(message.text) != 9 or not ToInt(message.text):
        bot.send_message(message.chat.id, 'это не артикул')
        return

    if not db.CheckingArticle(message.text) :
        bot.send_message(message.chat.id, 'этот артикул уже есть')
        return

    if not p.WbParser(message.text).TestArticle:
        bot.send_message(message.chat.id, 'этот артикул не существует')
        return

    db.NewArticle(message.text)
    boofer[message.chat.id] = message.text

    for i in list(text.keys()):
        item1 = types.KeyboardButton(i)
        markup.add(item1)

    bot.send_message(message.chat.id, 'Теперь выберите категорию', reply_markup=markup)

bot.polling(none_stop=True, interval=0, timeout=0)