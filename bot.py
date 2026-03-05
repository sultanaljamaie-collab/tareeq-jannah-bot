import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

# قائمة الأسئلة
questions = [
    {
        "question": "كم عدد أركان الإسلام؟",
        "options": ["4", "5", "6", "7"],
        "answer": "5"
    },
    {
        "question": "كم عدد أركان الإيمان؟",
        "options": ["5", "6", "7", "8"],
        "answer": "6"
    },
    {
        "question": "ما أول سورة في القرآن؟",
        "options": ["الفاتحة", "البقرة", "الإخلاص", "الفلق"],
        "answer": "الفاتحة"
    },
    {
        "question": "كم عدد الصلوات المفروضة؟",
        "options": ["3", "4", "5", "6"],
        "answer": "5"
    },
    {
        "question": "من هو خاتم الأنبياء؟",
        "options": ["موسى", "عيسى", "محمد ﷺ", "إبراهيم"],
        "answer": "محمد ﷺ"
    }
]

# آيات
ayat = [
    "﴿إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾",
    "﴿اللَّهُ خَالِقُ كُلِّ شَيْءٍ﴾",
    "﴿وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ﴾",
    "﴿وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا لِيَعْبُدُونِ﴾"
]


@bot.message_handler(commands=['start'])
def start(message):

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add("📖 تعلم عن الإسلام")
    keyboard.add("🔭 دلائل وجود الله")
    keyboard.add("🧠 اختبر معلوماتك")
    keyboard.add("📚 آية اليوم")
    keyboard.add("❓ اسأل عن الإسلام")

    bot.send_message(
        message.chat.id,
        "🌙 أهلاً بك في بوت طريق الجنة\n\nاختر من القائمة:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda m: m.text == "📖 تعلم عن الإسلام")
def islam(message):

    bot.send_message(
        message.chat.id,
        """
الإسلام هو دين التوحيد

يؤمن المسلمون أن الله واحد لا شريك له
وأن محمد ﷺ رسول الله.
"""
    )


@bot.message_handler(func=lambda m: m.text == "🔭 دلائل وجود الله")
def proof(message):

    bot.send_message(
        message.chat.id,
        """
قال الله تعالى:

﴿أَمْ خُلِقُوا مِنْ غَيْرِ شَيْءٍ أَمْ هُمُ الْخَالِقُونَ﴾
"""
    )


@bot.message_handler(func=lambda m: m.text == "📚 آية اليوم")
def verse(message):

    ayah = random.choice(ayat)

    bot.send_message(
        message.chat.id,
        "📖 آية للتأمل:\n\n" + ayah
    )


@bot.message_handler(func=lambda m: m.text == "🧠 اختبر معلوماتك")
def quiz(message):

    q = random.choice(questions)

    markup = InlineKeyboardMarkup()

    for option in q["options"]:
        markup.add(InlineKeyboardButton(option, callback_data=option))

    bot.send_message(
        message.chat.id,
        "❓ " + q["question"],
        reply_markup=markup
    )

    bot.register_next_step_handler(message, lambda msg: None)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):

    if call.data in ["5", "6", "الفاتحة", "محمد ﷺ"]:

        bot.send_message(
            call.message.chat.id,
            "✅ إجابة صحيحة"
        )

    else:

        bot.send_message(
            call.message.chat.id,
            "❌ إجابة خاطئة"
        )


@bot.message_handler(func=lambda m: m.text == "❓ اسأل عن الإسلام")
def ask(message):

    bot.send_message(
        message.chat.id,
        "اكتب سؤالك عن الإسلام وسنجيبك."
    )


bot.infinity_polling()
