from tkinter import *
import random

class TicTacToe:
    def __init__(self):
        window = Tk()
        window.title("TicTacToe")
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
        for r in range(3):
            for c in range(3):
                self.buttonList.append(Button(frame1, image = self.imageList[0], command = lambda Row = r, Col =c : self.pressed(Row, Col)))
                self.gameList.append(0)
                self.buttonList[r*3+c].grid(row = r, column = c)
        frame2 = Frame(window)
        frame2.pack()
        self.label = Label(frame2, text = "O 차례")
        self.label.pack()
        window.mainloop()
    def pressed(self, Row, Col):
        if self.playing:
            if not self.gameList[Row*3+Col]:
                if self.turn: # O턴
                    self.buttonList[ Row*3 + Col].configure(image = self.imageList[1])
                    self.label.configure(text = "X 차례")
                    self.gameList[Row * 3 + Col] = 1
                else: # X턴
                    self.buttonList[Row*3 + Col].configure(image = self.imageList[2])
                    self.label.configure(text="O 차례")
                    self.gameList[Row * 3 + Col] = 2
                self.turn = not self.turn
                self.checkGame()
            else:
                pass

    def checkGame(self):
        for r in range(3):
            if self.gameList[r*3] is 1 and self.gameList[r*3 +1] is 1 and self.gameList[r*3 +2] is 1:
                self.label.configure(text = "O 승리! 게임이 끝났습니다.")
                self.playing = False
                break
            elif self.gameList[r*3] is 2 and self.gameList[r*3+1] is 2 and self.gameList[r*3+2] is 2:
                self.label.configure(text="X 승리! 게임이 끝났습니다.")
                self.playing = False
                break
            if self.gameList[0*3+r] is 1 and self.gameList[1*3 +r] is 1 and self.gameList[2*3 +r] is 1:
                self.label.configure(text = "O 승리! 게임이 끝났습니다.")
                self.playing = False
                break
            elif self.gameList[0*3+r] is 2 and self.gameList[1*3+r] is 2 and self.gameList[2*3+r] is 2:
                self.label.configure(text="X 승리! 게임이 끝났습니다.")
                self.playing = False
                break
        if self.gameList[0] is 1 and self.gameList[4] is 1 and self.gameList[8] is 1:
            self.label.configure(text="O 승리! 게임이 끝났습니다.")
            self.playing = False
            return
        elif self.gameList[0] is 2 and self.gameList[4] is 2 and self.gameList[8] is 2:
            self.label.configure(text="X 승리! 게임이 끝났습니다.")
            self.playing = False
            return
        if self.gameList[2] is 1 and self.gameList[4] is 1 and self.gameList[6] is 1:
            self.label.configure(text="O 승리! 게임이 끝났습니다.")
            self.playing = False
            return
        elif self.gameList[2] is 2 and self.gameList[4] is 2 and self.gameList[6] is 2:
            self.label.configure(text="X 승리! 게임이 끝났습니다.")
            self.playing = False
            return

        count = 0
        for i in range(9):
            if self.gameList[i] == 1 or self.gameList[i] == 2:
                count += 1
            else:
                break
        if count == 9:
            self.label.configure(text="비김! 게임이 끝났습니다.")
            self.playing = False
TicTacToe()
