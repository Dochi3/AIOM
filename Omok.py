import OmokValue
class Omok:
    def __init__(self):
        self.size = 5
        self.gameOver = True
        self.newGame()

    def display(self):
        displayString = str()
        sliceSize = self.size * 2 + 1
        if self.gameOver:
            displayString = ("BLACK" if self.turn % 2 else "WHITE") + " win" + " " * sliceSize
        else:
            for row in range(self.size):
                for col in range(self.size):
                    nowStatus = self.board[row][col] % 2
                    validity, omokCase = self.checkValid(row, col)
                    if omokCase == OmokValue.CASE_3X3:
                        displayString += "3"
                    elif omokCase == OmokValue.CASE_4X4:
                        displayString += "4"
                    elif omokCase == OmokValue.CASE_OVER_6:
                        displayString += "6"
                    elif not self.board[row][col]:
                        displayString += " "
                    elif nowStatus == OmokValue.WHITE:
                        displayString += "O"
                    else:
                        displayString += "X"
                    displayString += "─"
                displayString = displayString[:-1] + "\n"
                for col in range(self.size):
                    displayString += "| "
                displayString = displayString[:-1] + "\n"
        displayString = displayString[:-sliceSize]
        return displayString

    def newGame(self):
        self.board = [[OmokValue.NONE for col in range(self.size)] for row in range(self.size)]
        self.turn = 1
        self.gameOver = False

    def isValidPosition(self, r, c):
        if r < 0 or r > self.size - 1:
            return False
        if c < 0 or c > self.size - 1:
            return False
        return True

    def countStone(self, r, c, dir_x, dir_y):
        count = [0, 0]
        nowStatus, jump = self.turn % 2, 0
        while jump < 2:
            r, c = r + dir_x, c + dir_y
            if not self.isValidPosition(r, c):
                jump = 2
                break
            if not self.board[r][c]:
                jump += 1
                continue
            if self.board[r][c] % 2 != nowStatus:
                break
            count[jump] += 1
        return (count, jump)

    def checkValid(self, r, c):
        # start position
        if self.turn == 1 and (r != self.size // 2 or c != self.size // 2):
            return (False, OmokValue.START_POSITION_ERROR)

        # check about position is valid
        if not self.isValidPosition(r, c):
            return (False, OmokValue.OUT_OF_BOARD)

        # if stone put before
        if self.board[r][c]:
            return (False, OmokValue.EXIST_POSITION)

        directions = [[0, 1], [1, 1], [1, 0], [1, -1]]
        case3x3, case4x4 = 0, 0
        for dir_x, dir_y in directions:
            positive, pCounter = self.countStone(r, c, dir_x, dir_y)
            negative, nCounter = self.countStone(r, c, -dir_x, -dir_y)
            linearCount, jumpCount = positive[0] + negative[0], positive[1] + negative[1]
            if linearCount == 4:
                return (True, OmokValue.CASE_OMOK)

            # white stone has no abandonment
            if self.turn % 2 == OmokValue.WHITE:
                continue

            # case Over 6
            if linearCount > 5:
                return (False, OmokValue.CASE_OVER_6)

            # case 3x3
            if pCounter * nCounter == 0:
                continue
            elif not jumpCount and linearCount == 2:
                case3x3 += 1
            elif (positive[1] and not negative[1]
                  and linearCount + positive[1] == 2 and pCounter > 1):
                case3x3 += 1
            elif (negative[1] and not positive[1]
                  and linearCount + negative[1] == 2 and nCounter > 1):
                case3x3 += 1

            # case 4x4
            if positive[1] + negative[1] == 0 and linearCount == 3:
                case4x4 += 1
            elif positive[1] and linearCount + positive[1] == 3:
                case4x4 += 1
            elif negative[1] and linearCount + negative[1] == 3:
                case4x4 += 1

            if case3x3 >= 2:
                return (False, OmokValue.CASE_3X3)
            if case4x4 >= 2:
                return (False, OmokValue.CASE_4X4)

        return (True, OmokValue.NONE)

    def changeTurn(self):
        self.turn += 1

    def putStone(self, r, c):
        if self.gameOver:
            return False
        r, c = r - 1, c - 1
        validity, omokCase = self.checkValid(r, c)
        if not validity:
            return False
        if omokCase == OmokValue.CASE_OMOK:
            self.gameOver = True
            return True
        self.board[r][c] = self.turn
        self.changeTurn()
        return True


if __name__ == "__main__":
    from os import system
    omok = Omok()
    displayClear = lambda: system("clear")
    while True:
        displayClear()
        print(omok.display(), flush=True)
        position = input("Enter pos : ")
        if position == "exit":
            break
        br, bc = map(int, position.split())
        omok.putStone(br, bc)
