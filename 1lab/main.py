import os

class Piece:
    def __init__(self, color, name, symbol):
        self.color = color
        self.name = name
        self.symbol = symbol

    def get_moves(self, x, y, board):
        # Базовая логика будет переопределена в подклассах
        return [], []

class Rook(Piece):
    def get_moves(self, x, y, board):
        moves, captures = [], []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            for i in range(1, board.size):
                nx, ny = x + dx * i, y + dy * i
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    target = board.grid[ny][nx]
                    if target is None:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        captures.append((nx, ny))
                        break
                    else: break 
                else: break
        return moves, captures

class King(Piece):
    def get_moves(self, x, y, board):
        moves, captures = [], []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    target = board.grid[ny][nx]
                    if target is None:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        captures.append((nx, ny))
        return moves, captures

class Pawn(Piece):
    def get_moves(self, x, y, board):
        moves, captures = [], []
        # Белые (W) ходят "вниз" по индексу (+1), Черные (B) "вверх" (-1)
        direction = 1 if self.color in ["White", "Red"] else -1
        
        if 0 <= y + direction < board.size:
            if board.grid[y + direction][x] is None:
                moves.append((x, y + direction))
        
        for dx in [-1, 1]:
            nx, ny = x + dx, y + direction
            if 0 <= nx < board.size and 0 <= ny < board.size:
                target = board.grid[ny][nx]
                if target is not None and target.color != self.color:
                    captures.append((nx, ny))
        return moves, captures

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def display(self, highlights=([], [])):
        # Очистка консоли
        os.system('cls' if os.name == 'nt' else 'clear')
        moves, captures = highlights
        header = "   " + "".join([f"{i:>3}" for i in range(self.size)])
        print(header)
        print("   " + "---" * self.size)

        for y in range(self.size):
            row = f"{y:<2}|" # Координата Y слева
            for x in range(self.size):
                piece = self.grid[y][x]
                
                # Приоритет отрисовки: Подсказки -> Фигуры -> Пустота
                if (x, y) in moves:
                    cell = "++"
                elif (x, y) in captures:
                    cell = "XX"
                elif piece:
                    cell = piece.symbol
                else:
                    cell = " ."
                
                row += f"{cell:>3}" # Каждая ячейка занимает ровно 3 символа
            print(row)

class ChessGame:
    def __init__(self):
        self.board = None
        self.players = []
        self.turn = 0

    def setup(self):
        print("1. Классика (2 игрока, 8x8)")
        print("2. На троих (3 игрока, 12x12)")
        mode = input("Выбор: ")
        
        if mode == "1":
            self.board = Board(8)
            self.players = ["White", "Black"]
            self._fill_classic()
        else:
            self.board = Board(12)
            self.players = ["White", "Black", "Red"]
            self._fill_three()

    def _fill_classic(self):
        # Расстановка фигур для демонстрации
        for i in range(8):
            self.board.grid[1][i] = Pawn("White", "Pawn", "WP")
            self.board.grid[6][i] = Pawn("Black", "Pawn", "BP")
        self.board.grid[0][0] = Rook("White", "Rook", "WR")
        self.board.grid[0][7] = Rook("White", "Rook", "WR")
        self.board.grid[0][4] = King("White", "King", "WK")
        self.board.grid[7][0] = Rook("Black", "Rook", "BR")
        self.board.grid[7][7] = Rook("Black", "Rook", "BR")
        self.board.grid[7][4] = King("Black", "King", "BK")

    def _fill_three(self):
        # Простая расстановка для 3 игроков по углам
        self.board.grid[0][5] = King("White", "King", "WK")
        self.board.grid[11][5] = King("Black", "King", "BK")
        self.board.grid[5][0] = King("Red", "King", "RK")
        for i in range(12):
            self.board.grid[1][i] = Pawn("White", "Pawn", "WP")
            self.board.grid[10][i] = Pawn("Black", "Pawn", "BP")

    def run(self):
        self.setup()
        while True:
            self.board.display()
            curr = self.players[self.turn % len(self.players)]
            print(f"\nХОД ИГРОКА: {curr}")
            
            try:
                inp = input("Выберите фигуру 'x y' (exit для выхода): ").split()
                if inp[0] == 'exit': break
                sx, sy = int(inp[0]), int(inp[1])
                
                fig = self.board.grid[sy][sx]
                if not fig or fig.color != curr:
                    input("Ошибка: Это не ваша фигура! Enter..."); continue

                moves, caps = fig.get_moves(sx, sy, self.board)
                self.board.display((moves, caps))
                
                target = input("Куда идти 'x y'? ").split()
                ex, ey = int(target[0]), int(target[1])

                if (ex, ey) in moves or (ex, ey) in caps:
                    self.board.grid[ey][ex] = fig
                    self.board.grid[sy][sx] = None
                    self.turn += 1
                else:
                    input("Недопустимый ход! Enter...")
            except Exception as e:
                input(f"Ошибка ввода! ({e}) Enter...")

if __name__ == "__main__":
    ChessGame().run()
