from dice import *
class Configuration:
    configs = ["Category", "Ones", "Twos", "Threes","Fours","Fives","Sixes", "Upper Scores","Upper Bonus(35)","Three of a kind", "Four of a kind", "Full House(25)", "Small Straight(30)", "Large Straight(40)", "Yahtzee(50)","Chance","Lower Scores", "Total"]

    def getConfigs():
        return Configuration.configs

    def score(row, d):
        if row >= 0 and row < 6:
            return Configuration.ScoreUpper(d, row+1)
        elif row == 8:
            return Configuration.scoreThreeOfAKind(d)
        elif row == 9:
            return Configuration.scoreFourOfAKind(d)
        elif row == 10:
            return Configuration.scoreFullHouse(d)
        elif row == 11:
            return Configuration.scoreSmallStraight(d)
        elif row == 12:
            return Configuration.scoreLargeStraight(d)
        elif row == 13:
            return Configuration.scoreYahtzee(d)
        elif row == 14:
            return Configuration.sumDie(d)


    def ScoreUpper(d, num):
        tot = 0
        for i in d:
            if i.getRoll() == num:
                tot += num
        return tot

    def scoreThreeOfAKind(d):
        for num in range(3):
            checker = d[num].getRoll()
            cnt = 0
            for i in d:
                if i.getRoll() == checker:
                    cnt += 1
            if cnt >= 3:
                sum = 0
                for i in d:
                    sum += i.getRoll()
                return sum
        return 0


    def scoreFourOfAKind(d):
        for num in range(2):
            checker = d[num].getRoll()
            cnt = 0
            for i in d:
                if i.getRoll() == checker:
                    cnt += 1
            if cnt >= 4:
                sum = 0
                for i in d:
                    sum += i.getRoll()
                return sum
        return 0

    def scoreFullHouse(d):
        d1 = d[0].getRoll()
        d2 = 0
        cnt1 = 0
        cnt2 = 0
        for i in d:
            if i.getRoll() == d1:
                cnt1 += 1
            elif d2 == 0:
                d2 = i.getRoll()
                cnt2 += 1
            elif i.getRoll() == d2:
                cnt2 += 1
            else:
                return 0
        if cnt1 < 4 and cnt2 <4:
            return 25
        else:
            return 0


    def scoreSmallStraight(d):
        diceset = set()
        for i in d:
            diceset.add(i.getRoll())
        for i in range(1,4):
            tmpset = {i, i+1, i+2, i+3}
            if diceset.intersection(tmpset) == tmpset:
                return 30
        return 0



    def scoreLargeStraight(d):
        diceset = set()
        for i in d:
            diceset.add(i.getRoll())
        for i in range(1, 3):
            tmpset = {i, i + 1, i + 2, i + 3, i+4}
            if diceset.intersection(tmpset) == tmpset:
                return 40
        return 0

    def scoreYahtzee(d):
        checker = d[0].getRoll()
        for i in d:
            if i.getRoll() != checker:
                return 0
        return 50

    def sumDie(d):
        sum = 0
        for i in d:
            sum += i.getRoll()
        return sum