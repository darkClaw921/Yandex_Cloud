import os
import json
from workTelegram import bot
import telebot
from datetime import datetime

def handler(event, context):
    #p = event['messages'][0]['details']['message']['body']
    p = event['body'].replace('false', 'False',).replace('true', 'True')
    print(p)
    p=eval(p)
    message = telebot.types.Update.de_json(p)

    bot.process_new_updates([message])
    #message = eval(p)
  
    return {
        'statusCode': 200,
        'body': 'Hello World!',
    }