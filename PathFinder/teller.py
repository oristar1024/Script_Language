#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import noti

def repSearch(user, key):
    #print(user, key)
    res_list = noti.SearchData( key )
    #print(res_list)
    msg = ''
    for r in res_list:
        #print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, key + '를 찾지 못했습니다.' )

def repBus(user, key1, key2):

    rep_list = noti.BusData(key1,key2)
    #print(rep_list)
    msg = ''
    msg += '탑승장소 : ' + rep_list[0] + '\n탑승정보 : ' + rep_list[1] + "\n하차장소 : " + rep_list[2]
    if rep_list[4] != '':
        msg += "\n환승장소 : " + rep_list[3] + '\n탑승정보 : ' + rep_list[4] + "\n하차장소 : " + rep_list[5] + "\n소요시간 : " + rep_list[6] + "분"
    else:
        msg += "\n소요시간 : " + rep_list[3] + "분"

    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, key1 + '또는' + key2 + '를 찾지 못했습니다.')


def repSub(user,key1, key2):

    rep_list = noti.SubData(key1,key2)
    #print(rep_list)
    msg = ''
    msg += '탑승장소 : ' + rep_list[0] + '\n탑승정보 : ' + rep_list[1] + "\n하차장소 : " + rep_list[2]
    if rep_list[4] != '':
        msg += "\n환승장소 : " + rep_list[3] + '\n탑승정보 : ' + rep_list[4] + "\n하차장소 : " + rep_list[5] + "\n소요시간 : " + rep_list[
            6] + "분"
    else:
        msg += "\n소요시간 : " + rep_list[3] + "분"

    if msg:
        noti.sendMessage(user, msg)
    else:
        noti.sendMessage(user, key1 + '또는' + key2 + '를 찾지 못했습니다.')
    pass

def repMix(user,key1,key2):
    rep_list = noti.MixData(key1,key2)
    #print(rep_list)
    msg = ''
    msg += '탑승장소 : ' + rep_list[0] + '\n탑승정보 : ' + rep_list[1] + "\n하차장소 : " + rep_list[2]
    if rep_list[4] != '':
        msg += "\n환승장소 : " + rep_list[3] + '\n탑승정보 : ' + rep_list[4] + "\n하차장소 : " + rep_list[5] + "\n소요시간 : " + \
               rep_list[
                   6] + "분"
    else:
        msg += "\n소요시간 : " + rep_list[3] + "분"

    if msg:
        noti.sendMessage(user, msg)
    else:
        noti.sendMessage(user, key1 + '또는' + key2 + '를 찾지 못했습니다.')
    pass
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('검색') and len(args)>1:
        repSearch(chat_id, args[1] )
    elif text.startswith('버스최단')  and len(args)>1:
        repBus(chat_id, args[1], args[2])
    elif text.startswith('지하철최단'):
        repSub(chat_id,args[1],args[2])
    elif text.startswith('환승최단'):
        repMix(chat_id,args[1],args[2])
        pass
    else:
        noti.sendMessage(chat_id, '모르는 명령어입니다.\n검색 [검색어]\n버스최단 [출발지] [목적지]\n지하철최단 [출발지] [목적지]\n환승최단 [출발지] [목적지]\n중 하나의 명령을 입력하세요.')


today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )

bot = telepot.Bot(noti.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)