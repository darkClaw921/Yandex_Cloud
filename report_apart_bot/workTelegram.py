import os
import random
import telebot
from createKeyboard import *
from datetime import datetime
import bitrix
#from dotenv import load_dotenv
from pprint import pprint
#load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEBOT_TOKEN'))
# инициализация бота и диспетчера
#dp = Dispatcher(bot)

@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    bot.send_message(message.chat.id,
                     'Hi, there! I am hosted by Yandex.Cloud Functions.\n'
                     parse_mode='markdown')

#@bot.callback_query_handler(startswitch('')
#@bot.callback_query_handler(Text(startswith='btn') or Text(startswith='btni_'))


#if call.data == 'test':
#    bot.send_message(call.chat.id, 'Hello')
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call): 
    btn = call.data.split('_')[0]
    print('callback: ',btn)
    pprint(call.message.chat.id)
    if btn == 'btnDeal': 
        #keyboard = create_inline_keyboard(bitrix.get_deals())
        dealID = btn = call.data.split('_')[1] 
        bitrix.create_deal(dealID)
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"Просьба не шуметь отправлена постояльцам",)

    if btn == 'next':
        pprint(call)
        pageNumber= int(call.data.split('_')[2]) + 1
        keyboard = create_inline_keyboard(bitrix.get_deals(), pageNumber)
        bot.answer_callback_query(call.id) 
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Какая квартира шумит?",
                            reply_markup=keyboard)

    if btn == 'prev':
        pprint(call)
        pageNumber= int(call.data.split('_')[2]) - 1
        keyboard = create_inline_keyboard(bitrix.get_deals(), pageNumber)
        bot.answer_callback_query(call.id) 
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Какая квартира шумит?",
                            reply_markup=keyboard)

@bot.message_handler(commands=['button'])
def send_button(message):
    print('отпровляем кнопки')
    #keyboard = create_keyboard_for_deal(bitrix.get_deals())
    keyboard = create_inline_keyboard(bitrix.get_deals())
    bot.send_message(message.chat.id, 
        "Какая квартира шумит?", 
        reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def any_message(message):
    print('это сообщение', message)
    text = message.text.lower()
    userID= message.chat.id
    bot.send_message(message.chat.id, f"Расписание обновляеться, это может занять какое-то время", )    
        
    bot.send_message(message.chat.id, f"Попробуйте еще раз",)
#bot.infinity_polling()