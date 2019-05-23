#import tkinter
from tkinter import *
class SK:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

#insert(SK(name, x, y))

class PathFinder:
    #키관련 검색
    def getPlace(self,key):
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
                print(itemlist)
                temp = 1
                for item in itemlist:
                    if item.nodeName == "itemList":
                        subitems = item.childNodes
                        self.searchList.append(SK(subitems[3].firstChild.nodeValue, subitems[0].firstChild.nodeValue,
                                                  subitems[1].firstChild.nodeValue))
                        self.keyList.insert(temp, self.searchList[temp-1].name)
                        print(self.searchList[temp-1].x,self.searchList[temp-1].y)
                        temp += 1



    def search(self):
        searchKey = self.dep.get()
        self.keyList.delete(0,END)
        self.getPlace(searchKey)
        pass
    def enterPage1(self):
        self.mainframe.destroy()
        self.Page1()
    def enterPage2(self):
        self.p1frame1.destroy()
        self.p1frame2.destroy()
        self.p1frame3.destroy()
        self.Page2()
    def MainPage(self):
        self.canvas = Canvas(self.window, bg = self.bgColor,width = 657, height = 443)
        self.canvas.pack()
        self.mainframe = Frame(self.canvas)
        self.mainframe.pack()
        self.mainB = Button(self.mainframe,image = self.imageList[0],width = 657, height = 443, bg = self.bgColor, command = self.enterPage1)
        self.mainB.pack(side = LEFT)

    def Page1(self):
        self.p1frame1 = Frame(self.canvas)
        self.p1frame1.pack()
        title = Label(self.p1frame1, image=self.imageList[0]).pack()

        self.p1frame2 = Frame(self.canvas, bg = self.bgColor)
        self.p1frame2.pack(side=LEFT)

        F_dep = Frame(self.p1frame2, bg=self.bgColor)
        F_dep.pack()
        Label(F_dep, text="출발지", bg=self.bgColor).pack(side=LEFT)
        self.dep = Entry(F_dep)
        self.dep.pack(side=LEFT)
        Button(F_dep, text="검색",command = self.search).pack(side=LEFT)

        F_dest = Frame(self.p1frame2, bg=self.bgColor)
        F_dest.pack()
        Label(F_dest, text="도착지", bg=self.bgColor).pack(side=LEFT)
        self.dest = Entry(F_dest)
        self.dest.pack(side=LEFT)
        Button(F_dest, text="검색").pack(side=LEFT)

        F_list = Frame(self.p1frame2, bg=self.bgColor)
        F_list.pack()
        Label(F_list, text="검색목록", bg=self.bgColor).pack()

        scrollbar = Scrollbar(F_list)
        scrollbar.pack(side=RIGHT, fill='y')

        # text를 검색정보로 변경해야함 .. 사이즈 확인용 text

        self.keyList = Listbox(F_list, width=40, height=19,yscrollcommand=scrollbar.set)
        self.keyList.pack()

        Label(F_list, text="선택지역 : ", bg=self.bgColor).pack(side=LEFT)
#        self.searchList = self.searchList.curselection()[0]
#        selected = ""
#        for n in range(0,self.searchList.length):
#            if self.searchList == n:
#                selected = self.searchList[n]
        Label(F_list, text="", bg=self.bgColor).pack(side=LEFT)

        Label(F_list, bg=self.bgColor).pack(side=LEFT)
        choose = Button(F_list, text="결정").pack(side=RIGHT)

        self.p1frame3 = Frame(self.canvas, bg=self.bgColor)
        self.p1frame3.pack(side=RIGHT)

        Label(self.p1frame3, text="주변지도", bg=self.bgColor).pack()
        map = Label(self.p1frame3, image=self.imageList[1]).pack()
        search = Button(self.p1frame3, text="검색", command = self.enterPage2)
        search.pack()

    def Page2(self):
        pass

    def __init__(self):
        self.window = Tk()
        self.window.title("PathFinder")
        self.imageList = []
        self.imageList.append(PhotoImage(file="title.gif"))
        self.imageList.append(PhotoImage(file="map.gif"))
        self.bgColor = 'white'
        self.MainPage()
        self.searchList = []
        self.window.mainloop()

PathFinder()