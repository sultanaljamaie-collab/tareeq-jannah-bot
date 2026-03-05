import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

scores = {}
users = set()
user_answers = {}

questions = [
{"q":"كم عدد أركان الإسلام؟","o":["4","5","6","7"],"a":"5"},
{"q":"كم عدد أركان الإيمان؟","o":["5","6","7","8"],"a":"6"},
{"q":"ما أول سورة في القرآن؟","o":["الفاتحة","البقرة","الإخلاص","الفلق"],"a":"الفاتحة"},
{"q":"كم عدد الصلوات المفروضة؟","o":["3","4","5","6"],"a":"5"},
{"q":"من هو خاتم الأنبياء؟","o":["موسى","عيسى","محمد ﷺ","إبراهيم"],"a":"محمد ﷺ"},
{"q":"في أي شهر يصوم المسلمون؟","o":["رمضان","شعبان","رجب","ذو الحجة"],"a":"رمضان"},
{"q":"كم عدد سور القرآن؟","o":["114","110","120","100"],"a":"114"},
{"q":"أين ولد النبي محمد ﷺ؟","o":["مكة","المدينة","الطائف","الشام"],"a":"مكة"},
{"q":"كم عدد الصلوات في اليوم؟","o":["3","4","5","6"],"a":"5"},
{"q":"ما اسم كتاب المسلمين؟","o":["التوراة","الإنجيل","القرآن","الزبور"],"a":"القرآن"}
]

ayat = [
"﴿إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾",
"﴿اللَّهُ خَالِقُ كُلِّ شَيْءٍ﴾",
"﴿وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا لِيَعْبُدُونِ﴾",
"﴿وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ﴾"
]

@bot.message_handler(commands=['start'])
def start(message):

    users.add(message.chat.id)

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add("🧠 اختبر معلوماتك")
    keyboard.add("📚 آية اليوم")
    keyboard.add("🏆 نقاطي")
    keyboard.add("🥇 المتصدرون")
    keyboard.add("📊 عدد المستخدمين")

    bot.send_message(
        message.chat.id,
        "🌙 أهلاً بك في بوت طريق الجنة",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda m: m.text=="📚 آية اليوم")
def verse(message):

    bot.send_message(message.chat.id,random.choice(ayat))

@bot.message_handler(func=lambda m: m.text=="🧠 اختبر معلوماتك")
def quiz(message):

    q=random.choice(questions)

    user_answers[message.chat.id]=q["a"]

    markup=InlineKeyboardMarkup()

    for opt in q["o"]:
        markup.add(InlineKeyboardButton(opt,callback_data=opt))

    bot.send_message(message.chat.id,"❓ "+q["q"],reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def answer(call):

    user_id=call.message.chat.id

    correct=user_answers.get(user_id)

    if call.data==correct:

        scores[user_id]=scores.get(user_id,0)+1

        bot.send_message(user_id,"✅ إجابة صحيحة\n\nنقاطك: "+str(scores[user_id]))

    else:

        bot.send_message(user_id,"❌ إجابة خاطئة")

@bot.message_handler(func=lambda m: m.text=="🏆 نقاطي")
def points(message):

    score=scores.get(message.chat.id,0)

    bot.send_message(message.chat.id,"🏆 مجموع نقاطك: "+str(score))

@bot.message_handler(func=lambda m: m.text=="🥇 المتصدرون")
def leaderboard(message):

    if not scores:
        bot.send_message(message.chat.id,"لا يوجد متصدرون بعد.")
        return

    top=sorted(scores.items(),key=lambda x:x[1],reverse=True)[:5]

    text="🥇 لوحة المتصدرين\n\n"

    for i,(user,score) in enumerate(top,1):

        text+=str(i)+"️⃣ — "+str(score)+" نقطة\n"

    bot.send_message(message.chat.id,text)

@bot.message_handler(func=lambda m: m.text=="📊 عدد المستخدمين")
def stats(message):

    bot.send_message(message.chat.id,"👥 عدد مستخدمي البوت: "+str(len(users)))

bot.infinity_polling()
