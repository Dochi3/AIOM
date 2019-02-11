import OmokValue
class Omok:
    def __init__(self):
        self.size = 19
        self.newGame()

    def display(self):
        displayString = str()
        for row in range(self.size):
            for col in range(self.size):
                nowStatus = self.board[row][col] % 2
                if not self.board[row][col]:
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
        displayString = displayString[:-39]
        return displayString

    def newGame(self):
        self.board = [[OmokValue.NONE for col in range(self.size)] for row in range(self.size)]
        self.turn = 1
        self.gameOver = False

    def isValidPosition(self, r, c):
        if r < 0 or r > 18:
            return False
        if c < 0 or c > 18:
            return False
        return True

    def countStone(self, r, c, dir_x, dir_y):
        count, counter = [0, 0], False
        nowStatus, jump = self.turn % 2, 0
        while jump < 2:
            r, c = r + dir_x, c + dir_y
            if not self.isValidPosition(r, c):
                break
            if not self.board[r][c]:
                jump += 1
            if self.board[r][c] % 2 != nowStatus:
                counter = True
                break
        return (count, counter)

    def checkValid(self, r, c):
        # start position
        if self.turn == 1 and (r != 9 or c != 9):
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
            positive, p_counter = self.countStone(r, c, dir_x, dir_y)
            negative, n_counter = self.countStone(r, c, -dir_x, -dir_y)
            linearCount = positive[0] + negative[0]
            if linearCount == 4:
                return (True, OmokValue.CASE_OMOK)

            # white stone has no abandonment
            if self.turn % 2 == OmokValue.WHITE:
                continue
            
            # case Over 6
            if linearCount > 5:
                return (False, OmokValue.CASE_OVER_6)

            # case 3x3

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
        print(omok.display())
        position = input("Enter pos : ")
        if position == "exit":
            break
        br, bc = map(int, position.split())
        omok.putStone(br, bc)
