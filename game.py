import tkinter as tk
from tkinter import messagebox

class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.geometry("300x300")

        self.current_player = "X"
        self.board = [[None]*3 for _ in range(3)]

        self.buttons = [[tk.Button(self, width=10, height=3, font=("Helvetica", 24),
                                   command=lambda row=row, col=col: self.on_click(row, col))
                         for col in range(3)] for row in range(3)]

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].grid(row=row, column=col)

    def on_click(self, row, col):
        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state="disabled")

            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"{self.current_player} wins!")
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    row, col = self.computer_move()
                    self.on_click(row, col)

    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return True

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return True

        return False

    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell is None:
                    return False
        return True

    def reset_game(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state="normal")
                self.board[row][col] = None
        self.current_player = "X"

    def evaluate(self):
        # Checking for Rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2]:
                if self.board[row][0] == "X":
                    return -1
                elif self.board[row][0] == "O":
                    return 1

        # Checking for Columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col]:
                if self.board[0][col] == "X":
                    return -1
                elif self.board[0][col] == "O":
                    return 1

        # Checking for Diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == "X":
                return -1
            elif self.board[0][0] == "O":
                return 1

        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == "X":
                return -1
            elif self.board[0][2] == "O":
                return 1

        # Draw
        return 0

    def can_move(self, row, col):
        return self.board[row][col] is None

    def get_all_available_pos(self):
        ans = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    ans.append((i, j))
        return ans

    def minimax(self, is_player):
        utility_func_val = self.evaluate()

        if utility_func_val == 1 or utility_func_val == -1:
            return utility_func_val, None, None

        if self.check_draw():
            return 0, None, None

        if is_player:
            best = -float('inf')
            best_row, best_col = None, None
            for i in range(3):
                for j in range(3):
                    if self.can_move(i, j):
                        self.board[i][j] = "O"
                        val, _, _ = self.minimax(False)
                        self.board[i][j] = None
                        if val > best:
                            best = val
                            best_row, best_col = i, j
            return best, best_row, best_col
        else:
            best = float('inf')
            best_row, best_col = None, None
            for i in range(3):
                for j in range(3):
                    if self.can_move(i, j):
                        self.board[i][j] = "X"
                        val, _, _ = self.minimax(True)
                        self.board[i][j] = None
                        if val < best:
                            best = val
                            best_row, best_col = i, j
            return best, best_row, best_col

    def computer_move(self):
        _, row, col = self.minimax(True)
        return row, col

if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
