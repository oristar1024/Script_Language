#import tkinter
from tkinter import *

class SK:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

class PathFinder:
    #키관련 검색
    def getPlace(self,key):
        self.searchList = []
        self.keyList.delete(0)
        self.map.configure(image = self.imageList[1])


        import urllib
        import http.client
        hangul_utf8 = urllib.parse.quote(key)
        from xml.dom.minidom import parse, parseString
        conn = http.client.HTTPConnection("ws.bus.go.kr")
        conn.request("GET","/api/rest/pathinfo/getLocationInfo?serviceKey=RYbKTedumwvcnqN7rvckfb0RqAYkfMpedWrsxmfXHs2PLuK5g7pk%2Bh7PM3nhn5hh%2FUbUjvs2gAgIWepm%2FjeVDQ%3D%3D&stSrch=" + hangul_utf8)
        req = conn.getresponse()

        if req.status == 200:
            xmldoc = req.read().decode('utf-8)')
            if xmldoc == None:
                #팝업창으로 없는주소라고 쓴다
                pass
            else:
                parseData = parseString(xmldoc)
                ServiceResult = parseData.childNodes
                msgBody = ServiceResult[0].childNodes
                itemlist = msgBody[2].childNodes
                temp = 1
                for item in itemlist:
                    if item.nodeName == "itemList":
                        subitems = item.childNodes
                        self.searchList.append(SK(subitems[3].firstChild.nodeValue, subitems[0].firstChild.nodeValue,
                                                  subitems[1].firstChild.nodeValue))
                        self.keyList.insert(temp, self.searchList[temp-1].name)
                        temp += 1

    def drawmap(self):
        idx = self.keyList.curselection()[0]
        sk = self.searchList[idx]
        from urllib.request import urlopen
        from io import BytesIO
        from PIL import Image, ImageTk
        url = "https://maps.googleapis.com/maps/api/staticmap?center=" + str(sk.y) + "," + str(sk.x) + \
              "&zoom=15&markers=color:red|color:red|lavel:C|" +str(sk.y) + "," + str(sk.x) +\
              "&size=359x291&format=jpg&key=AIzaSyCWJAM-nuDT2BaF08b6VR9dQXn3um7puaA"
        with urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(im)
        self.map.configure(image = image)
        self.map.image = image

    def search(self):
        searchKey = self.keyword.get()
        self.keyList.delete(0,END)
        self.getPlace(searchKey)

    def enterPage1(self):
        self.mainframe.destroy()
        self.Page1()

    def enterPage2(self):
        if self.depart and self.dest:
            self.p1frame1.destroy()
            self.p1frame2.destroy()
            self.p1frame3.destroy()
            self.Page2()
        else:
            pass

    def goPage2(self):
        self.p2frame1.destroy()
        self.p2frame2.destroy()
        self.p2frame3.destroy()
        self.p2frame4.destroy()
        self.Page1()
    def MainPage(self):
        self.canvas = Canvas(self.window, bg = self.bgColor,width = 657, height = 443)
        self.canvas.pack()
        self.mainframe = Frame(self.canvas)
        self.mainframe.pack()
        self.mainB = Button(self.mainframe,image = self.imageList[0],width = 657, height = 443, bg = self.bgColor, command = self.enterPage1)
        self.mainB.pack(side = LEFT)

    def desButton(self):
        iSearchIndex = self.keyList.curselection()[0]
        self.des.configure(text=str(self.searchList[iSearchIndex].name))
        self.dest = self.searchList[iSearchIndex]

    def depButton(self):
        iSearchIndex = self.keyList.curselection()[0]
        self.dep.configure(text=str(self.searchList[iSearchIndex].name))
        self.depart = self.searchList[iSearchIndex]

    def Page1(self):
        self.p1frame1 = Frame(self.canvas, bg=self.bgColor)
        self.p1frame1.pack()
        title = Label(self.p1frame1, image=self.imageList[0]).pack()

        self.p1frame2 = Frame(self.canvas, bg = self.bgColor)
        self.p1frame2.pack(side=LEFT)

        F_dep = Frame(self.p1frame2, bg=self.bgColor)
        F_dep.pack()
        Label(F_dep, text="검색어", bg=self.bgColor).pack(side=LEFT)
        self.keyword = Entry(F_dep)
        self.keyword.pack(side=LEFT)
        Button(F_dep, text="검색",command = self.search).pack(side=LEFT)

        F_list = Frame(self.p1frame2, bg=self.bgColor)
        F_list.pack()
        Label(F_list, text="검색목록", bg=self.bgColor).pack()

        scrollbar = Scrollbar(F_list)
        scrollbar.pack(side=RIGHT, fill='y')

        # text를 검색정보로 변경해야함 .. 사이즈 확인용 text

        self.keyList = Listbox(F_list, width=40, height=19,yscrollcommand=scrollbar.set)
        self.keyList.pack()
        choose = Button(F_list, text="도착지",command = self.desButton).pack(side=RIGHT)
        choose = Button(F_list, text="출발지",command = self.depButton).pack(side=RIGHT)

        choose = Button(F_list, text="지도보기", command = self.drawmap).pack(side=LEFT)

        self.p1frame3 = Frame(self.canvas, bg=self.bgColor)
        self.p1frame3.pack(side=RIGHT)

        Label(self.p1frame3, text="주변지도", bg=self.bgColor).pack()

        self.map = Label(self.p1frame3, image = self.imageList[1])
        self.map.pack()

        search = Button(self.p1frame3, text="검색", command = self.enterPage2)
        search.pack(side = RIGHT)

        self.des = Label(self.p1frame3, text="도착", bg=self.bgColor)
        self.des.pack(side=RIGHT)
        Label(self.p1frame3, text="->", bg=self.bgColor).pack(side=RIGHT)
        self.dep = Label(self.p1frame3, text="출발", bg=self.bgColor)
        self.dep.pack(side=RIGHT)

    def Page2(self):
        self.FindPath()
        self.p2frame1 = Frame(self.canvas, bg=self.bgColor)
        self.p2frame1.pack()
        title = Label(self.p2frame1, image=self.imageList[0]).pack()

        self.p2frame2 = Frame(self.canvas, bg=self.bgColor)
        self.p2frame2.pack()

        self.dep = Label(self.p2frame2, text=str(self.depart.name), bg=self.bgColor)
        self.dep.pack(side=LEFT)
        Label(self.p2frame2, text="->", bg=self.bgColor).pack(side = LEFT)
        self.des = Label(self.p2frame2, text=str(self.dest.name), bg=self.bgColor)
        self.des.pack(side = LEFT)
        self.goP2 = Button(self.p2frame2, text="경로재설정", command = self.goPage2,bg = self.bgColor).pack(side = LEFT)

        self.p2frame3 = Frame(self.canvas)
        self.p2frame3.pack()
        self.choose = IntVar()
        rb1 = Radiobutton(self.p2frame3,variable=self.choose, text='버스', value=1, bg = self.bgColor)
        rb1.pack(side=LEFT)
        rb2 = Radiobutton(self.p2frame3,variable=self.choose, text='지하철', value=2, bg = self.bgColor)
        rb2.pack(side=LEFT)
        rb3 = Radiobutton(self.p2frame3,variable=self.choose, text='버스+지하철', value=3, bg = self.bgColor)
        rb3.pack(side=LEFT)

        self.p2frame4 = Frame(self.canvas)
        self.p2frame4.pack()
        scrollbar = Scrollbar(self.p2frame4)
        scrollbar.pack(side=RIGHT, fill='y')
        self.FindedPath = Listbox(self.p2frame4, width=92, height=20, yscrollcommand=scrollbar.set)
        self.FindedPath.pack()

    def FindPath(self):
        StartX = self.depart.x
        StartY = self.depart.y
        endX = self.dest.x
        endY = self.dest.y

        ServiceKey = "N8USDHDG7JwSXDABxAAGBfrlp8wB6sYQDVQX8eEDTJeBpAce21z18uAhHFSTh%2BromrgASad0VNzaJ1YBkZi5IQ%3D%3D"
        option = "&startX=" + str(StartX)+"&startY=" +str(StartY) +"&endX=" + str(endX) + "&endY=" + str(endY)
        import http.client
        from xml.dom.minidom import parseString

        # 지하철 경로탐색
        conn = http.client.HTTPConnection("ws.bus.go.kr")
        conn.request("GET","/api/rest/pathinfo/getPathInfoBySubway?ServiceKey=" + ServiceKey + option)
        req = conn.getresponse()
        print("지하철경로")
        print()
        if req.status == 200:
            xmldoc = req.read().decode('utf-8)')
            if xmldoc == None:
                pass
            else:
                parseData = parseString(xmldoc)
                ServiceResult = parseData.childNodes
                msgBody = ServiceResult[0].childNodes
                itemlist = msgBody[2].childNodes
                for item in itemlist:
                    if item.nodeName == "itemList":
                        subitems = item.childNodes
                        for subitem in subitems:
                            if subitem.nodeName == 'pathList':
                                pathes = subitem.childNodes
                                for path in pathes:
                                    if path.nodeName == 'fname':
                                        print(path.firstChild.nodeValue, "에서")
                                    elif path.nodeName == 'routeNm':
                                        print(path.firstChild.nodeValue, "타고")
                                    elif path.nodeName == 'tname':
                                        print(path.firstChild.nodeValue, "으로이동")
                            elif subitem.nodeName == 'time':
                                print("소요시간 약", subitem.firstChild.nodeValue, "분")
                                print()

        # 버스 경로탐색
        conn = http.client.HTTPConnection("ws.bus.go.kr")
        conn.request("GET", "/api/rest/pathinfo/getPathInfoByBus?ServiceKey=" + ServiceKey + option)
        req = conn.getresponse()
        print("버스경로")
        print()
        if req.status == 200:
            xmldoc = req.read().decode('utf-8)')
            if xmldoc == None:
                pass
            else:
                parseData = parseString(xmldoc)
                ServiceResult = parseData.childNodes
                msgBody = ServiceResult[0].childNodes
                itemlist = msgBody[2].childNodes
                for item in itemlist:
                    if item.nodeName == "itemList":
                        subitems = item.childNodes
                        for subitem in subitems:
                            if subitem.nodeName == 'pathList':
                                pathes = subitem.childNodes
                                for path in pathes:
                                    if path.nodeName == 'fname':
                                        print(path.firstChild.nodeValue, "에서")
                                    elif path.nodeName == 'routeNm':
                                        print(path.firstChild.nodeValue, "타고")
                                    elif path.nodeName == 'tname':
                                        print(path.firstChild.nodeValue, "으로이동")
                            elif subitem.nodeName == 'time':
                                print("소요시간 약", subitem.firstChild.nodeValue, "분")
                                print()

        # 버스 + 지하철 경로탐색
        conn = http.client.HTTPConnection("ws.bus.go.kr")
        conn.request("GET", "/api/rest/pathinfo/getPathInfoByBusNSub?ServiceKey=" + ServiceKey + option)
        req = conn.getresponse()
        print("버스+지하철 경로")
        print()
        if req.status == 200:
            xmldoc = req.read().decode('utf-8)')
            if xmldoc == None:
                pass
            else:
                parseData = parseString(xmldoc)
                ServiceResult = parseData.childNodes
                msgBody = ServiceResult[0].childNodes
                itemlist = msgBody[2].childNodes
                for item in itemlist:
                    if item.nodeName == "itemList":
                        subitems = item.childNodes
                        for subitem in subitems:
                            if subitem.nodeName == 'pathList':
                                pathes = subitem.childNodes
                                for path in pathes:
                                    if path.nodeName == 'fname':
                                        print(path.firstChild.nodeValue, "에서")
                                    elif path.nodeName == 'routeNm':
                                        print(path.firstChild.nodeValue, "타고")
                                    elif path.nodeName == 'tname':
                                        print(path.firstChild.nodeValue, "으로이동")
                            elif subitem.nodeName == 'time':
                                print("소요시간 약", subitem.firstChild.nodeValue, "분")
                                print()

    def __init__(self):
        self.window = Tk()
        self.window.title("PathFinder")
        self.imageList = []
        self.imageList.append(PhotoImage(file="title.gif"))
        self.imageList.append(PhotoImage(file="map.gif"))
        self.bgColor = 'white'
        self.MainPage()
        self.searchList = []
        self.depart = None
        self.dest = None
        self.window.mainloop()

PathFinder()
