class Omok:
    def __init__(self):
        self.NONE = -1
        self.BLACK = 0
        self.WHITE = 1
        self.size = 19
        self.turn = self.BLACK
        self.newGame()

    def display(self):
        displayString = str()
        for row in range(self.size):
            for col in range(self.size):
                nowStatus = self.board[row][col]
                if nowStatus == self.NONE:
                    displayString += " "
                elif nowStatus == self.WHITE:
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
        self.board = [[self.NONE for col in range(self.size)] for row in range(self.size)]

    def checkValid(self, r, c):
        # if stone put before
        if self.board[r][c]:
            return False

    def changeTurn(self):
        self.turn = 1 - self.turn

    def putStone(self, r, c):
        if not self.checkValid(r, c):
            return False
        self.board[r][c] = self.turn
        self.changeTurn()


if __name__ == "__main__":
    from os import system
    omok = Omok()
    displayClear = lambda: system("clear")
    while True:
        displayClear()
        print(omok.display())
        r, c = map(int, input("Enter pos :").split())
        omok.putStone(r, c)