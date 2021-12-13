import math
import random


class TicTacToe():
    """The Tic-Tac-Toe with AI
    The hard project of Hyperskill"""

    size_of_side = 3

    def __init__(self):
        self.cells = []
        self.count_zero = 0
        self.count_x = 0
        self.free_cells = []
        self.x_player = ""
        self.y_player = ""

    def start(self):
        while True:
            try:
                answer = input("Input command: ")
                settings = answer.split()
                if len(settings) == 0:
                    raise Exception
                if settings[0] == "exit" and len(settings) > 1:
                    raise Exception
                if settings[0] == "start":
                    if len(settings) != 3:
                        raise Exception
                    if settings[1] not in ("user", "easy", "medium", "hard"):
                        raise  Exception
                    if settings[2] not in ("user", "easy", "medium", "hard"):
                        raise  Exception
                if settings[0] == "exit":
                    return False
                elif settings[0] == "start":
                    self.x_player = settings[1]
                    self.y_player = settings[2]
                if settings[0] not in ("start", "finish"):
                    raise Exception
                return True
            except:
                print("Bad parameters!")

    def create_cell(self):
        i, j, self.count_x, self.count_zero = 0, 0, 0, 0
        self.cells.clear()
        self.free_cells.clear()

        for i in range(TicTacToe.size_of_side):
            row = list()
            for j in range(TicTacToe.size_of_side):
                row.append("_")
                self.free_cells.append((i, j))
            self.cells.append(row)

    def print_state(self):
        print("---------")
        for i in range(TicTacToe.size_of_side):
            print("| ", end="")
            for j in range(TicTacToe.size_of_side):
                print(f"{self.cells[i][j]} ", end="")
            print("| ")
        print("---------")

    def cell_value(self, x, y):
        return self.cells[x - 1][y - 1]

    def delete_free_cell(self, i, j):
        if (i, j) in self.free_cells:
            self.free_cells.remove((i, j))

    def find_almost_win_cell(self, mark):
        for i in range(TicTacToe.size_of_side):
            count_mark, count_empty = 0, 0
            empty_cell = (-1, -1)
            for j in range(TicTacToe.size_of_side):
                if self.cells[i][j] == mark:
                    count_mark += 1
                elif self.cells[i][j] == "_":
                    count_empty += 1
                    empty_cell = (i, j)
            if count_mark == 2 and count_empty == 1:
                return empty_cell

        for j in range(TicTacToe.size_of_side):
            count_mark, count_empty = 0, 0
            empty_cell = (-1, -1)
            for i in range(TicTacToe.size_of_side):
                if self.cells[i][j] == mark:
                    count_mark += 1
                elif self.cells[i][j] == "_":
                    count_empty += 1
                    empty_cell = (i, j)
            if count_mark == 2 and count_empty == 1:
                return empty_cell

        count_mark, count_empty = 0, 0
        empty_cell = (-1, -1)
        for i in range(TicTacToe.size_of_side):
            if self.cells[i][i] == mark:
                count_mark += 1
            elif self.cells[i][i] == "_":
                count_empty += 1
                empty_cell = (i, i)
        if count_mark == 2 and count_empty == 1:
            return empty_cell

        count_mark, count_empty = 0, 0
        empty_cell = (-1, -1)
        for i in range(TicTacToe.size_of_side):
            j = TicTacToe.size_of_side - i - 1
            if self.cells[i][j] == mark:
                count_mark += 1
            elif self.cells[i][j] == "_":
                count_empty += 1
                empty_cell = (i, j)
        if count_mark == 2 and count_empty == 1:
            return empty_cell

        return None

    def get_antimark(self, mark):
        if mark == "X":
            return "O"
        else:
            return "X"

    def put_the_mark(self, i, j, mark):
        self.cells[i][j] = mark
        self.delete_free_cell(i, j)

    def make_turn(self, type_of_player, mark):
        if type_of_player == "user":
            while True:
                try:
                    coordinates_string = input("Enter the coordinates: ")
                    x, y = [int(word) for word in coordinates_string.split()]
                    if x < 1 or x > TicTacToe.size_of_side \
                            or y < 1 or y > TicTacToe.size_of_side:
                        raise IndexError
                    if game.cell_value(x, y) != "_":
                        print("This cell is occupied! Choose another one!")
                        raise Exception()
                    break
                except ValueError:
                    print("You should enter numbers!")
                except IndexError:
                    print("Coordinates should be from 1 to 3!")
                except Exception:
                    pass
            self.put_the_mark(x - 1, y - 1, mark)
        elif type_of_player == "easy":
            cell = random.choice(self.free_cells)
            self.put_the_mark(cell[0], cell[1], mark)
        elif type_of_player == "medium":
            # at first let's try to win!
            cell = self.find_almost_win_cell(mark)
            # okay, we haven't won yet
            # let's try to prevent the opponent's win!
            if cell is None:
                cell = self.find_almost_win_cell(self.get_antimark(mark))
                if cell is None:
                    # if we still here...
                    # well, all we can do is random move...
                    cell = random.choice(self.free_cells)
            self.put_the_mark(cell[0], cell[1], mark)
        elif type_of_player == "hard":
            # let's try to find optimum cell using mimimax algorithm
            cell = self.find_best_move(mark)["cell"]
            self.put_the_mark(cell[0], cell[1], mark)

    def copy(self):
        new_board = TicTacToe()
        new_board.create_cell()
        for i in range(TicTacToe.size_of_side):
            for j in range(TicTacToe.size_of_side):
                new_board.cells[i][j] = self.cells[i][j]
        new_board.free_cells = self.free_cells.copy()
        return new_board

    def find_best_move(self, mark):

        best_move = (-1, -1)
        if self.game_status() == "X wins":
            return {"cell": best_move, "score": 10}
        elif self.game_status() == "O wins":
            return {"cell": best_move, "score": -10}
        elif self.game_status == "Draw":
            return {"cell": best_move, "score": 0}

        if mark == "X":
            best_value = -10000
        elif mark == "O":
            best_value = 10000

        for free_cell in self.free_cells:
            new_board = self.copy()
            new_board.put_the_mark(free_cell[0], free_cell[1], mark)

            hyp_move = new_board.find_best_move(self.get_antimark(mark))
            hyp_value = hyp_move["score"]
            if mark == "X" and hyp_value > best_value:
                best_value = hyp_value
                best_move = free_cell
            if mark == "O" and hyp_value < best_value:
                best_value = hyp_value
                best_move = free_cell

        return {"cell": best_move, "score": best_value}

    def game_status(self):
        # check the rows
        free_cells_count = 0
        for i in range(TicTacToe.size_of_side):
            count_x, count_y = 0, 0
            for j in range(TicTacToe.size_of_side):
                if self.cells[i][j] == "X":
                    count_x += 1
                elif self.cells[i][j] == "O":
                    count_y += 1
                elif self.cells[i][j] == "_":
                    free_cells_count += 1
            if count_x == 3:
                return "X wins"
            elif count_y == 3:
                return "O wins"

        # check the columns
        for i in range(TicTacToe.size_of_side):
            count_x, count_y = 0, 0
            for j in range(TicTacToe.size_of_side):
                if self.cells[j][i] == "X":
                    count_x += 1
                elif self.cells[j][i] == "O":
                    count_y += 1
            if count_x == 3:
                return "X wins"
            elif count_y == 3:
                return "O wins"

        # check the diagonals
        count_x, count_y = 0, 0
        for i in range(TicTacToe.size_of_side):
            if self.cells[i][i] == "X":
                count_x += 1
            elif self.cells[i][i] == "O":
                count_y += 1
        if count_x == 3:
            return "X wins"
        elif count_y == 3:
            return "O wins"

        count_x, count_y = 0, 0
        for i in range(TicTacToe.size_of_side):
            if self.cells[i][TicTacToe.size_of_side - i - 1] == "X":
                count_x += 1
            elif self.cells[i][TicTacToe.size_of_side - i - 1] == "O":
                count_y += 1
        if count_x == 3:
            return "X wins"
        elif count_y == 3:
            return "O wins"

        if free_cells_count > 0:
            return "Game not finished"
        else:
            return "Draw"

game = TicTacToe()

if not game.start():
    exit(0)

game.create_cell()
game.print_state()

type_of_player = game.x_player
mark = "X"

while True:
    game.make_turn(type_of_player, mark)
    if type_of_player in ("easy", "medium", "hard"):
         print(f"Making move level \"{type_of_player}\"")
    game.print_state()
    status = game.game_status()
    if status != "Game not finished":
        print(status)
        exit()
    if mark == "X":
        mark = "O"
        type_of_player = game.y_player
    else:
        mark = "X"
        type_of_player = game.x_player




