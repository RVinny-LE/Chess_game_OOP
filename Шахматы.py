from enum import Enum, auto

# Перечисление для цветов фигур
class Color(Enum):
    WHITE = auto()
    BLACK = auto()

# Базовый класс для всех шахматных фигур
class Piece:
    def __init__(self, color):
        """
        Инициализирует фигуру с указанным цветом.

        :param color: Цвет фигуры (Color.WHITE или Color.BLACK).
        """
        self.color = color

    def __str__(self):
        """
        Возвращает символ фигуры.

        :return: Символ фигуры.
        """
        return self.symbol[self.color]

    def is_valid_move(self, start, end, board):
        """
        Проверяет, является ли ход допустимым для данной фигуры.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если ход допустим, иначе False.
        """
        raise NotImplementedError("Метод должен быть реализован в подклассе")

# Класс для пешки
class Pawn(Piece):
    symbol = {
        Color.WHITE: '♙',
        Color.BLACK: '♟'
    }

    def is_valid_move(self, start, end, board):
        """
        Проверяет, является ли ход допустимым для пешки.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если ход допустим, иначе False.
        """
        x1, y1 = start
        x2, y2 = end
        direction = -1 if self.color == Color.WHITE else 1
        # Пешка движется вперед на одну клетку
        if y1 == y2 and x2 == x1 + direction and not board.get_piece(x2, y2):
            return True
        # Пешка движется вперед на две клетки (только из начальной позиции)
        if y1 == y2 and x2 == x1 + 2 * direction and x1 == (6 if self.color == Color.WHITE else 1) and not board.get_piece(x2, y2):
            return True
        # Пешка бьет по диагонали
        if abs(y2 - y1) == 1 and x2 == x1 + direction:
            target = board.get_piece(x2, y2)
            if target and target.color != self.color:
                return True
            # Взятие на проходе
            if (x2, y2) == board.en_passant_target:
                return True
        return False

# Класс для ладьи
class Rook(Piece):
    symbol = {
        Color.WHITE: '♖',
        Color.BLACK: '♜'
    }

    def is_valid_move(self, start, end, board):
        """
        Проверяет, является ли ход допустимым для ладьи.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если ход допустим, иначе False.
        """
        x1, y1 = start
        x2, y2 = end
        # Ладья движется по прямой
        if x1 == x2 or y1 == y2:
            return self.is_path_clear(start, end, board)
        return False

    def is_path_clear(self, start, end, board):
        """
        Проверяет, свободен ли путь для ладьи.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если путь свободен, иначе False.
        """
        x1, y1 = start
        x2, y2 = end
        if x1 == x2:
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if board.get_piece(x1, y):
                    return False
        else:
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if board.get_piece(x, y1):
                    return False
        return True

# Класс для коня
class Knight(Piece):
    symbol = {
        Color.WHITE: '♘',
        Color.BLACK: '♞'
    }

    def is_valid_move(self, start, end, board):
        """
        Проверяет, является ли ход допустимым для коня.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если ход допустим, иначе False.
        """
        x1, y1 = start
        x2, y2 = end
        # Конь движется буквой "Г"
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

# Класс для слона
class Bishop(Piece):
    symbol = {
        Color.WHITE: '♗',
        Color.BLACK: '♝'
    }

    def is_valid_move(self, start, end, board):
        """
        Проверяет, является ли ход допустимым для слона.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если ход допустим, иначе False.
        """
        x1, y1 = start
        x2, y2 = end
        # Слон движется по диагонали
        if abs(x2 - x1) == abs(y2 - y1):
            return self.is_path_clear(start, end, board)
        return False

    def is_path_clear(self, start, end, board):
        """
        Проверяет, свободен ли путь для слона.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если путь свободен, иначе False.
        """
        x1, y1 = start
        x2, y2 = end
        step_x = 1 if x2 > x1 else -1
        step_y = 1 if y2 > y1 else -1
        x, y = x1 + step_x, y1 + step_y
        while x != x2 and y != y2:
            if board.get_piece(x, y):
                return False
            x += step_x
            y += step_y
        return True

# Класс для ферзя
class Queen(Piece):
    symbol = {
        Color.WHITE: '♕',
        Color.BLACK: '♛'
    }

    def is_valid_move(self, start, end, board):
        """
        Проверяет, является ли ход допустимым для ферзя.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если ход допустим, иначе False.
        """
        x1, y1 = start
        x2, y2 = end

        # Проверка движения по прямой (как ладья)
        if x1 == x2 or y1 == y2:
            return self.is_path_clear_straight(start, end, board)

        # Проверка движения по диагонали (как слон)
        if abs(x2 - x1) == abs(y2 - y1):
            return self.is_path_clear_diagonal(start, end, board)

        return False

    def is_path_clear_straight(self, start, end, board):
        """
        Проверяет, свободен ли путь для движения по прямой (как ладья).

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если путь свободен, иначе False.
        """
        x1, y1 = start
        x2, y2 = end

        if x1 == x2:
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if board.get_piece(x1, y):
                    return False
        else:
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if board.get_piece(x, y1):
                    return False

        return True

    def is_path_clear_diagonal(self, start, end, board):
        """
        Проверяет, свободен ли путь для движения по диагонали (как слон).

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если путь свободен, иначе False.
        """
        x1, y1 = start
        x2, y2 = end

        step_x = 1 if x2 > x1 else -1
        step_y = 1 if y2 > y1 else -1

        x, y = x1 + step_x, y1 + step_y
        while x != x2 and y != y2:
            if board.get_piece(x, y):
                return False
            x += step_x
            y += step_y

        return True

# Класс для короля
class King(Piece):
    symbol = {
        Color.WHITE: '♔',
        Color.BLACK: '♚'
    }

    def is_valid_move(self, start, end, board):
        """
        Проверяет, является ли ход допустимым для короля.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если ход допустим, иначе False.
        """
        x1, y1 = start
        x2, y2 = end
        # Король движется на одну клетку в любом направлении
        if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1:
            return True
        # Рокировка
        if x1 == x2 and abs(y2 - y1) == 2:
            return self.can_castle(start, end, board)
        return False

    def can_castle(self, start, end, board):
        """
        Проверяет, возможна ли рокировка для короля.

        :param start: Кортеж (x, y) начальной позиции короля.
        :param end: Кортеж (x, y) конечной позиции короля.
        :param board: Объект доски.
        :return: True, если рокировка возможна, иначе False.
        """
        x1, y1 = start
        x2, y2 = end
        # Король не должен находиться под шахом
        if board.is_in_check(self.color):
            return False
        # Определяем направление рокировки
        direction = 1 if y2 > y1 else -1
        # Проверяем, свободен ли путь
        y = y1 + direction
        while y != y2:
            if board.get_piece(x1, y):
                return False
            y += direction
        # Проверяем, что ладья не двигалась
        rook_x, rook_y = x1, 7 if direction == 1 else 0
        rook = board.get_piece(rook_x, rook_y)
        if not isinstance(rook, Rook) or rook.color != self.color:
            return False
        return True

# Класс для шашки
class Checker(Piece):
    symbol = {
        Color.WHITE: '⛀',
        Color.BLACK: '⛂'
    }

    def is_valid_move(self, start, end, board):
        """
        Проверяет, является ли ход допустимым для шашки.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если ход допустим, иначе False.
        """
        x1, y1 = start
        x2, y2 = end
        direction = -1 if self.color == Color.WHITE else 1

        # Обычный ход шашки
        if abs(y2 - y1) == 1 and x2 == x1 + direction and not board.get_piece(x2, y2):
            return True

        # Ход с взятием
        if abs(y2 - y1) == 2 and x2 == x1 + 2 * direction:
            mid_x = x1 + direction
            mid_y = (y1 + y2) // 2
            mid_piece = board.get_piece(mid_x, mid_y)
            if mid_piece and mid_piece.color != self.color:
                return True

        return False

    def promote_to_king(self, pos, board):
        """
        Превращает шашку в дамку, когда она достигает последней горизонтали.

        :param pos: Кортеж (x, y) позиции шашки.
        :param board: Объект доски.
        """
        x, y = pos
        if (self.color == Color.WHITE and x == 0) or (self.color == Color.BLACK and x == 7):
            board.board[x][y] = CheckerKing(self.color)

# Класс для дамки (шашка, которая превратилась в дамку)
class CheckerKing(Piece):
    symbol = {
        Color.WHITE: '⛁',
        Color.BLACK: '⛃'
    }

    def is_valid_move(self, start, end, board):
        """
        Проверяет, является ли ход допустимым для дамки.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если ход допустим, иначе False.
        """
        x1, y1 = start
        x2, y2 = end

        # Дамка может ходить на любое количество клеток по диагонали
        if abs(x2 - x1) == abs(y2 - y1):
            return self.is_path_clear(start, end, board)

        return False

    def is_path_clear(self, start, end, board):
        """
        Проверяет, свободен ли путь для дамки.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :param board: Объект доски.
        :return: True, если путь свободен, иначе False.
        """
        x1, y1 = start
        x2, y2 = end

        step_x = 1 if x2 > x1 else -1
        step_y = 1 if y2 > y1 else -1

        x, y = x1 + step_x, y1 + step_y
        while x != x2 and y != y2:
            if board.get_piece(x, y):
                return False
            x += step_x
            y += step_y

        return True

# Класс для представления доски
class Board:
    def __init__(self, game_type):
        """
        Инициализирует доску 8x8 и расставляет фигуры в зависимости от типа игры.
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.game_type = game_type
        self.setup_pieces()
        self.en_passant_target = None  # Поле для взятия на проходе (для шахмат)

    def setup_pieces(self):
        """
        Расставляет фигуры на доске в зависимости от типа игры.
        """
        if self.game_type == "chess":
            # Расстановка шахматных фигур
            for i in range(8):
                self.board[6][i] = Pawn(Color.WHITE)  # Белые пешки на 6-й горизонтали
                self.board[1][i] = Pawn(Color.BLACK)  # Черные пешки на 1-й горизонтали

            pieces_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
            for i, piece in enumerate(pieces_order):
                self.board[7][i] = piece(Color.WHITE)  # Белые фигуры на 7-й горизонтали
                self.board[0][i] = piece(Color.BLACK)  # Черные фигуры на 0-й горизонтали

        elif self.game_type == "checkers":
            # Расстановка шашек
            for i in range(8):
                if i % 2 == 0:
                    self.board[5][i] = Checker(Color.WHITE)  # Белые шашки на 5-й горизонтали
                    self.board[1][i] = Checker(Color.BLACK)  # Черные шашки на 2-й горизонтали
                    self.board[7][i] = Checker(Color.WHITE)  # Белые шашки на 5-й горизонтали
                
                if i % 2 != 0:
                    self.board[6][i] = Checker(Color.WHITE)  # Белые шашки на 5-й горизонтали
                    self.board[0][i] = Checker(Color.BLACK)  # Черные шашки на 2-й горизонтали
                    self.board[2][i] = Checker(Color.BLACK)  # Белые шашки на 5-й горизонтали
            

    def display(self):
        """
        Отображает текущее состояние доски с координатами.
        """
        print("   a b c d e f g h")
        print(" +-----------------+")
        for i, row in enumerate(self.board):
            print(f"{8 - i}|", end=" ")
            for piece in row:
                print(str(piece) if piece else '_', end=" ")
            print(f"|{8 - i}")
        print(" +-----------------+")
        print("   a b c d e f g h")

    def get_piece(self, x, y):
        """
        Возвращает фигуру, находящуюся на указанных координатах.

        :param x: Номер строки (0-7).
        :param y: Номер столбца (0-7).
        :return: Фигура или None, если клетка пуста.
        """
        return self.board[x][y]

    def move_piece(self, start, end):
        """
        Перемещает фигуру с начальной позиции на конечную.

        :param start: Кортеж (x, y) начальной позиции.
        :param end: Кортеж (x, y) конечной позиции.
        :return: True, если ход выполнен успешно, иначе False.
        """
        x1, y1 = start
        x2, y2 = end
        piece = self.board[x1][y1]
        if piece:
            self.board[x2][y2] = piece
            self.board[x1][y1] = None
            # Превращение пешки в ферзя (для шахмат)
            if isinstance(piece, Pawn) and (x2 == 0 or x2 == 7):
                self.promote_pawn((x2, y2))
            # Превращение шашки в дамку (для шашек)
            if isinstance(piece, Checker) and (x2 == 0 or x2 == 7):
                piece.promote_to_king((x2, y2), self)
            return True
        return False

    def promote_pawn(self, pos):
        """
        Превращает пешку в выбранную фигуру, когда она достигает последней горизонтали.

        :param pos: Кортеж (x, y) позиции пешки.
        """
        x, y = pos
        pawn = self.board[x][y]
        if not isinstance(pawn, Pawn):
            return
        color = pawn.color
        # Выбор фигуры для превращения
        print("Выберите фигуру для превращения пешки:")
        print("1. Ферзь (Q)")
        print("2. Ладья (R)")
        print("3. Слон (B)")
        print("4. Конь (N)")
        choice = input("Введите номер (1-4): ")
        if choice == '1':
            self.board[x][y] = Queen(color)
        elif choice == '2':
            self.board[x][y] = Rook(color)
        elif choice == '3':
            self.board[x][y] = Bishop(color)
        elif choice == '4':
            self.board[x][y] = Knight(color)
        else:
            print("Неверный выбор. Пешка превращена в ферзя по умолчанию.")
            self.board[x][y] = Queen(color)

    def is_in_check(self, color):
        """
        Проверяет, находится ли король указанного цвета под шахом.

        :param color: Цвет короля (Color.WHITE или Color.BLACK).
        :return: True, если король под шахом, иначе False.
        """
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        x, y = king_pos
        # Проверка всех фигур противника
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece and piece.color != color and piece.is_valid_move((i, j), (x, y), self):
                    return True
        return False

    def find_king(self, color):
        """
        Находит позицию короля указанного цвета на доске.

        :param color: Цвет короля (Color.WHITE или Color.BLACK).
        :return: Кортеж (x, y) позиции короля или None, если король не найден.
        """
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if isinstance(piece, King) and piece.color == color:
                    return (i, j)
        return None

    def is_checkmate(self, color):
        """
        Проверяет, является ли текущая позиция матом для короля указанного цвета.

        :param color: Цвет короля (Color.WHITE или Color.BLACK).
        :return: True, если мат, иначе False.
        """
        if not self.is_in_check(color):
            return False
        # Проверка всех возможных ходов
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece and piece.color == color:
                    for x in range(8):
                        for y in range(8):
                            if piece.is_valid_move((i, j), (x, y), self):
                                # Пробуем сделать ход
                                temp = self.board[x][y]
                                self.board[x][y] = piece
                                self.board[i][j] = None
                                if not self.is_in_check(color):
                                    # Отменяем ход
                                    self.board[i][j] = piece
                                    self.board[x][y] = temp
                                    return False
                                # Отменяем ход
                                self.board[i][j] = piece
                                self.board[x][y] = temp
        return True

# Базовый класс игры
class Game:
    def __init__(self, game_type):
        """
        Инициализирует игру, создавая доску и устанавливая текущий ход белых.
        """
        self.board = Board(game_type)
        self.current_turn = Color.WHITE

    def play(self):
        """
        Основной цикл игры, где игроки поочередно делают ходы.
        """
        while True:
            self.board.display()
            print(f"Ход {'белых' if self.current_turn == Color.WHITE else 'черных'}")
            if self.board.is_in_check(self.current_turn):
                print("ШАХ!")
                if self.board.is_checkmate(self.current_turn):
                    print("МАТ! Игра окончена.")
                    break
            move = input("Введите ваш ход (например, 'e2 e4'): ")
            if self.make_move(move):
                self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
            else:
                print("Некорректный ход, попробуйте снова.")

    def make_move(self, move):
        """
        Выполняет ход, если он допустим.

        :param move: Строка с ходом в формате "e2 e4".
        :return: True, если ход выполнен успешно, иначе False.
        """
        try:
            start, end = move.split()
            x1, y1 = self.parse_position(start)
            x2, y2 = self.parse_position(end)
            piece = self.board.get_piece(x1, y1)
            if piece and piece.color == self.current_turn and piece.is_valid_move((x1, y1), (x2, y2), self.board):
                # Выполняем рокировку
                if isinstance(piece, King) and abs(y2 - y1) == 2:
                    self.castle((x1, y1), (x2, y2))
                # Выполняем взятие на проходе
                elif isinstance(piece, Pawn) and (x2, y2) == self.board.en_passant_target:
                    self.en_passant((x1, y1), (x2, y2))
                else:
                    self.board.move_piece((x1, y1), (x2, y2))
                return True
            return False
        except:
            return False

    def castle(self, start, end):
        """
        Выполняет рокировку.

        :param start: Кортеж (x, y) начальной позиции короля.
        :param end: Кортеж (x, y) конечной позиции короля.
        """
        x1, y1 = start
        x2, y2 = end
        direction = 1 if y2 > y1 else -1
        # Перемещаем короля
        self.board.move_piece((x1, y1), (x2, y2))
        # Перемещаем ладью
        rook_x, rook_y = x1, 7 if direction == 1 else 0
        rook_new_y = y2 - direction
        self.board.move_piece((rook_x, rook_y), (x1, rook_new_y))

    def en_passant(self, start, end):
        """
        Выполняет взятие на проходе.

        :param start: Кортеж (x, y) начальной позиции пешки.
        :param end: Кортеж (x, y) конечной позиции пешки.
        """
        x1, y1 = start
        x2, y2 = end
        # Перемещаем пешку
        self.board.move_piece((x1, y1), (x2, y2))
        # Убираем пешку противника
        captured_pawn_x = x1
        captured_pawn_y = y2
        self.board.board[captured_pawn_x][captured_pawn_y] = None

    def parse_position(self, pos):
        """
        Преобразует шахматную нотацию (например, "e2") в координаты доски (x, y).

        :param pos: Строка с позицией в шахматной нотации (например, "e2").
        :return: Кортеж (x, y) координат доски.
        """
        x = 8 - int(pos[1])
        y = ord(pos[0]) - ord('a')
        return x, y

# Класс для шахмат
class ChessGame(Game):
    def __init__(self):
        super().__init__("chess")

# Класс для шашек
class CheckersGame(Game):
    def __init__(self):
        super().__init__("checkers")

# Запуск игры
if __name__ == "__main__":
    print("Выберите игру:")
    print("1. Шахматы")
    print("2. Шашки")
    choice = input("Введите номер (1 или 2): ")

    if choice == '1':
        game = ChessGame()
    elif choice == '2':
        game = CheckersGame()
    else:
        print("Неверный выбор. Запускаются шахматы по умолчанию.")
        game = ChessGame()

    game.play()
