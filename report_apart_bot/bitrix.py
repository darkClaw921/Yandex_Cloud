from fast_bitrix24 import Bitrix
from dataclasses import dataclass
import os
from pprint import pprint
import math
import traceback
from dotenv import load_dotenv
load_dotenv()


webhook = os.getenv('webHook')
bit = Bitrix(webhook)

@dataclass
class Crm:
    categotyIDLiveBreak: int = 3 # ID категории "прожывание выезд"
    categotyIDRobot: int = 7 # ID категории "робот"
    STAGE_SEMANTIC_ID: str = 'P' # ID стадии "в работе" 

def get_deals():
    deals = bit.call('crm.deal.list', 
            {'ORDER': { "ID": "ASC" },
            'FILTER':{'CATEGORY_ID': Crm.categotyIDLiveBreak,
                      'STAGE_SEMANTIC_ID': Crm.STAGE_SEMANTIC_ID},
            }, raw=True)
    dealsTrue = deals['result']
    startTotal = deals['next']
    #pprint(deals) 
    try:
        while deals['total'] > startTotal:
            #print(deals['next'], deals['total']) 
            dealsNext = bit.call('crm.deal.list', 
                {'ORDER': { "ID": "ASC" },
                'FILTER':{'CATEGORY_ID': Crm.categotyIDLiveBreak,
                        'STAGE_SEMANTIC_ID': Crm.STAGE_SEMANTIC_ID},
                'start': startTotal,
                }, raw=True)
            dealsTrue = dealsTrue + dealsNext['result']     
            
            startTotal =dealsNext['next']
            #print(f'{startTotal=}') 
            pprint(deals)

    except Exception as e :
        print(f'ошибка bitrix',e)
        print(traceback.format_exc())

    return dealsTrue
        


    #pprint(deals)
    
    # lenStart = deals['total'] // 50
    # start = 0
    # dealsTrue = deals['result']
    # for i in range(1, math.ceil(lenStart)):
    #     start = 50 * i
    #     #print('start', start)
    #     # pprint(params)
    #     dealsStart = bit.call('crm.deal.list', 
    #         {'ORDER': { "ID": "ASC" },
    #         'FILTER':{'CATEGORY_ID': Crm.categotyIDLiveBreak,
    #                   'STAGE_SEMANTIC_ID': Crm.STAGE_SEMANTIC_ID},
    #         'START': start,
    #         }, raw=True) 
    #     deals = deals + dealsStart['result']
    pprint(deals)
    # print(f'{len(dealsTrue)=}')
    return deals

def get_deal(id):
    deal = bit.get_all('crm.deal.get', 
        params = {
            'id': id})
    pprint(deal)
    return deal

def get_phone_is_deal(id):
    deal = get_deal(id)
    phone = deal['PHONE'][0]['VALUE']
    return phone

def get_contact_is_deal(id):
    deal = get_deal(id)
    contact = deal['CONTACT_ID']
    return contact

def create_deal(dealID):
    contactID = get_contact_is_deal(dealID)
    fields = {'fields': {'TITLE':f'Жалоба на {dealID}' ,'CATEGORY_ID': Crm.categotyIDRobot, 'CONTACT_ID': contactID,}}
    #deal = bit.call('crm.deal.add', fields)
    #print('создана сделка', deal)
    print('создана сделка', fields)
