import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

TOKEN = os.getenv("TOKEN")

# ضع هنا آيدي حسابك في تلجرام ليصلك سؤال المستخدم
ADMIN_ID = 1330477563

bot = telebot.TeleBot(TOKEN)

scores = {}
users = set()
answers = {}
asking = set()

# أسئلة موثوقة
questions = [
{"q":"كم عدد أركان الإسلام؟","o":["4","5","6","7"],"a":"5"},
{"q":"كم عدد أركان الإيمان؟","o":["5","6","7","8"],"a":"6"},
{"q":"كم عدد الصلوات المفروضة؟","o":["3","4","5","6"],"a":"5"},
{"q":"كم عدد سور القرآن؟","o":["110","114","120","124"],"a":"114"},
{"q":"ما أول سورة في القرآن؟","o":["الفاتحة","البقرة","الإخلاص","الناس"],"a":"الفاتحة"},
{"q":"من هو خاتم الأنبياء؟","o":["موسى","عيسى","محمد ﷺ","إبراهيم"],"a":"محمد ﷺ"},
{"q":"في أي شهر يصوم المسلمون؟","o":["رمضان","شعبان","رجب","ذو الحجة"],"a":"رمضان"},
{"q":"أين ولد النبي محمد ﷺ؟","o":["مكة","المدينة","الطائف","القدس"],"a":"مكة"}
]

# آيات
ayat = [
"﴿إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾",
"﴿اللَّهُ خَالِقُ كُلِّ شَيْءٍ﴾",
"﴿إِنَّ اللَّهَ مَعَ الصَّابِرِينَ﴾",
"﴿وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا لِيَعْبُدُونِ﴾"
]

# أحاديث
hadith = [
"قال رسول الله ﷺ: «إنما الأعمال بالنيات»",
"قال رسول الله ﷺ: «الدين النصيحة»",
"قال رسول الله ﷺ: «خيركم من تعلم القرآن وعلمه»",
"قال رسول الله ﷺ: «المسلم من سلم المسلمون من لسانه ويده»"
]

# قصص مختصرة
stories = {
"آدم":"آدم عليه السلام أول إنسان خلقه الله وأسكنه الجنة.",
"نوح":"نوح عليه السلام دعا قومه لعبادة الله وصنع السفينة.",
"إبراهيم":"إبراهيم عليه السلام دعا إلى التوحيد وحطم الأصنام.",
"موسى":"موسى عليه السلام أرسله الله إلى فرعون.",
"عيسى":"عيسى عليه السلام ولد بمعجزة دون أب.",
"محمد ﷺ":"محمد ﷺ خاتم الأنبياء أرسله الله رحمة للعالمين."
}


@bot.message_handler(commands=['start'])
def start(message):

    users.add(message.chat.id)

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add("📖 تعلم عن الإسلام")
    keyboard.add("🔭 دلائل وجود الله")
    keyboard.add("🧠 اختبر معلوماتك")

    keyboard.add("📚 آية اليوم")
    keyboard.add("🕌 حديث نبوي")

    keyboard.add("📜 قصص الأنبياء")
    keyboard.add("🌍 Discover Islam")

    keyboard.add("❓ اسأل عن الإسلام")

    keyboard.add("🏆 نقاطي")
    keyboard.add("🥇 المتصدرون")

    keyboard.add("📊 عدد المستخدمين")

    bot.send_message(
        message.chat.id,
        "🌙 أهلاً بك في بوت طريق الجنة\n\nاختر من القائمة:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda m: m.text=="📖 تعلم عن الإسلام")
def islam(message):

    bot.send_message(message.chat.id,
"""
الإسلام هو عبادة الله وحده
واتباع النبي محمد ﷺ.

﴿إِنَّ الدِّينَ عِندَ اللَّهِ الإِسْلَامُ﴾
""")


@bot.message_handler(func=lambda m: m.text=="🔭 دلائل وجود الله")
def proof(message):

    bot.send_message(message.chat.id,
"""
من دلائل وجود الله:

• دقة الكون
• خلق الإنسان
• نظام الليل والنهار

﴿أَمْ خُلِقُوا مِنْ غَيْرِ شَيْءٍ﴾
""")


@bot.message_handler(func=lambda m: m.text=="📚 آية اليوم")
def verse(message):

    bot.send_message(message.chat.id, random.choice(ayat))


@bot.message_handler(func=lambda m: m.text=="🕌 حديث نبوي")
def hadith_send(message):

    bot.send_message(message.chat.id, random.choice(hadith))


@bot.message_handler(func=lambda m: m.text=="📜 قصص الأنبياء")
def prophets(message):

    text="📜 اختر نبي:\n\n"

    for name in stories:
        text += name + "\n"

    bot.send_message(message.chat.id,text)


@bot.message_handler(func=lambda m: m.text in stories)
def story(message):

    bot.send_message(message.chat.id,stories[message.text])


@bot.message_handler(func=lambda m: m.text=="🧠 اختبر معلوماتك")
def quiz(message):

    q = random.choice(questions)

    answers[message.chat.id] = q["a"]

    markup = InlineKeyboardMarkup()

    for opt in q["o"]:
        markup.add(InlineKeyboardButton(opt,callback_data=opt))

    bot.send_message(message.chat.id,"❓ "+q["q"],reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):

    user = call.message.chat.id

    correct = answers.get(user)

    if call.data == correct:

        scores[user] = scores.get(user,0) + 1

        bot.send_message(user,"✅ إجابة صحيحة\n🏆 نقاطك: "+str(scores[user]))

    else:

        bot.send_message(user,"❌ إجابة خاطئة")


@bot.message_handler(func=lambda m: m.text=="🏆 نقاطي")
def points(message):

    bot.send_message(message.chat.id,"🏆 نقاطك: "+str(scores.get(message.chat.id,0)))


@bot.message_handler(func=lambda m: m.text=="🥇 المتصدرون")
def leaderboard(message):

    if not scores:
        bot.send_message(message.chat.id,"لا يوجد متصدرون بعد.")
        return

    top = sorted(scores.items(),key=lambda x:x[1],reverse=True)[:5]

    text="🥇 لوحة المتصدرين\n\n"

    for i,(user,score) in enumerate(top,1):
        text+=str(i)+"️⃣ "+str(score)+" نقطة\n"

    bot.send_message(message.chat.id,text)


@bot.message_handler(func=lambda m: m.text=="📊 عدد المستخدمين")
def stats(message):

    bot.send_message(message.chat.id,"👥 عدد المستخدمين: "+str(len(users)))


# سؤال المستخدم
@bot.message_handler(func=lambda m: m.text=="❓ اسأل عن الإسلام")
def ask(message):

    asking.add(message.chat.id)

    bot.send_message(message.chat.id,"اكتب سؤالك وسيرسله البوت للإدارة.")


@bot.message_handler(func=lambda m: m.chat.id in asking)
def forward_question(message):

    asking.remove(message.chat.id)

    bot.send_message(ADMIN_ID,"📩 سؤال جديد:\n\n"+message.text)

    bot.send_message(message.chat.id,"تم إرسال سؤالك وسيتم الرد عليك قريبًا.")


# قسم الإنجليزي
@bot.message_handler(func=lambda m: m.text=="🌍 Discover Islam")
def english(message):

    bot.send_message(message.chat.id,
"""
Islam means submitting to One God.

Muslims believe:

• God is One
• Muhammad is His final messenger
• The Quran is the word of God
""")

bot.infinity_polling()
