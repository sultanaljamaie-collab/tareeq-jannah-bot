import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import threading
import time

TOKEN = os.getenv("TOKEN")

ADMIN_ID = 1330477563

bot = telebot.TeleBot(TOKEN)

scores={}
users=set()
asking=set()

current_question={}
question_message={}
timer_running={}

user_level={}
question_count={}
correct_answers={}

quiz_levels={
"easy":10,
"medium":50,
"hard":100,
"master":500
}

questions=[

{"q":"كم عدد أركان الإسلام؟","o":["4","5","6","7"],"a":"5"},
{"q":"كم عدد أركان الإيمان؟","o":["5","6","7","8"],"a":"6"},
{"q":"كم عدد الصلوات المفروضة؟","o":["3","4","5","6"],"a":"5"},
{"q":"كم عدد سور القرآن؟","o":["110","114","120","124"],"a":"114"},
{"q":"ما أول سورة في القرآن؟","o":["الفاتحة","البقرة","الإخلاص","الناس"],"a":"الفاتحة"},
{"q":"من هو خاتم الأنبياء؟","o":["موسى","عيسى","محمد ﷺ","إبراهيم"],"a":"محمد ﷺ"},
{"q":"في أي شهر يصوم المسلمون؟","o":["رمضان","شعبان","رجب","ذو الحجة"],"a":"رمضان"}

]

ayat=[
"﴿إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾",
"﴿اللَّهُ خَالِقُ كُلِّ شَيْءٍ﴾",
"﴿إِنَّ اللَّهَ مَعَ الصَّابِرِينَ﴾"
]

hadith=[
"قال رسول الله ﷺ: «إنما الأعمال بالنيات»",
"قال رسول الله ﷺ: «الدين النصيحة»",
"قال رسول الله ﷺ: «خيركم من تعلم القرآن وعلمه»"
]

stories={
"آدم":"آدم عليه السلام أول إنسان خلقه الله.",
"نوح":"نوح عليه السلام دعا قومه لعبادة الله.",
"إبراهيم":"إبراهيم عليه السلام دعا إلى التوحيد.",
"موسى":"موسى عليه السلام أرسله الله إلى فرعون.",
"عيسى":"عيسى عليه السلام ولد بمعجزة.",
"محمد ﷺ":"محمد ﷺ خاتم الأنبياء."
}

@bot.message_handler(commands=['start'])
def start(message):

    users.add(message.chat.id)

    keyboard=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add("📖 تعلم عن الإسلام","🔭 دلائل وجود الله")
    keyboard.add("📚 آية اليوم","🕌 حديث نبوي")
    keyboard.add("📜 قصص الأنبياء","🌍 Discover Islam")
    keyboard.add("🎮 المسابقة","🏆 نقاطي")
    keyboard.add("🥇 المتصدرون","📊 عدد المستخدمين")
    keyboard.add("❓ اسأل عن الإسلام")

    bot.send_message(message.chat.id,
    "🌙 أهلاً بك في بوت طريق الجنة",
    reply_markup=keyboard)

@bot.message_handler(func=lambda m:m.text=="📖 تعلم عن الإسلام")
def islam(message):

    bot.send_message(message.chat.id,
    "الإسلام هو عبادة الله وحده واتباع النبي محمد ﷺ")

@bot.message_handler(func=lambda m:m.text=="🔭 دلائل وجود الله")
def proof(message):

    bot.send_message(message.chat.id,
    "من دلائل وجود الله: خلق الكون والإنسان ونظام الطبيعة")

@bot.message_handler(func=lambda m:m.text=="📚 آية اليوم")
def verse(message):

    bot.send_message(message.chat.id,random.choice(ayat))

@bot.message_handler(func=lambda m:m.text=="🕌 حديث نبوي")
def hadith_send(message):

    bot.send_message(message.chat.id,random.choice(hadith))

@bot.message_handler(func=lambda m:m.text=="📜 قصص الأنبياء")
def prophets(message):

    text="اختر نبي:\n\n"

    for name in stories:

        text+=name+"\n"

    bot.send_message(message.chat.id,text)

@bot.message_handler(func=lambda m:m.text in stories)
def story(message):

    bot.send_message(message.chat.id,stories[message.text])

@bot.message_handler(func=lambda m:m.text=="🌍 Discover Islam")
def english(message):

    bot.send_message(message.chat.id,
    "Islam means worshiping One God and following Prophet Muhammad.")

@bot.message_handler(func=lambda m:m.text=="🎮 المسابقة")
def choose_level(message):

    markup=InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton("🟢 سهل",callback_data="level_easy"))
    markup.add(InlineKeyboardButton("🟡 متوسط",callback_data="level_medium"))
    markup.add(InlineKeyboardButton("🔵 متقدم",callback_data="level_hard"))
    markup.add(InlineKeyboardButton("🔴 عالم",callback_data="level_master"))

    bot.send_message(message.chat.id,
    "اختر مستوى المسابقة",
    reply_markup=markup)

@bot.callback_query_handler(func=lambda call:call.data.startswith("level_"))
def set_level(call):

    user=call.message.chat.id

    level=call.data.replace("level_","")

    user_level[user]=level

    question_count[user]=0

    correct_answers[user]=0

    send_question(user)

def send_question(user):

    level=user_level[user]

    total=quiz_levels[level]

    if question_count[user]>=total:

        bot.send_message(user,
        f"🎉 انتهت المسابقة\n\n"
        f"الإجابات الصحيحة: {correct_answers[user]} / {total}\n"
        f"النقاط: {scores.get(user,0)}")

        return

    question_count[user]+=1

    q=random.choice(questions)

    current_question[user]=q

    markup=InlineKeyboardMarkup()

    for opt in q["o"]:
        markup.add(InlineKeyboardButton(opt,callback_data="quiz_"+opt))

    msg=bot.send_message(user,
    f"السؤال {question_count[user]} / {total}\n\n⏱ 60 ثانية\n\n❓ {q['q']}",
    reply_markup=markup)

    question_message[user]=msg.message_id

    timer_running[user]=True

    start_timer(user)

def start_timer(user):

    def countdown():

        for i in range(60,0,-1):

            if not timer_running.get(user):
                return

            q=current_question[user]

            markup=InlineKeyboardMarkup()

            for opt in q["o"]:
                markup.add(InlineKeyboardButton(opt,callback_data="quiz_"+opt))

            try:

                bot.edit_message_text(
                chat_id=user,
                message_id=question_message[user],
                text=f"السؤال {question_count[user]}\n\n⏱ {i} ثانية\n\n❓ {q['q']}",
                reply_markup=markup)

            except:
                pass

            time.sleep(1)

        timeout(user)

    threading.Thread(target=countdown).start()

def timeout(user):

    scores[user]=scores.get(user,0)-2

    bot.send_message(user,"⏰ انتهى الوقت\n-2 نقاط")

    send_question(user)

@bot.callback_query_handler(func=lambda call:call.data.startswith("quiz_"))
def answer(call):

    user=call.message.chat.id

    timer_running[user]=False

    ans=call.data.replace("quiz_","")

    correct=current_question[user]["a"]

    if ans==correct:

        scores[user]=scores.get(user,0)+1

        correct_answers[user]+=1

        bot.send_message(user,"✅ إجابة صحيحة")

    else:

        scores[user]=scores.get(user,0)-2

        bot.send_message(user,"❌ إجابة خاطئة\n-2 نقاط")

    send_question(user)

@bot.message_handler(func=lambda m:m.text=="🏆 نقاطي")
def points(message):

    bot.send_message(message.chat.id,
    "نقاطك: "+str(scores.get(message.chat.id,0)))

@bot.message_handler(func=lambda m:m.text=="🥇 المتصدرون")
def leaderboard(message):

    top=sorted(scores.items(),
    key=lambda x:x[1],
    reverse=True)[:5]

    text="لوحة المتصدرين\n\n"

    for i,(user,score) in enumerate(top,1):

        text+=str(i)+" - "+str(score)+" نقطة\n"

    bot.send_message(message.chat.id,text)

@bot.message_handler(func=lambda m:m.text=="📊 عدد المستخدمين")
def stats(message):

    bot.send_message(message.chat.id,
    "عدد المستخدمين: "+str(len(users)))

@bot.message_handler(func=lambda m:m.text=="❓ اسأل عن الإسلام")
def ask(message):

    asking.add(message.chat.id)

    bot.send_message(message.chat.id,"اكتب سؤالك")

@bot.message_handler(func=lambda m:m.chat.id in asking)
def forward_question(message):

    asking.remove(message.chat.id)

    bot.send_message(ADMIN_ID,
    "سؤال جديد:\n"+message.text)

    bot.send_message(message.chat.id,
    "تم إرسال السؤال")

bot.infinity_polling()
