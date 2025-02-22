import sqlite3
import telebot
from telebot import types
global inp#variable for input
connection = sqlite3.connect('my_database.db', check_same_thread=False)#connect
cursor = connection.cursor()
token='7896437955:AAF6meLEqWoFPg6dLm2wKtpkidCcBXKSKas'#token tg
bot=telebot.TeleBot(token)#for telebot
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
username INTEGER PRIMARY KEY,
plan TEXT NOT NULL,
score INTEGER
)
''')#make db
@bot.message_handler(commands=['start'])#faund start massage
def start_message(message):
    print(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)#for button
    btn1 = types.KeyboardButton("план")# button plan
    btn2 = types.KeyboardButton("счет")# button score
    btn3 = types.KeyboardButton("ввод план")# input plan
    markup.add(btn1, btn2, btn3)#show plan
    cursor.execute('INSERT INTO Users (username, plan, score) VALUES (?, ?, ?)', (int(message.chat.id), " ", 0))# start in db
    connection.commit()#save db
    bot.send_message(message.chat.id, "здесь будет инструкция ", reply_markup = markup)#start message

@bot.message_handler(content_types=['text'])
def func(message):
    global inp#variable for input
    if message.text == "план":#plan
        cursor.execute("SELECT  plan FROM users WHERE username = ?", (message.from_user.id,))#take plan in db
        plan = str(cursor.fetchall())[3:-4]#take plan in db and delete extra
        bot.send_message(message.chat.id, text="вот ваш план" + ": " + plan)#output plan
        for i in plan.split(";"):#cycle for do inline but
            markup = types.InlineKeyboardMarkup()#for inline
            button1 = types.InlineKeyboardButton(i, callback_data=i)#output inline
            markup.add(button1)#show inline
            bot.send_message(message.chat.id, i.format(message.from_user), reply_markup = markup)#send text
        inp = "0"#variable for input
    elif message.text == "счет":#score
        cursor.execute("SELECT  plan FROM users WHERE username = ?", (message.from_user.id,))#take score in db

        score = str(cursor.fetchall()).count("✅")
        print(score)
        bot.send_message(message.chat.id, text="вот ваш счет" + ": " + str(score))#output score
        inp = "0"#variable for input
    elif message.text == "ввод план":# input start plan
        inp = message.from_user.id#variable for input
        bot.send_message(message.chat.id, text="жду")#output info
    elif inp == message.from_user.id: # input plan
        planin = str(message.text)# message in "str"
        print(planin+"52")
        cursor.execute('UPDATE Users SET plan = ? WHERE username = ?', (planin, message.from_user.id))#save in db
        connection.commit()# save change
        inp = "0"#variable for input
        bot.send_message(message.chat.id, text="план введен!")#output info




@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    cursor.execute("SELECT  plan FROM users WHERE username = ?", (call.from_user.id, ))
    plan = str(cursor.fetchall())
    plan = plan[3:-4]
    print(call.data+"66")
    print(plan+"67")
    index = plan.find(str(call.data))
    print(plan[index]+"69")
    if index != -1 and plan[index] != "✅" :
        bot.answer_callback_query(call.id, call.data )
        string_list = plan
        string_list = string_list[:index] +"✅"+ string_list[index:]
        plan = "".join(string_list)
        print (plan)
        cursor.execute('UPDATE Users SET plan = ? WHERE username = ?', (plan, call.from_user.id))
        connection.commit()
    else:
        bot.answer_callback_query(call.id, "задача выполнена" )

        
      
bot.polling(none_stop=True)

connection.close()
"""
tz: Task completion series
    count plan
    # = series +(n+1)
    * = presentation +5
    - = plan +0.5

"""
#kostik<33