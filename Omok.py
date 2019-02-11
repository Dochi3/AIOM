class Omok:
    def __init__(self):
        self.NONE = 0
        self.BLACK = 1
        self.WHITE = 0
        self.size = 19
        self.newGame()

    def display(self):
        displayString = str()
        for row in range(self.size):
            for col in range(self.size):
                nowStatus = self.board[row][col] % 2
                if not self.board[row][col]:
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
        self.turn = 1

    def checkValid(self, r, c):
        if self.turn == 1 and (r != 9 or c != 9):
            return False
        if r < 0 or r > 18:
            return False
        if c < 0 or c > 18:
            return False
        # if stone put before
        if self.board[r][c]:
            return False
        return True

    def changeTurn(self):
        self.turn += 1

    def putStone(self, r, c):
        r, c = r - 1, c - 1
        if not self.checkValid(r, c):
            return False
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
        r, c = map(int, position.split())
        omok.putStone(r, c)