from tkinter import *
import tkinter
from tkinter import messagebox
import random

class FourMok:
    def remake(self):
        self.turn = False
        for r in range(6):
            for c in range(7):
                self.buttonList[r * 7 + c]["image"] = self.imageList[2]
                self.buttonList[r * 7 + c]["text"] = ' '

    def pressed(self,Row,Col):
        for r in range(5,-1,-1):
            if self.buttonList[r*7+Col]["text"] == ' ':
                self.turn = not self.turn
                if self.turn:
                    self.buttonList[r*7+Col].configure(text = 'O', image = self.imageList[0])
                    self.checkWinner(r,Col)
                else:
                    self.buttonList[r*7+Col].configure(text = 'X', image = self.imageList[1])
                    self.checkWinner(r,Col)
                break

    def checkWinner(self,Row,Col):
        self.checkRow(Row,Col)
        self.checkCol(Row,Col)
        self.checkUpR(Row,Col)
        self.checkUpL(Row,Col)

    def checkRow(self,Row,Col):
        #가로확인
        start = 0
        end = 7
        if Col <= 3:
            end = Col + 4
        if Col >= 3:
            start = Col - 3
        count = 0
        for c in range(start, end):
            if self.turn:  # 'O' 차례인경우
                if self.buttonList[Row * 7 + c]["text"] == 'O':
                    count += 1
                    if count == 4:
                        # '0" 승리
                        tkinter.messagebox.showinfo("게임종료","O 가 승리했습니다.")
                        self.remake()
                else:
                    count = 0

            else:  # "X" 차례인경우
                if self.buttonList[Row * 7 + c]["text"] == 'X':
                    count += 1
                    if count == 4:
                        # 'X" 승리
                        tkinter.messagebox.showinfo("게임종료","X 가 승리했습니다.")
                        self.remake()
                else:
                    count = 0

    def checkCol(self,Row,Col):
        #세로확인
        start = Row
        end = 6

        if Row <= 1:
            end = Row + 4

        count = 0
        for r in range(start, end):
            if self.turn:   # 'O' 차례인경우
                if self.buttonList[r * 7 + Col]["text"] == 'O':
                    count += 1
                    if count == 4:
                        tkinter.messagebox.showinfo("게임종료","O 가 승리했습니다.")
                        self.remake()
                else:
                    count = 0

            else:           # 'X' 차례인경우
                if self.buttonList[r * 7 + Col]["text"] == 'X':
                    count += 1
                    if count == 4:
                        tkinter.messagebox.showinfo("게임종료","X 가 승리했습니다.")
                        self.remake()
                else:
                    count = 0

    def checkUpR(self,Row,Col):
        length = 0
        if Col + Row == 6 or Col + Row == 5:
            length = 6
        elif Col + Row == 4 or Col + Row == 7:
            length = 5
        elif Col + Row == 3 or Col + Row == 8:
            length = 4

        if length >= 4:
            tempRow = Row
            tempCol = Col
            while tempRow < 5 and tempCol > 0:
                tempRow += 1
                tempCol -= 1

            count = 0

            for r in range(0,length):
                if self.turn:  # 'O' 차례인경우
                    if self.buttonList[(tempRow - r) * 7 + (tempCol + r)]["text"] == 'O':
                        count += 1
                        if count == 4:
                            tkinter.messagebox.showinfo("게임종료","O 가 승리했습니다.")
                            self.remake()
                    else:
                        count = 0
                else:
                    if self.buttonList[(tempRow - r) * 7 + (tempCol + r)]["text"] == 'X':
                        count += 1
                        if count == 4:
                            tkinter.messagebox.showinfo("게임종료","X 가 승리했습니다.")
                            self.remake()
                    else:
                        count = 0

    def checkUpL(self,Row,Col):
        tempRow = Row
        tempCol = Col
        while tempRow > 0 and tempCol > 0:
            tempRow -= 1
            tempCol -= 1

        length = 0
        if tempCol == 0:
            if tempRow == 0:
                length = 6
            elif tempRow == 1:
                length = 5
            elif tempRow == 2:
                length = 4
        else:
            if tempCol == 1:
                length = 6
            elif tempCol == 2:
                length = 5
            elif tempCol == 3:
                length = 4

        if length >= 4:
            count = 0
            for r in range(0, length):
                if self.turn:  # 'O' 차례인경우
                    if self.buttonList[(tempRow + r) * 7 + (tempCol + r)]["text"] == 'O':
                        count += 1
                        if count == 4:
                            tkinter.messagebox.showinfo("게임종료","O 가 승리했습니다.")
                            self.remake()
                    else:
                        count = 0
                else:
                    if self.buttonList[(tempRow + r) * 7 + (tempCol + r)]["text"] == 'X':
                        count += 1
                        if count == 4:
                            tkinter.messagebox.showinfo("게임종료","X 가 승리했습니다.")
                            self.remake()
                    else:
                        count = 0

    def __init__(self):
        window = Tk()
        self.turn = False
        self.imageList = []
        self.imageList.append(PhotoImage(file = "book/pybook/image/o.gif"))
        self.imageList.append(PhotoImage(file = "book/pybook/image/x.gif"))
        self.imageList.append(PhotoImage(file = "book/pybook/image/empty.gif"))
        frame1 = Frame(window)
        frame1.pack()
        self.buttonList = []
        for r in range(6):
            for c in range(7):
                self.buttonList.append(Button(frame1,text = ' ', image=self.imageList[2],\
                                              command=lambda Row=r, Col = c: self.pressed(Row, Col)))
                self.buttonList[r*7+c].grid(row = r, column = c)

        frame2 = Frame(window)
        self.button = Button(frame2,text = "다시생성", command = self.remake).pack()
        frame2.pack()

        window.mainloop()


FourMok()