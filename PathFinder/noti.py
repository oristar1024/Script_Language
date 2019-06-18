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

key = 'RYbKTedumwvcnqN7rvckfb0RqAYkfMpedWrsxmfXHs2PLuK5g7pk%2Bh7PM3nhn5hh%2FUbUjvs2gAgIWepm%2FjeVDQ%3D%3D'
TOKEN = '880368039:AAFZZBMmsrKZZqQxCkJYjHm4Cz1JfaPVts0'
MAX_MSG_LENGTH = 300
baseurl = 'http://ws.bus.go.kr/api/rest/pathinfo/getLocationInfo?serviceKey='+key
bot = telepot.Bot(TOKEN)

class Path:
    def __init__(self):
        self.list = []
        self.time = None

    def render(self):
        renderedList = []
        for path in self.list:
            renderedList.append(path)
        renderedList.append("소요시간 약 "+ str(self.time) + "분")
        return renderedList

class SinglePath:
    def __init__(self):
        self.start = None
        self.by = None
        self.end = None

    def render(self):
        return str(self.start) + "에서 " + str(self.by) + "타고 " + str(self.end) + "로 이동"

def BusData(key1,key2):
    import urllib
    import http.client
    depInfo = []
    destInfo = []
    itemList = []
    for i in range(2):
        if i == 0:
            hangul_utf8 = urllib.parse.quote(key1)
        else:
            hangul_utf8 = urllib.parse.quote(key2)
        url = "http://ws.bus.go.kr/api/rest/pathinfo/getLocationInfo?serviceKey=RYbKTedumwvcnqN7rvckfb0RqAYkfMpedWrsxmfXHs2PLuK5g7pk%2Bh7PM3nhn5hh%2FUbUjvs2gAgIWepm%2FjeVDQ%3D%3D&stSrch=" + hangul_utf8

        res_body = urlopen(url).read().decode('utf-8')
        # print(res_body)
        soup = BeautifulSoup(res_body, 'html.parser')

        # print(soup)
        msgBody = soup.find('msgbody')

        for items in msgBody:
            items = re.sub('<.*?>', '|', str(items))
            parsed = items.split('||')
            # print(parsed)
            if parsed[4] == key1:
                depInfo.append(parsed[4])
                depInfo.append(parsed[1])
                depInfo.append(parsed[2])

            if parsed[4] == key2:
                destInfo.append(parsed[4])
                destInfo.append(parsed[1])
                destInfo.append(parsed[2])

    #print(depInfo)
    #print(destInfo)

    StartX = depInfo[1]
    StartY = depInfo[2]
    endX = destInfo[1]
    endY = destInfo[2]

    busUrl = "http://ws.bus.go.kr/api/rest/pathinfo/getPathInfoByBus?ServiceKey="
    ServiceKey = "N8USDHDG7JwSXDABxAAGBfrlp8wB6sYQDVQX8eEDTJeBpAce21z18uAhHFSTh%2BromrgASad0VNzaJ1YBkZi5IQ%3D%3D"
    option = "&startX=" + str(StartX) + "&startY=" + str(StartY) + "&endX=" + str(endX) + "&endY=" + str(endY)

    addUrl = busUrl + ServiceKey + option
    #print(addUrl)
    res_body = urlopen(addUrl).read().decode('utf-8')
    soup = BeautifulSoup(res_body, 'html.parser')
    msgBody = soup.find('msgbody')
    #print(msgBody)
    for items in msgBody:
        items = re.sub('<.*?>', '/', str(items))
        items = re.sub('///', '//', str(items))
        parsed = items.split('//')
        #print(parsed)
        itemList.append(parsed[3])
        itemList.append(parsed[7])
        itemList.append(parsed[9])

        if parsed[13] != '':
            itemList.append(parsed[13])
            itemList.append(parsed[17])
            itemList.append(parsed[19])
            itemList.append(parsed[22])
            itemList.append('')
        else:
            itemList.append(parsed[12])
            itemList.append('')
        break
    return itemList

def SubData(key1,key2):
    import urllib
    import http.client
    depInfo = []
    destInfo = []
    itemList = []
    for i in range(2):
        if i == 0:
            hangul_utf8 = urllib.parse.quote(key1)
        else:
            hangul_utf8 = urllib.parse.quote(key2)
        url = "http://ws.bus.go.kr/api/rest/pathinfo/getLocationInfo?serviceKey=RYbKTedumwvcnqN7rvckfb0RqAYkfMpedWrsxmfXHs2PLuK5g7pk%2Bh7PM3nhn5hh%2FUbUjvs2gAgIWepm%2FjeVDQ%3D%3D&stSrch=" + hangul_utf8

        res_body = urlopen(url).read().decode('utf-8')
        # print(res_body)
        soup = BeautifulSoup(res_body, 'html.parser')

        # print(soup)
        msgBody = soup.find('msgbody')

        for items in msgBody:
            items = re.sub('<.*?>', '|', str(items))
            parsed = items.split('||')

            # print(parsed)
            if parsed[4] == key1:
                depInfo.append(parsed[4])
                depInfo.append(parsed[1])
                depInfo.append(parsed[2])

            if parsed[4] == key2:
                destInfo.append(parsed[4])
                destInfo.append(parsed[1])
                destInfo.append(parsed[2])

    # print(depInfo)
    # print(destInfo)

    StartX = depInfo[1]
    StartY = depInfo[2]
    endX = destInfo[1]
    endY = destInfo[2]

    subUrl = "http://ws.bus.go.kr/api/rest/pathinfo/getPathInfoBySubway?ServiceKey="
    ServiceKey = "N8USDHDG7JwSXDABxAAGBfrlp8wB6sYQDVQX8eEDTJeBpAce21z18uAhHFSTh%2BromrgASad0VNzaJ1YBkZi5IQ%3D%3D"
    option = "&startX=" + str(StartX) + "&startY=" + str(StartY) + "&endX=" + str(endX) + "&endY=" + str(endY)

    addUrl = subUrl + ServiceKey + option
    #print(addUrl)
    res_body = urlopen(addUrl).read().decode('utf-8')
    soup = BeautifulSoup(res_body, 'html.parser')
    msgBody = soup.find('msgbody')
    #print(msgBody)
    msgBody = re.sub('<routeNm>','/rn//',str(msgBody))
    msgBody = re.sub('<fname>','/st//',str(msgBody))
    msgBody = re.sub('<tname>','/end//',str(msgBody))
    msgBody = re.sub('<time>','/time//',str(msgBody))
    msgBody = re.sub('<.*?>', '/', str(msgBody))
    msgBody = re.sub('///', '//', str(msgBody))
    parsed = msgBody.split('//')

    for i in range(len(parsed)):
        if parsed[i] == 'st':
            itemList.append(parsed[i+1])
        elif parsed[i] == 'end':
            itemList.append(parsed[i-2])
            itemList.append(parsed[i+1])
        elif parsed[i] == 'time':
            itemList.append(parsed[i+1])

    itemList.append('')
    return itemList

def MixData(key1,key2):
    import urllib
    import http.client
    depInfo = []
    destInfo = []
    itemList = []
    for i in range(2):
        if i == 0:
            hangul_utf8 = urllib.parse.quote(key1)
        else:
            hangul_utf8 = urllib.parse.quote(key2)
        url = "http://ws.bus.go.kr/api/rest/pathinfo/getLocationInfo?serviceKey=RYbKTedumwvcnqN7rvckfb0RqAYkfMpedWrsxmfXHs2PLuK5g7pk%2Bh7PM3nhn5hh%2FUbUjvs2gAgIWepm%2FjeVDQ%3D%3D&stSrch=" + hangul_utf8

        res_body = urlopen(url).read().decode('utf-8')
        # print(res_body)
        soup = BeautifulSoup(res_body, 'html.parser')

        # print(soup)
        msgBody = soup.find('msgbody')

        for items in msgBody:
            items = re.sub('<.*?>', '|', str(items))
            parsed = items.split('||')

            # print(parsed)
            if parsed[4] == key1:
                depInfo.append(parsed[4])
                depInfo.append(parsed[1])
                depInfo.append(parsed[2])

            if parsed[4] == key2:
                destInfo.append(parsed[4])
                destInfo.append(parsed[1])
                destInfo.append(parsed[2])

    # print(depInfo)
    # print(destInfo)

    StartX = depInfo[1]
    StartY = depInfo[2]
    endX = destInfo[1]
    endY = destInfo[2]

    subUrl = "http://ws.bus.go.kr/api/rest/pathinfo/getPathInfoByBusNSub?ServiceKey="
    ServiceKey = "N8USDHDG7JwSXDABxAAGBfrlp8wB6sYQDVQX8eEDTJeBpAce21z18uAhHFSTh%2BromrgASad0VNzaJ1YBkZi5IQ%3D%3D"
    option = "&startX=" + str(StartX) + "&startY=" + str(StartY) + "&endX=" + str(endX) + "&endY=" + str(endY)

    addUrl = subUrl + ServiceKey + option
    #print(addUrl)
    res_body = urlopen(addUrl).read().decode('utf-8')
    soup = BeautifulSoup(res_body, 'html.parser')
    msgBody = soup.find('msgbody')
    #print(msgBody)
    msgBody = re.sub('<routeNm>','/rn//',str(msgBody))
    msgBody = re.sub('<fname>','/st//',str(msgBody))
    msgBody = re.sub('<tname>','/end//',str(msgBody))
    msgBody = re.sub('<time>','/time//',str(msgBody))
    msgBody = re.sub('<.*?>', '/', str(msgBody))
    msgBody = re.sub('///', '//', str(msgBody))
    parsed = msgBody.split('//')

    for i in range(len(parsed)):
        if parsed[i] == 'st':
            itemList.append(parsed[i+1])
        elif parsed[i] == 'end':
            itemList.append(parsed[i-2])
            itemList.append(parsed[i+1])
        elif parsed[i] == 'time':
            itemList.append(parsed[i+1])
            break;

    itemList.append('')
    return itemList

def SearchData(key):
    import urllib
    import http.client
    res_list = []

    hangul_utf8 = urllib.parse.quote(key)
    url = baseurl+'&stSrch='+hangul_utf8
    #print(url)
    res_body = urlopen(url).read().decode('utf-8')
    #print(res_body)
    #print(res_body)
    soup = BeautifulSoup(res_body, 'html.parser')

    msgBody = soup.find('msgbody')

    for itemList in msgBody:
        #print(itemList)
        #print(itemList.text)
        itemList = re.sub('<.*?>', '|', str(itemList))
        #print(itemList)
        parsed = itemList.split('||')
       # print(parsed)
        try:
            row = parsed[4]
            #print(row)
        except IndexError:
            row = itemList.replace('|', ',')

        if row:
            res_list.append(row)
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):

    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = SearchData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
