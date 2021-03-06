#import tkinter
from tkinter import *
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
        self.Graph = 0
        self.listbox = 1
        rb4 = Radiobutton(self.p2frame3, variable=self.choose, text='그래프보기', value=4, bg=self.bgColor, command=self.select)
        rb4.pack(side=LEFT)
        rb1 = Radiobutton(self.p2frame3,variable=self.choose, text='버스', value=1, bg = 'red', command = self.select)
        rb1.pack(side=LEFT)
        rb2 = Radiobutton(self.p2frame3,variable=self.choose, text='지하철', value=2, bg = 'blue', command = self.select)
        rb2.pack(side=LEFT)
        rb3 = Radiobutton(self.p2frame3,variable=self.choose, text='버스+지하철', value=3, bg = 'green', command = self.select)
        rb3.pack(side=LEFT)


        self.p2frame4 = Frame(self.canvas)
        self.p2frame4.pack()

        self.scrollbar = Scrollbar(self.p2frame4)
        self.scrollbar.pack(side=RIGHT, fill='y')
        self.FindedPath = Listbox(self.p2frame4, width=92, height=20, yscrollcommand=self.scrollbar.set)
        self.FindedPath.pack()

        # 메일 추가부분
        self.MailEntry = Entry(self.p2frame4)
        self.MailButton = Button(self.p2frame4, text="메일전송", command=self.sendMail)
        self.MailButton.pack(side=RIGHT)
        self.MailEntry.pack(side=RIGHT)
        Label(self.p2frame4, text="받을메일주소 : ").pack(side=RIGHT)

    def getPath(self, requestUrl, lst):
        StartX = self.depart.x
        StartY = self.depart.y
        endX = self.dest.x
        endY = self.dest.y

        ServiceKey = "N8USDHDG7JwSXDABxAAGBfrlp8wB6sYQDVQX8eEDTJeBpAce21z18uAhHFSTh%2BromrgASad0VNzaJ1YBkZi5IQ%3D%3D"
        option = "&startX=" + str(StartX) + "&startY=" + str(StartY) + "&endX=" + str(endX) + "&endY=" + str(endY)

        import http.client
        from xml.dom.minidom import parseString

        conn = http.client.HTTPConnection("ws.bus.go.kr")
        conn.request("GET", requestUrl + ServiceKey + option)
        req = conn.getresponse()

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
                        tmppath = Path()
                        for subitem in subitems:
                            if subitem.nodeName == 'pathList':
                                pathes = subitem.childNodes
                                tmpSinglePath = SinglePath()
                                for path in pathes:
                                    if path.nodeName == 'fname':
                                        tmpSinglePath.start = path.firstChild.nodeValue
                                    elif path.nodeName == 'routeNm':
                                        tmpSinglePath.by = path.firstChild.nodeValue
                                    elif path.nodeName == 'tname':
                                        tmpSinglePath.end = path.firstChild.nodeValue
                                tmppath.list.append(tmpSinglePath.render())
                            elif subitem.nodeName == 'time':
                                tmppath.time = subitem.firstChild.nodeValue
                                lst.append(tmppath)

    def FindPath(self):
        self.subPathList = []
        self.busPathList = []
        self.busNsubPathList = []

        subUrl = "/api/rest/pathinfo/getPathInfoBySubway?ServiceKey="
        busUrl = "/api/rest/pathinfo/getPathInfoByBus?ServiceKey="
        busNsubUrl = "/api/rest/pathinfo/getPathInfoByBusNSub?ServiceKey="

        self.getPath(subUrl, self.subPathList)
        self.getPath(busUrl, self.busPathList)
        self.getPath(busNsubUrl, self.busNsubPathList)

    def select(self):
        if self.choose.get() == 1:
            if self.Graph == 1:
                self.graph.destroy()
                self.Graph = 0
            if self.listbox == 0:
                self.scrollbar = Scrollbar(self.p2frame4)
                self.scrollbar.pack(side=RIGHT, fill='y')
                self.FindedPath = Listbox(self.p2frame4, width=92, height=20, yscrollcommand=self.scrollbar.set)
                self.FindedPath.pack()
                self.listbox = 1
            self.printPathList(self.busPathList)
        elif self.choose.get() == 2:
            if self.Graph == 1:
                self.graph.destroy()
                self.Graph = 0
            if self.listbox == 0:
                self.scrollbar = Scrollbar(self.p2frame4)
                self.scrollbar.pack(side=RIGHT, fill='y')
                self.FindedPath = Listbox(self.p2frame4, width=92, height=20, yscrollcommand=self.scrollbar.set)
                self.FindedPath.pack()
                self.listbox = 1
            self.printPathList(self.subPathList)
        elif self.choose.get() == 3:
            if self.Graph == 1:
                self.graph.destroy()
                self.Graph = 0
            if self.listbox == 0:
                self.scrollbar = Scrollbar(self.p2frame4)
                self.scrollbar.pack(side=RIGHT, fill='y')
                self.FindedPath = Listbox(self.p2frame4, width=92, height=20, yscrollcommand=self.scrollbar.set)
                self.FindedPath.pack()
                self.listbox = 1
            self.printPathList(self.busNsubPathList)
        elif self.choose.get() == 4:
            if self.listbox == 1:
                self.FindedPath.destroy()
                self.scrollbar.destroy()
            if self.Graph != 1:
                self.printGraph()
                self.listbox = 0
                self.Graph = 1

    def printGraph(self):
        GraphInfo = []
        for info in self.busPathList:
            tempInfo = []
            tempInfo.append('bus')
            tempInfo.append(info.time)
            GraphInfo.append(tempInfo)
        for info in self.subPathList:
            tempInfo = []
            tempInfo.append('sub')
            tempInfo.append(info.time)
            GraphInfo.append(tempInfo)
        for info in self.busNsubPathList:
            tempInfo = []
            tempInfo.append('busNsub')
            tempInfo.append(info.time)
            GraphInfo.append(tempInfo)

        for i in range(len(GraphInfo)-1):
            for j in range(len(GraphInfo)-1-i):
                if GraphInfo[j][1] > GraphInfo[j+1][1]:
                    temp = GraphInfo[j+1]
                    GraphInfo[j+1] = GraphInfo[j]
                    GraphInfo[j] = temp

        #print(GraphInfo)
        histogram = [0]*len(GraphInfo)
        for i in range(len(GraphInfo)):
            histogram[i] = GraphInfo[i][1]

        maxCount = GraphInfo[len(GraphInfo)-1][1]
        #print(len(GraphInfo))
        self.graph = Canvas(self.p2frame4, bg = self.bgColor,width=661, height=320)
        self.graph.pack()
        width = 661
        height = 320
        self.graph.create_line(20, height - 10, 640, height - 10, tags="line")
        barW = (width - 5) / 26
        for i in range(len(GraphInfo)):
            if i > 23:
                break
            tmpColor = 'white'

            if GraphInfo[i][0] == 'bus':
                tmpColor = 'red'
            elif GraphInfo[i][0] == 'sub':
                tmpColor = 'blue'
            else:
                tmpColor = 'green'
            self.graph.create_rectangle(i * barW + 30 , height - (height - 20) * int(histogram[i]) / int(maxCount),
                                         (i + 1) * barW + 15, height - 10, tags="grim", fill = tmpColor)





    def printPathList(self, lst):
        self.FindedPath.delete(0, END)
        self.indexList = []
        self.lineList = []  # 메일추가부분
        self.idx = 0
        temp = 0
        for path in lst:
            tmpSK = SK(str(self.idx), temp, None)
            self.idx += 1
            for line in path.list:
                self.FindedPath.insert(temp, line)
                self.lineList.append(line)
                temp += 1
            self.FindedPath.insert(temp, "소요시간 약 " + str(path.time) + "분")
            self.lineList.append("소요시간 약 " + str(path.time) + "분")
            temp += 1
            tmpSK.y = temp
            self.indexList.append(tmpSK)
        self.FindedPath.bind('<<ListboxSelect>>', self.bindListbox)

    def bindListbox(self, event=None):
        selection = self.FindedPath.curselection()[0]
        for idx in self.indexList:
            if selection >= idx.x and selection < idx.y:
                self.FindedPath.selection_set(idx.x, idx.y - 1)

    def sendMail(self):
        import mimetypes
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        self.host = "smtp.gmail.com"
        self.port = "587"
        self.htmlFileName = "logo.html"
        self.senderAddr = "tronia94@gmail.com"
        self.recipientAddr = self.MailEntry.get()

        msg = MIMEMultipart("alternative")
        msg['subject'] = "Finded Path"
        msg['From'] = self.senderAddr
        msg["To"] = self.recipientAddr


        selection = self.FindedPath.curselection()
        self.msgPart = []
        for i in selection:
            msgtext = self.lineList[i] + "<br>"
            self.msgPart.append(MIMEText(msgtext, 'plane'))

        for part in self.msgPart:
            msg.attach(part)

        s = smtplib.SMTP(self.host, self.port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("tronia94", "dlstj5720")
        s.sendmail(self.senderAddr, [self.recipientAddr], msg.as_string())
        s.close()


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
