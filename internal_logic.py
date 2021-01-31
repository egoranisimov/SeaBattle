class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы пытаетесь выстрелить за пределы доски'


class BoardShootedDotsException(BoardException):
    def __str__(self):
        return 'Вы уже стреляли в эту клетку'


class BoardContourDotsException(BoardException):
    def __str__(self):
        return 'Нет смысла стрелять в эту клетку, поскольку она граничит ' \
               'с убитым кораблем '


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'


class Board:
    def __init__(self, hid=False, size=6, indent=False):
        self.hid = hid
        self.size = size
        self.indent = indent

        self.ships = []
        self.field = [['O'] * self.size for _ in range(self.size)]
        self.count = 0

        self.busy = []
        self.shooted_dots = []
        self.cont = []

    def out_of_board(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def contour(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1)]

        for dot in ship.dots():
            for dx, dy in near:
                cur = Dot(dot.x + dx, dot.y + dy)
                if not (self.out_of_board(cur)) and cur not in ship.dots():
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                        self.cont.append(cur)
                    if cur not in self.busy:
                        self.busy.append(cur)

    def add_ship(self, ship):
        for dot in ship.dots():
            if self.out_of_board(dot) or dot in self.busy:
                raise BoardWrongShipException
        for dot in ship.dots():
            self.field[dot.x][dot.y] = '■'
            self.busy.append(dot)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, dot):
        if self.out_of_board(dot):
            raise BoardOutException
        if dot in self.cont:
            raise BoardContourDotsException
        if dot in self.shooted_dots:
            raise BoardShootedDotsException

        self.shooted_dots.append(dot)

        for ship in self.ships:
            if dot in ship.dots():
                ship.lives -= 1
                self.field[dot.x][dot.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)

                    if self.indent:
                        print(" " * 32, 'Корабль уничтожен!')
                    else:
                        print('Корабль уничтожен!')

                    return False

                else:
                    if self.indent:
                        print(" " * 32, 'Корабль ранен!')
                    else:
                        print('Корабль ранен!')

                    return True

        self.field[dot.x][dot.y] = '.'

        if self.indent:
            print(" " * 32, 'Мимо!')
        else:
            print('Мимо!')

        return False

    def __repr__(self):
        board = '    '
        for i in range(self.size):
            board += f' {i + 1}  '
        for i in range(self.size):
            board += f'\n {i + 1} |'
            for j in self.field[i]:
                board += f' {j} |'
        if self.hid:
            board = board.replace('■', 'O')
        return board


class Ship:
    def __init__(self, begining, length, orient):
        self.begining = begining
        self.length = length
        self.orient = orient
        self.lives = length

    def dots(self):
        ship_dots = []
        for i in range(self.length):
            if self.orient == 0:
                ship_dots.append(Dot(self.begining.x + i, self.begining.y))
            else:
                ship_dots.append(Dot(self.begining.x, self.begining.y + i))
        return ship_dots

    def __repr__(self):
        return f'{self.dots()}'
