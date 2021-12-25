import telebot
from telebot import types
from test3 import Exchange_Rates, Banks

bot = telebot.TeleBot('5037094742:AAEJ7DAEzyxm1QejxpS5IbleFNugiisfZWI')


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, на связи бот для обмена валют в Казани.")
        bot.send_photo(message.chat.id, photo='thumbs.dreamstime.com/b/%D0%B4%D0%BE%D0%B1%D1%80%D0%BE-%D0%BF%D0%BE%D0'
                                              '%B6%D0%B0-%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-35252551.jpg',
                       caption='хе-хе, какая та картинка')
        keyboard = types.InlineKeyboardMarkup()
        key_eur = types.InlineKeyboardButton(text='Купить/продать евро', callback_data='eur')
        keyboard.add(key_eur)
        key_usd = types.InlineKeyboardButton(text='Купить/продать доллар', callback_data='usd')
        keyboard.add(key_usd)
        key_show = types.InlineKeyboardButton(text='Показать курс доллара и евро к рублю', callback_data='show')
        keyboard.add(key_show)
        bot.send_message(message.from_user.id, text='Выберите валюту, которую хотите обменять', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "Напиши привет")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'show':
        bot.send_message(call.message.chat.id, 'Курс доллара к рублю')
        bot.send_message(call.message.chat.id, Exchange_Rates.Dollar())
        bot.send_message(call.message.chat.id, 'Курс евро к рублю')
        bot.send_message(call.message.chat.id, Exchange_Rates.Eur())
        bot.send_message(call.message.chat.id, '______________________________________________________________________')

    if call.data == 'usd':
        bot.send_message(call.message.chat.id, 'Покупка доллара в ЦБ')
        bot.send_message(call.message.chat.id, Banks.Dollar2(0))
        bot.send_message(call.message.chat.id, 'Самая выгодная покупка доллара в Казани')
        bot.send_message(call.message.chat.id, Banks.Dollar2(2))
        bot.send_message(call.message.chat.id, Banks.Dollar_bank(2))
        bot.send_message(call.message.chat.id, 'Самая выгодная продажа доллара в Казани')
        bot.send_message(call.message.chat.id, Banks.Dollar2(1))
        bot.send_message(call.message.chat.id, Banks.Dollar_bank(1))
        bot.send_message(call.message.chat.id, '______________________________________________________________________')

    if call.data == 'eur':
        bot.send_message(call.message.chat.id, 'Покупка евро в ЦБ')
        bot.send_message(call.message.chat.id, Banks.Euro2(0))
        bot.send_message(call.message.chat.id, 'Самая выгодная покупка евро в Казани')
        bot.send_message(call.message.chat.id, Banks.Euro2(2))
        bot.send_message(call.message.chat.id, Banks.Euro_bank(2))
        bot.send_message(call.message.chat.id, 'Самая выгодная продажа евро в Казани')
        bot.send_message(call.message.chat.id, Banks.Euro2(1))
        bot.send_message(call.message.chat.id, Banks.Euro_bank(1))
        bot.send_message(call.message.chat.id, '______________________________________________________________________')


bot.polling(none_stop=True, interval=0)
