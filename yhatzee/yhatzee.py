from tkinter import *
from tkinter import font
import  tkinter.messagebox
from player import *
from dice import *
from configuration import *
class YahtzeeBoard:
    UPPERTOTAL = 6
    UPPERBONUS = 7
    LOWERTOTAL = 15
    TOTAL = 16
    dice = []
    diceButtons = []
    fields = [] #점수판 2차원리스트 열 = 플레이어, 행 = 점수
    players = [] #player 객체리스트
    numPlayers = 0
    player = 0 #턴제어
    round = 0 # 13라운드 제어
    roll = 0 #라운드마다 3번까지 가능

    def __init__(self):
        self.initPlayers()

    def initPlayers(self):
        self.pwindow = Tk()
        self.TempFont = font.Font(size = 16, weight = 'bold', family = 'Consolas')
        self.label = []
        self.entry = []
        self.label.append(Label(self.pwindow, text = "플레이어 명수", font = self.TempFont))
        self.label[0].grid(row = 0, column = 0)

        for i in range(1, 11):
            self.label.append(Label(self.pwindow, text = "플레이어"+str(i)+" 이름", font = self.TempFont))
            self.label[i].grid(row = i, column = 0)

        for i in range(11):
            self.entry.append(Entry(self.pwindow, font = self.TempFont))
            self.entry[i].grid(row = i, column =1)
        Button(self.pwindow, text = "Yahtzee 플레이어 설정 완료", font = self.TempFont, command = self.playerNames).grid(row = 11, column = 0)
        self.pwindow.mainloop()

    def playerNames(self):
        self.numPlayers = int(self.entry[0].get())
        for i in range(1, self.numPlayers+1):
            self.players.append(Player(str(self.entry[i].get())))
        self.pwindow.destroy()
        self.initInterface()

    def initInterface(self):
        self.window = Tk("Yhayzee Game")
        self.window.geometry("1800x900")
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')
        for i in range(5):
            self.dice.append(Dice())

        self.rollDice = Button(self.window, text = "Roll Dice", font =self.TempFont, command = self.rollDiceListener)
        self.rollDice.grid(row = 0, column = 0)
        for i in range(5):
            self.diceButtons.append(Button(self.window, text ="?", font = self.TempFont, width = 8, command = lambda row=i: self.diceListener(row)))
            self.diceButtons[i].grid(row=i+1, column = 0)

        for i in range(self.TOTAL+2):
            Label(self.window, text = Configuration.configs[i], font = self.TempFont).grid(row =i, column = 1)
            for j in range(self.numPlayers):
                if i == 0:
                    Label(self.window, text = self.players[j].toString(), font = self.TempFont).grid(row = i, column = 2 + j)
                else:
                    if j == 0:
                        self.fields.append(list())
                    self.fields[i-1].append(Button(self.window, text = "", font = self.TempFont, width = 8, command = lambda row=i-1: self.categoryListener(row)))
                    self.fields[i-1][j].grid(row = i, column = j+2)
                    # 누를 필요없는 버튼은 disable
                    if (j != self.player or (i-1) == self.UPPERTOTAL or (i-1) == self.UPPERBONUS or (i-1) == self.LOWERTOTAL or (i-1) == self.TOTAL):
                        self.fields[i-1][j]['state'] = 'disabled'
                        self.fields[i-1][j]['bg'] = 'light gray'
        self.bottomLabel = Label(self.window, text = self.players[self.player].toString() + "차례: Roll Dice 버튼을 누르세요", width = 35, font = self.TempFont)
        self.bottomLabel.grid(row = self.TOTAL+2, column = 0)
        self.window.mainloop()

    def rollDiceListener(self):
        for i in range(5):
            if self.diceButtons[i]['state'] != 'disabled':
                self.dice[i].rollDie()
                self.diceButtons[i].configure(text = str(self.dice[i].getRoll()))
        if self.roll == 0 or self.roll == 1:
            self.roll += 1
            self.rollDice.configure(text = "Roll Again")
            self.bottomLabel.configure(text = "보관할 주사위 선택 후 Roll Again")
        elif self.roll == 2:
            self.bottomLabel.configure(text = "카테고리를 선택하세요")
            self.rollDice['state'] = 'disabled'
            self.rollDice['bg'] = 'light gray'
    def diceListener(self, row):
        self.diceButtons[row]['state'] = 'disabled'
        self.diceButtons[row]['bg'] = 'light gray'

    def categoryListener(self, row):
        score = Configuration.score(row, self.dice)
        index = row
        if row > 7:
            index = row - 2

        #선택한 카테고리 점수 적고 disable
        self.players[self.player].setScore(score, index)
        self.players[self.player].setAtUsed(index)
        self.fields[row][self.player].configure(text=str(score))
        self.fields[row][self.player]['state'] = 'disabled'
        self.fields[row][self.player]['bg'] = 'light gray'

        #UPPERSCORE 계산
        if self.players[self.player].allUpperUsed():
            self.fields[self.UPPERTOTAL][self.player].configure(text = str(self.players[self.player].getUpperScore()))
            if self.players[self.player].getUpperScore() > 63:
                self.fields[self.UPPERBONUS][self.player].configure(text = '35')
            else:
                self.fields[self.UPPERBONUS][self.player].configure(text = '0')

        #LOWERSCORE 계산
        if self.players[self.player].allLowerUsed():
            self.fields[self.LOWERTOTAL][self.player].configure(text=str(self.players[self.player].getLowerScore()))

        if self.players[self.player].allLowerUsed() and self.players[self.player].allUpperUsed():
            self.fields[self.TOTAL][self.player].configure(text=str(self.players[self.player].getTotalScore()))

        # 턴넘기고 선택불가한 카테고리는 disable
        self.player = (self.player+1) % self.numPlayers
        self.roll = 0
        for i in range(self.TOTAL+1):
            for j in range(self.numPlayers):
                if (j != self.player or (i-1) == self.UPPERTOTAL or (i-1) == self.UPPERBONUS or (i-1) == self.LOWERTOTAL or (i-1) == self.TOTAL):
                    self.fields[i - 1][j]['state'] = 'disabled'
                    self.fields[i - 1][j]['bg'] = 'light gray'
                elif i-1 < 6 and self.players[self.player].used[i-1] == False:
                    self.fields[i - 1][j]['state'] = 'active'
                    self.fields[i - 1][j]['bg'] = 'white'
                elif i-1 > 7 and self.players[self.player].used[i-3] == False and (i-1) != self.TOTAL:
                    self.fields[i - 1][j]['state'] = 'active'
                    self.fields[i - 1][j]['bg'] = 'white'

        for i in range(5):
            self.diceButtons[i]['state'] = 'active'
            self.diceButtons[i]['bg'] = 'white'
            self.diceButtons[i]['text'] = '?'
            self.dice[i].roll = -i
        self.rollDice['state'] = 'active'
        self.rollDice['bg'] = 'white'
        self.rollDice['text'] = 'Roll Dice'
        self.bottomLabel['text'] = self.players[self.player].toString() + "차례: Roll Dice 버튼을 누르세요"

        if self.player == 0:
            self.round += 1
        if self.round == 13:
            winner = None
            winscore = 0
            for one in self.players:
                if one.getTotalScore() > winscore:
                    winner = one
                    winscore = one.getTotalScore()
            self.bottomLabel['text'] = winner.name + "이 승리하였습니다."
            self.rollDice['state'] = 'disabled'
            self.rollDice['bg'] = 'light gray'
            self.rollDice['text'] = 'Roll Dice'

YahtzeeBoard()



