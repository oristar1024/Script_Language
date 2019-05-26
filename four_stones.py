from tkinter import *
import random

class TicTacToe:
    def __init__(self):
        window = Tk()
        self.playing = True
        self.turn = True
        self.imageList = []
        self.imageList.append(PhotoImage(file = "image/empty.gif"))
        self.imageList.append(PhotoImage(file = "image/o.gif"))
        self.imageList.append(PhotoImage(file = "image/x.gif"))
        self.buttonList = []
        self.gameList = []
        frame1 = Frame(window)
        frame1.pack()
        for r in range(6):
            for c in range(7):
                self.buttonList.append(Button(frame1,text = " ", image = self.imageList[0], command = lambda Row = r, Col =c : self.pressed(Row, Col)))
                self.gameList.append(0)
                self.buttonList[r*7+c].grid(row = r, column = c)
        frame2 = Frame(window)
        frame2.pack()
        Button(frame2, text = "재생성", command = self.again).pack()
        window.mainloop()
    def pressed(self, Row, Col):
        self.checkGame()
        for r in range(5, -1, -1):
           if not self.gameList[r*7+Col]:
                if self.playing:
                    if not self.gameList[r*7+Col]:
                        if self.turn: # O턴
                            self.buttonList[r*7 + Col].configure(text = "O",image = self.imageList[1])
                            self.gameList[r * 7 + Col] = 1
                        else: # X턴
                            self.buttonList[r*7 + Col].configure(text = "X",image = self.imageList[2])
                            self.gameList[r * 7 + Col] = 2
                        self.turn = not self.turn
                        break
                    else:
                        pass

    def again(self):
        for r in range(6):
            for c in range(7):
                self.buttonList[r*7+c].configure(image = self.imageList[0])
                self.gameList[r*7+c] = 0


    def checkGame(self):
        for r in range(6):
            if self.gameList[r*3] is 1 and self.gameList[r*3 +1] is 1 and self.gameList[r*3 +2] is 1:
                self.playing = False
            elif self.gameList[r*3] is 2 and self.gameList[r*3+1] is 2 and self.gameList[r*3+2] is 2:
                self.playing = False
            if self.gameList[0*3+r] is 1 and self.gameList[1*3 +r] is 1 and self.gameList[2*3 +r] is 1:
                self.playing = False
            elif self.gameList[0*3+r] is 2 and self.gameList[1*3+r] is 2 and self.gameList[2*3+r] is 2:
                self.playing = False
# 대각선 처리할것
TicTacToe()