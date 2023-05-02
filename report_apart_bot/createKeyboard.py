import telebot
from loguru import logger
from pprint import pprint 
import math

@logger.catch
def create_inline_keyboard(deals: list, pageCountCallback: int=1 ):
    """_summary_

    Args:
        deals (list): сделки
        pageCountCallback (int, optional): Defaults to 1. Какую страницу мы хотим потулчить

    Returns:
        _types.InlineKeyboardMark_p(): inline клавиатура   
    """
    # Создаем объект клавиатуры и списка кнопок
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = []
    # Переменная для отслеживания количества кнопок
    buttonCount = 0
    # Переменная для отслеживания числа страниц
    pageCount = 1
    # Проходим по всем элементам deals для создания кнопок
    keyboardDict={}
    for deal in deals:
        # Создаем кнопку и добавляем ее в список кнопок
        button = telebot.types.InlineKeyboardButton(text=deal['ID'], callback_data=f"btnDeal_{deal['ID']}")
        buttons.append(button)
        # Увеличиваем счетчик кнопок
        buttonCount += 1
        # Если мы дошли до конца строки 3 (т.е. у нас уже 3 кнопки в строке), то добавляем эту
        # строку в объект клавиатуры и обнуляем список кнопок
        if buttonCount % 3 == 0:
            keyboard.row(*buttons)
            buttons = []
        # Проверяем, достигли ли мы 20 кнопок (т.е. достигли лимита количества кнопок на одной странице)
        # Если да, то добавляем кнопку для перехода на следующую страницу и сбрасываем счетчик кнопок
        if buttonCount == 20:
            keyboard.row(*buttons)
            
            if pageCount == 1: 
                next_button = telebot.types.InlineKeyboardButton(text=">>", callback_data=f"next_page_{pageCount}")
                keyboard.row(next_button)
            elif pageCount >= math.ceil((len(deals)/20)): #last
                prevButton = telebot.types.InlineKeyboardButton(text="<<", callback_data=f"prev_page_{pageCount}")
                keyboard.row(prevButton)
                #keyboardDict.setdefault(pageCount, keyboard)
                # pprint(keyboardDict)
                #return keyboardDict[pageCountCallback] 
            else:
                prevButton = telebot.types.InlineKeyboardButton(text="<<", callback_data=f"prev_page_{pageCount}")
                nextButton = telebot.types.InlineKeyboardButton(text=">>", callback_data=f"next_page_{pageCount}")
                keyboard.row(prevButton, nextButton)

            buttonCount = 0
            buttons = []
            keyboardDict.setdefault(pageCount, keyboard)
            keyboard = telebot.types.InlineKeyboardMarkup() 
            pageCount += 1
            print(f'{pageCount}')

    # Добавляем остаток списка кнопок в объект клавиатуры
    if buttonCount !=0:
        print('Добавляем остаток списка кнопок в объект клавиатуры')
        keyboard.row(*buttons)
        prevButton = telebot.types.InlineKeyboardButton(text="<<", callback_data=f"prev_page_{pageCount}")
        keyboard.row(prevButton)
        keyboardDict.setdefault(pageCount, keyboard)

    # Если страниц больше, чем 1 (т.е. мы создали более 20 кнопок), то добавляем кнопки навигации
    # if pageCount > 1:
    #     prevButton = telebot.types.InlineKeyboardButton(text="<<", callback_data=f"prev_page_{pageCount}")
    #     nextButton = telebot.types.InlineKeyboardButton(text=">>", callback_data=f"next_page_{pageCount}")
    #     keyboard.row(prevButton, nextButton)
    pprint(keyboardDict)
    return keyboardDict[pageCountCallback] 

def create_menu_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Соседи шумят')
    keyboard.row('Мои занятия')
    
    return keyboard