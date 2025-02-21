from operator import index
import sqlite3
import telebot
from telebot import types
global list
global inp
inp = "0"
connection = sqlite3.connect('my_database.db', check_same_thread=False)
cursor = connection.cursor()
plan = []
token='7896437955:AAF6meLEqWoFPg6dLm2wKtpkidCcBXKSKas'
bot=telebot.TeleBot(token)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
username INTEGER PRIMARY KEY,
plan TEXT NOT NULL,
score INTEGER
)
''')
@bot.message_handler(commands=['start'])
def start_message(message):

    print(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("план")
    btn2 = types.KeyboardButton("счет")
    btn3 = types.KeyboardButton("ввод план")
    markup.add(btn1, btn2, btn3)
    cursor.execute('INSERT INTO Users (username, plan, score) VALUES (?, ?, ?)', (int(message.chat.id), " ", 0))
    connection.commit()
    bot.send_message(message.chat.id, "здесь будет инструкция ", reply_markup = markup)
#cursor.execute('INSERT INTO Users (username) VALUES (?)', (str(message.chat.id)))

@bot.message_handler(content_types=['text'])
def func(message):
    global inp
    if(message.text == "план"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("счет")
        btn3 = types.KeyboardButton("ввод план")
        back = types.KeyboardButton("Вернуться в главное меню")
        cursor.execute("SELECT  plan FROM users WHERE username = ?", (message.from_user.id,))
        plan = str(cursor.fetchall())
        plan = plan[3:-4]
        bot.send_message(message.chat.id, text="вот ваш план" + ": " + plan, reply_markup = markup)
        for i in plan.split(";"):
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(i[2:], callback_data=i)
            markup.add(button1)
            bot.send_message(message.chat.id, i.format(message.from_user), reply_markup=markup)
        markup.add(btn1, btn3, back)
        inp = "0"
    elif(message.text == "счет"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("план")
        btn3 = types.KeyboardButton("ввод план")
        back = types.KeyboardButton("Вернуться в главное меню")
        cursor.execute("SELECT  score FROM users WHERE username = ?", (message.from_user.id,))
        score = str(cursor.fetchall())
        print(score)
        bot.send_message(message.chat.id, text="вот ваш счет" + ": " + score[2:-3], reply_markup = markup)
        markup.add(btn1, btn3, back)
        inp = "0"
    elif (message.text == "ввод план"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("план")
        btn2 = types.KeyboardButton("счет")
        btn3 = types.KeyboardButton("ввод план")
        markup.add(btn1, btn2, btn3)
        inp = message.from_user.id
        bot.send_message(message.chat.id, text="жду", reply_markup = markup)
    elif inp == message.from_user.id:
        planin = str(message.text)
        print(planin)
        cursor.execute('UPDATE Users SET plan = ? WHERE username = ?', (planin, message.from_user.id))
        connection.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("план")
        btn2 = types.KeyboardButton("счет")
        btn3 = types.KeyboardButton("ввод план")
        inp = "0"
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="план введен!", reply_markup=markup)




@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    cursor.execute("SELECT  plan FROM users WHERE username = ?", (call.from_user.id, ))
    plan = str(cursor.fetchall())
    print(plan)
    plan = plan[2:-3]
    print(call.data)
    print(plan)

    index = plan.find(str(call.data))
    if index != -1:
        bot.answer_callback_query(call.id, call.data )
        string_list = list(plan)
        string_list[index] = "✅"
        plan = "".join(string_list)
        print (plan)
        cursor.execute('UPDATE Users SET plan = ? WHERE username = ?', (plan, call.from_user.id))
        connection.commit()
    else:
        bot.answer_callback_query(call.id, "ds" )

        
      
bot.polling(none_stop=True)

connection.close()
