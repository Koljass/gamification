import sqlite3
import datetime
import telebot
from telebot import types
global inp#variable for input
connection = sqlite3.connect('my_database.db', check_same_thread=False)#connect
cursor = connection.cursor()
token=''#token tg
bot=telebot.TeleBot(token)#for telebot
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
username INTEGER PRIMARY KEY,
plan TEXT NOT NULL,
score INTEGER,
times INTEGER
)
''')#make db
@bot.message_handler(commands=['start'])#faund start massage
def start_message(message):
    global inp
    print(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)#for button
    btn1 = types.KeyboardButton("план")# button plan
    btn2 = types.KeyboardButton("счет")# button score
    btn3 = types.KeyboardButton("ввод план")# input plan
    markup.add(btn1, btn2, btn3)#show plan
    bot.send_message(message.chat.id, "привестую вас в геймификации, введите пожалуста день недели и время когда у вас начинается неделя в формате 0 10.20 день нелели от 0 до 6 понедельник воскресенье соответственно и время через точку час.мин", reply_markup = markup)#start messag
    inp = str(message.chat.id) + "time"
    cursor.execute('INSERT INTO Users (username, plan, score, times) VALUES (?, ?, ?, ?)', (int(message.chat.id), " ", 0, 0))# start in db
    connection.commit()#save db


@bot.message_handler(content_types=['text'])
def func(message):
    global inp#variable for input
    global inptim


    if message.text == "план":#plan
        cursor.execute("SELECT  plan FROM users WHERE username = ?", (message.from_user.id,))#take plan in db
        plan = str(cursor.fetchall())[3:-4]#take plan in db and delete extra
        #output plan
        markup = types.InlineKeyboardMarkup()#for inline

        for i in plan.split(";"):#cycle for do inline but
            button1= types.InlineKeyboardButton(i, callback_data=i)#output inline
            markup.add(button1)
        inp = "0"#variable for input
       #show inline
        print(markup)
        bot.send_message(message.chat.id, "ваш план:", reply_markup = markup)#send text
    elif message.text == "счет":#score
        cursor.execute("SELECT  score FROM users WHERE username = ?", (message.from_user.id,))
        score = int(str(cursor.fetchall())[2:-3])
        bot.send_message(message.chat.id, text=score)
    elif message.text == "ввод план":# input start plan
        date = datetime.datetime.today()
        nowtime = date.strftime('%H.%M')
        cursor.execute("SELECT  times FROM users WHERE username = ?", (message.from_user.id,))
        timedate = str(cursor.fetchall())[3:-4]
        day, time = timedate.split(" ")
        nowday = datetime.datetime.today().weekday()
        print(nowtime,time,day,nowday)
        if int(day) > int(nowday):
            inp = message.from_user.id  # variable for input
            inp = message.from_user.id#variable for input
            bot.send_message(message.chat.id, text="введите план такого типа: #Математика(0/4); *презентация прог; помыть полы ")#output info
            bot.send_message(message.chat.id, text="# обозначает повторения обязательно в конце (0/n)")
            bot.send_message(message.chat.id, text="* обозначает презентацию плюс 5 очков")
            bot.send_message(message.chat.id, text="каждое дело разделять ;")  # output info
        elif int(day) == int(nowday) and int(float(nowtime)) <= int(float(time)):
            inp = message.from_user.id#variable for input
            bot.send_message(message.chat.id, text="введите план такого типа: #Математика(0/4); *презентация прог; помыть полы ")#output info
            bot.send_message(message.chat.id, text="# обозначает повторения обязательно в конце (0/n)")
            bot.send_message(message.chat.id, text="* обозначает презентацию плюс 5 очков")
            bot.send_message(message.chat.id, text="каждое дело разделять ;")
        else:
            bot.send_message(message.chat.id, text="прием плана заверше")
    elif inp == str(message.from_user.id) + "time":
        timedate = message.text
        cursor.execute('UPDATE Users SET times = ? WHERE username = ?', (timedate, message.from_user.id))#save in db
        connection.commit()
        bot.send_message(message.chat.id, text="вы высавили время "+ timedate)  # output scor
        inp = "0"
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
    index = plan.find(str(call.data))
    if index != -1 and plan[index] != "✅" :
        if call.data[0] == "*" or call.data[1] == "*":
            cursor.execute("SELECT  score FROM users WHERE username = ?", (call.from_user.id,))
            score = int(str(cursor.fetchall())[2:-3])
            score += 5
            cursor.execute('UPDATE Users SET score = ? WHERE username = ?', (score, call.from_user.id))  # save in db
            connection.commit()
            bot.answer_callback_query(call.id, call.data)
            string_list = plan
            string_list = string_list[:index] + "✅" + string_list[index:]
            plan = "".join(string_list)
            cursor.execute('UPDATE Users SET plan = ? WHERE username = ?', (plan, call.from_user.id))
            connection.commit()
        elif call.data[0] == "#" or call.data[1] == "#":
            if int(call.data[-2]) -1 == int(call.data[-4]):
                num = str(int(plan[int(index) + len(call.data)-4])+ 1)
                print(num)
                plan = plan[:index + len(call.data)-4] + num + plan[index + len(call.data)-3:]
                print(plan)
                plan = "".join(plan)
                print(plan)
                bot.answer_callback_query(call.id, call.data)
                string_list = plan
                string_list = string_list[:index] + "✅" + string_list[index:]
                plan = "".join(string_list)
                cursor.execute('UPDATE Users SET plan = ? WHERE username = ?', (plan, call.from_user.id))
                connection.commit()
                cursor.execute("SELECT  score FROM users WHERE username = ?", (call.from_user.id,))
                score = int(str(cursor.fetchall())[2:-3])
                score += 2
                cursor.execute('UPDATE Users SET score = ? WHERE username = ?', (score, call.from_user.id))  # save in db
                connection.commit()
            elif call.data[-2] != call.data[-4]:
                num = str(int(plan[int(index) + len(call.data)-4])+ 1)
                print(num)
                plan = plan[:index + len(call.data)-4] + num + plan[index + len(call.data)-3:]
                print(plan)
                plan = "".join(plan)
                print(plan)
                cursor.execute('UPDATE Users SET plan = ? WHERE username = ?', (plan, call.from_user.id))
                connection.commit()
                cursor.execute("SELECT  score FROM users WHERE username = ?", (call.from_user.id,))
                score = int(str(cursor.fetchall())[2:-3])
                score += 1
                cursor.execute('UPDATE Users SET score = ? WHERE username = ?', (score, call.from_user.id))  # save in db
                connection.commit()
        else:
            cursor.execute("SELECT  score FROM users WHERE username = ?", (call.from_user.id,))
            score = int(str(cursor.fetchall())[2:-3])
            score += 1
            cursor.execute('UPDATE Users SET score = ? WHERE username = ?', (score, call.from_user.id))  # save in db
            connection.commit()
            bot.answer_callback_query(call.id, call.data)
            string_list = plan
            string_list = string_list[:index] + "✅" + string_list[index:]
            plan = "".join(string_list)
            print(plan)
            cursor.execute('UPDATE Users SET plan = ? WHERE username = ?', (plan, call.from_user.id))
            connection.commit()
    else:
        bot.answer_callback_query(call.id, "задача выполнена" )
bot.polling(none_stop=True)
connection.close()
"""
tz: Task completion series 
    - = plan +0.5
    
    shop:
    
    random

"""
#kostik<33