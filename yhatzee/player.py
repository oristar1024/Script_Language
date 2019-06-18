class Player:
    UPPER = 6
    LOWER = 7
    def __init__(self, name):
        self.name = name
        self.scores = [0 for i in range(self.UPPER+self.LOWER)]
        self.used = [False for i in range(self.UPPER+self.LOWER)]

    def setScore(self, score, index):
        self.scores[index] = score
    def setAtUsed(self, index):
        self.used[index] = True
    def getUpperScore(self):
        sum = 0
        for i in range(self.UPPER):
            sum += self.scores[i]
        return sum
    def getLowerScore(self):
        sum = 0
        for i in range(self.UPPER, self.LOWER + self.UPPER):
            sum += self.scores[i]
        return sum
    def getUsed(self):
        pass
    def getTotalScore(self):
        up = self.getUpperScore()
        if up > 63:
            up += 35
        low = self.getLowerScore()
        return up + low
    def toString(self):
        return self.name
    def allLowerUsed(self): # lower 사용체크
        for i in range(self.UPPER, self.UPPER+self.LOWER):
            if(self.used[i] == False):
                return False
        return True
    def allUpperUsed(self): # upper 사용체크
        for i in range(self.UPPER):
            if (self.used[i] == False):
                return False
        return True