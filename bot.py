import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add("📖 تعلم عن الإسلام")
    keyboard.add("🔭 دلائل وجود الله")
    keyboard.add("🧠 اختبر معلوماتك")

    bot.send_message(
        message.chat.id,
        "🌙 أهلاً بك في بوت طريق الجنة\n\nاختر من القائمة:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda m: m.text == "📖 تعلم عن الإسلام")
def islam(message):

    bot.send_message(
        message.chat.id,
        "الإسلام هو عبادة الله وحده واتباع رسول الله محمد ﷺ"
    )


@bot.message_handler(func=lambda m: m.text == "🔭 دلائل وجود الله")
def proof(message):

    bot.send_message(
        message.chat.id,
        "قال الله تعالى:\n\n﴿أَمْ خُلِقُوا مِنْ غَيْرِ شَيْءٍ أَمْ هُمُ الْخَالِقُونَ﴾"
    )


@bot.message_handler(func=lambda m: m.text == "🧠 اختبر معلوماتك")
def quiz(message):

    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton("4", callback_data="wrong")
    btn2 = InlineKeyboardButton("5", callback_data="correct")
    btn3 = InlineKeyboardButton("6", callback_data="wrong")
    btn4 = InlineKeyboardButton("7", callback_data="wrong")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(
        message.chat.id,
        "❓ كم عدد أركان الإسلام؟",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def answer(call):

    if call.data == "correct":

        bot.send_message(
            call.message.chat.id,
            "✅ إجابة صحيحة\n\nأركان الإسلام خمسة."
        )

    else:

        bot.send_message(
            call.message.chat.id,
            "❌ إجابة خاطئة حاول مرة أخرى."
        )


bot.infinity_polling()
