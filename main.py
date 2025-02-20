from operator import index
import sqlite3
import telebot
from telebot import types
global list
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
    bot.send_message(message.chat.id,"Привет ✌️ ")
    print(message.chat.id)
    cursor.execute('INSERT INTO Users (username, plan, score) VALUES (?, ?, ?)', (int(message.chat.id), "q", 0))
    connection.commit()
#cursor.execute('INSERT INTO Users (username) VALUES (?)', (str(message.chat.id)))
@bot.message_handler(content_types='text')
def message_reply(Message):
    global plan
    plan = str(Message.text)
    cursor.execute('UPDATE Users SET plan = ? WHERE username = ?', (plan, Message.chat.id))
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    print (users)
    for i in plan.split("\n"):

        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(i, callback_data= i)
        markup.add(button1)
        bot.send_message(Message.chat.id, i .format(Message.from_user), reply_markup=markup)
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
    else:
        bot.answer_callback_query(call.id, "ds" )

        
      
bot.polling(none_stop=True)

connection.close()
