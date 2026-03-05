import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from gtts import gTTS
import random
import os
import threading
import time

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

quiz_levels = {
"easy":10,
"medium":50,
"hard":100,
"master":500
}

questions = [

{"q":"كم عدد أركان الإسلام؟","o":["4","5","6","7"],"a":"5"},
{"q":"كم عدد أركان الإيمان؟","o":["5","6","7","8"],"a":"6"},
{"q":"كم عدد سور القرآن؟","o":["110","114","120","124"],"a":"114"},
{"q":"ما أول سورة في القرآن؟","o":["الفاتحة","البقرة","الإخلاص","الناس"],"a":"الفاتحة"},
{"q":"من هو خاتم الأنبياء؟","o":["موسى","عيسى","محمد ﷺ","إبراهيم"],"a":"محمد ﷺ"}

]

def speak(text):

    tts = gTTS(text=text, lang="ar")

    file = "voice.mp3"

    tts.save(file)

    return file


@bot.message_handler(commands=['start'])
def start(message):

    users.add(message.chat.id)

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add("🎮 المسابقة","🔥 التحدي اليومي")
    keyboard.add("🏆 نقاطي","🥇 المتصدرون")

    bot.send_message(
        message.chat.id,
        "مرحبا بك في طريق الجنة",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda m: m.text=="🎮 المسابقة")
def choose_level(message):

    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton("🟢 سهل",callback_data="level_easy"))
    markup.add(InlineKeyboardButton("🟡 متوسط",callback_data="level_medium"))
    markup.add(InlineKeyboardButton("🔵 متقدم",callback_data="level_hard"))
    markup.add(InlineKeyboardButton("🔴 عالم",callback_data="level_master"))

    bot.send_message(message.chat.id,"اختر المستوى",reply_markup=markup)


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

        voice = speak("انتهت المسابقة")

        bot.send_voice(user,open(voice,"rb"))

        bot.send_message(user,
        f"🎉 انتهت المسابقة\n\n"
        f"الإجابات الصحيحة {score} من {total}\n"
        f"النقاط {scores.get(user,0)}")

        return

    question_count[user] += 1

    q = random.choice(questions)

    answers[user] = q["a"]

    markup = InlineKeyboardMarkup()

    for opt in q["o"]:
        markup.add(InlineKeyboardButton(opt,callback_data="quiz_"+opt))

    msg = bot.send_message(
        user,
        f"السؤال {question_count[user]} من {total}\n\n⏱ {QUESTION_TIME} ثانية\n\n❓ {q['q']}",
        reply_markup=markup
    )

    voice = speak(q["q"])

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


@bot.message_handler(func=lambda m: m.text=="🏆 نقاطي")
def points(message):

    score = scores.get(message.chat.id,0)

    bot.send_message(message.chat.id,f"🏆 نقاطك {score}")


@bot.message_handler(func=lambda m: m.text=="🥇 المتصدرون")
def leaderboard(message):

    top = sorted(scores.items(),key=lambda x:x[1],reverse=True)[:5]

    text = "🥇 لوحة المتصدرين\n\n"

    for i,(user,score) in enumerate(top,1):

        text += f"{i} - {score} نقطة\n"

    bot.send_message(message.chat.id,text)


@bot.message_handler(func=lambda m: m.text=="🔥 التحدي اليومي")
def daily(message):

    q = random.choice(questions)

    voice = speak("تحدي اليوم")

    bot.send_voice(message.chat.id,open(voice,"rb"))

    bot.send_message(message.chat.id,q["q"])


bot.infinity_polling()
