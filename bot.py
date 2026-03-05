import telebot
import os
import random
import threading
import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from questions import questions
from prophets import prophets
from achievements import get_medal
from daily import daily_question
from levels import quiz_levels
from voice import speak

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

QUESTION_TIME = 30

scores = {}
answers = {}
timer_running = {}
users = set()

user_level = {}
question_count = {}
correct_answers = {}

@bot.message_handler(commands=['start'])
def start(message):

    users.add(message.chat.id)

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add("🎮 المسابقة","🔥 التحدي اليومي")
    keyboard.add("📜 قصص الأنبياء","🏆 نقاطي")

    bot.send_message(
        message.chat.id,
        "🌙 مرحبا بك في بوت طريق الجنة\nاختر من القائمة:",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda m: m.text=="🎮 المسابقة")
def choose_level(message):

    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton("🟢 سهل",callback_data="level_easy"))
    markup.add(InlineKeyboardButton("🟡 متوسط",callback_data="level_medium"))
    markup.add(InlineKeyboardButton("🔵 متقدم",callback_data="level_hard"))
    markup.add(InlineKeyboardButton("🔴 عالم",callback_data="level_master"))

    bot.send_message(
        message.chat.id,
        "اختر مستوى المسابقة:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("level_"))
def set_level(call):

    user = call.message.chat.id

    level = call.data.replace("level_","")

    user_level[user] = level
    question_count[user] = 0
    correct_answers[user] = 0

    voice = speak("بدأت المسابقة")

    bot.send_voice(user,open(voice,"rb"))

    send_question(user)

def send_question(user):

    level = user_level[user]

    total = quiz_levels[level]

    if question_count[user] >= total:

        score = correct_answers[user]

        medal = get_medal(scores.get(user,0))

        voice = speak("انتهت المسابقة")

        bot.send_voice(user,open(voice,"rb"))

        bot.send_message(
            user,
            f"🎉 انتهت المسابقة\n\n"
            f"الإجابات الصحيحة {score} من {total}\n"
            f"النقاط {scores.get(user,0)}\n"
            f"{medal}"
        )

        return

    question_count[user] += 1

    q = random.choice(questions)

    answers[user] = q["answer"]

    markup = InlineKeyboardMarkup()

    for opt in q["options"]:
        markup.add(
            InlineKeyboardButton(
                opt,
                callback_data="quiz_"+opt
            )
        )

    bot.send_message(
        user,
        f"السؤال {question_count[user]} من {total}\n"
        f"⏱ {QUESTION_TIME} ثانية\n\n"
        f"❓ {q['question']}",
        reply_markup=markup
    )

    voice = speak(q["question"])

    bot.send_voice(user,open(voice,"rb"))

    timer_running[user] = True

    start_timer(user)

def start_timer(user):

    def timer():

        for i in range(QUESTION_TIME,0,-1):

            if not timer_running.get(user):
                return

            time.sleep(1)

        scores[user] = scores.get(user,0)-2

        voice = speak("انتهى الوقت")

        bot.send_voice(user,open(voice,"rb"))

        bot.send_message(user,"⏰ انتهى الوقت\n-2 نقاط")

        send_question(user)

    threading.Thread(target=timer).start()

@bot.callback_query_handler(func=lambda call: call.data.startswith("quiz_"))
def answer(call):

    user = call.message.chat.id

    timer_running[user] = False

    ans = call.data.replace("quiz_","")

    correct = answers.get(user)

    if ans == correct:

        scores[user] = scores.get(user,0)+1

        correct_answers[user] += 1

        voice = speak("إجابة صحيحة أحسنت")

        bot.send_voice(user,open(voice,"rb"))

        bot.send_message(user,"✅ إجابة صحيحة")

    else:

        scores[user] = scores.get(user,0)-2

        voice = speak("إجابة خاطئة")

        bot.send_voice(user,open(voice,"rb"))

        bot.send_message(user,"❌ إجابة خاطئة\n-2 نقاط")

    send_question(user)

@bot.message_handler(func=lambda m: m.text=="🔥 التحدي اليومي")
def daily(message):

    q = daily_question()

    bot.send_message(
        message.chat.id,
        f"🔥 تحدي اليوم\n\n{q['question']}"
    )

@bot.message_handler(func=lambda m: m.text=="🏆 نقاطي")
def points(message):

    score = scores.get(message.chat.id,0)

    medal = get_medal(score)

    bot.send_message(
        message.chat.id,
        f"🏆 نقاطك: {score}\n{medal}"
    )

@bot.message_handler(func=lambda m: m.text=="📜 قصص الأنبياء")
def prophets_menu(message):

    markup = InlineKeyboardMarkup()

    for name in prophets.keys():

        markup.add(
            InlineKeyboardButton(
                name,
                callback_data="prophet_"+name
            )
        )

    bot.send_message(
        message.chat.id,
        "اختر نبي:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("prophet_"))
def prophet_story(call):

    name = call.data.replace("prophet_","")

    bot.send_message(
        call.message.chat.id,
        prophets[name]
    )

bot.infinity_polling()
