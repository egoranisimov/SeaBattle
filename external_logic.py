from internal_logic import BoardException, BoardWrongShipException, Dot, Board, Ship
from random import randint


class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardException as e:
                if not self.board.indent:
                    print(" " * 32, e)
                else:
                    print(e)


class AI(Player):
    def ask(self):
        while True:
            dot = Dot(randint(0, self.enemy_board.size - 1),
                      randint(0, self.enemy_board.size - 1))
            if dot not in self.enemy_board.cont and dot not in self.enemy_board.shooted_dots:
                break

        print(f'Ход компьютера - {dot.x + 1} {dot.y + 1}')
        return dot


class User(Player):
    def ask(self):
        while True:
            cord = input(" " * 33 + 'Ваш ход, введите координаты: ').split()
            if len(cord) != 2:
                print(" " * 32, 'Ввдетие две координаты!')
                continue
            x, y = cord

            if not(x.isdigit()) or not(y.isdigit()):
                print(" " * 32, 'Введите числа!')

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        player_board = self.random_board()
        comp_board = self.random_board()
        comp_board.hid = True
        comp_board.indent = True

        self.ai = AI(comp_board, player_board)
        self.user = User(player_board, comp_board)

    def random_ship(self):
        ship_length = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        count = 0
        for l in ship_length:
            while True:
                count += 1
                if count > 2000:
                    return None

                ship = Ship(Dot(randint(0, self.size - 1), randint(0, self.size - 1)), l, randint(0, 1))

                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.random_ship()

        return board

    def greet(self):
        print("-" * 65)
        print("Приветсвуем вас в игре морской бой".center(65))
        print("-" * 65)
        print("формат ввода: x y".center(65))
        print("x - номер строки".center(65))
        print("y - номер столбца".center(65))
        print("-" * 65, '\n')

    def set_boards(self):
        print("Доска пользователя:".center(27), "         ",
              "Доска компьютера:".center(27))
        player_board = str(self.user.board).split('\n')
        comp_board = str(self.ai.board).split('\n')
        boards = ''

        for i in range(self.size + 1):
            boards += player_board[i] + "    |    " + comp_board[i] + "\n"

        return boards[0:-1]

    def loop(self):
        num = 0
        while True:
            print(self.set_boards())
            if num % 2 == 0:
                print("-" * 65)
                print(" " * 32, "Ходит пользователь!")
                repeat = self.user.move()
            else:
                print("-" * 65)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 65)
                print(self.set_boards())
                print(" " * 32, "Пользователь выиграл!")
                break

            if self.user.board.count == 7:
                print("-" * 65)
                print(self.set_boards())
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()
