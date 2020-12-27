import pygame
from pygame import color
from constants import NO_OF_ROWS, NO_OF_COLS, CUBE_SIZE, WIDTH, HEIGHT
from constants import BLACK, WHITE, RED, BLUE

b_pawn = pygame.transform.scale2x(pygame.image.load("./images/black_pawn.png"))
b_rook = pygame.transform.scale2x(pygame.image.load("./images/black_rook.png"))
b_knight = pygame.transform.scale2x(pygame.image.load("./images/black_knight.png"))
b_bishop = pygame.transform.scale2x(pygame.image.load("./images/black_bishop.png"))
b_queen = pygame.transform.scale2x(pygame.image.load("./images/black_queen.png"))
b_king = pygame.transform.scale2x(pygame.image.load("./images/black_king.png"))

w_pawn = pygame.transform.scale2x(pygame.image.load("./images/white_pawn.png"))
w_rook = pygame.transform.scale2x(pygame.image.load("./images/white_rook.png"))
w_knight = pygame.transform.scale2x(pygame.image.load("./images/white_knight.png"))
w_bishop = pygame.transform.scale2x(pygame.image.load("./images/white_bishop.png"))
w_queen = pygame.transform.scale2x(pygame.image.load("./images/white_queen.png"))
w_king = pygame.transform.scale2x(pygame.image.load("./images/white_king.png"))

class Piece:
    def __init__(self, screen, row, col, color):
        self.screen = screen
        self.row = row
        self.col = col
        self.color = color.lower()
        self.selected = False
        self.set_image()
        self.moves = []
        self.is_under_check = False

    def draw(self):
        x = (self.col * CUBE_SIZE) + (CUBE_SIZE // 2) - (self.piece_img.get_width() // 2)
        y = (self.row * CUBE_SIZE) + (CUBE_SIZE // 2) - (self.piece_img.get_height() // 2)

        self.screen.blit(self.piece_img, (x, y))

        x = self.col * CUBE_SIZE
        y = self.row * CUBE_SIZE
            
        if self.selected:
            pygame.draw.rect(self.screen, BLUE, (x, y, CUBE_SIZE, CUBE_SIZE), 3)

        if isinstance(self, King) and self.is_under_attack:
            pygame.draw.rect(self.screen, RED, (x, y, CUBE_SIZE, CUBE_SIZE), 5)
          
    def update_valid_moves(self, board):
        self.moves = self.valid_moves(board)

        new_board = board[:]
        valid_moves = []

        for move in self.moves:
            i, j = move
            cur = new_board[self.row][self.col]
            new_board[self.row][self.col] = 0
            whatever = new_board[i][j]
            new_board[i][j] = cur

            if not self.is_check(self.color, new_board):
                valid_moves.append(move)
            new_board[self.row][self.col] = cur
            new_board[i][j] = whatever
        
        self.moves = valid_moves


    def update_pos(self, pos):
        self.row, self.col = pos

    def is_selected(self):
        return self.selected

    def is_check(self, color, board=None):
        king_pos = (-1, -1)
        king = 0
        enemy_moves = []
        # TODO CHNAGES NEEDED
        for row in board:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    king_pos = piece.row, piece.col
                    king = board[piece.row][piece.col]
                if piece != 0 and piece.color != color:
                    enemy_moves.extend(piece.moves)

        for pos in enemy_moves:
            if pos == king_pos:
                #king.is_under_attack = True
                return True
        return False
    

class Pawn(Piece):

    # def __init__(self, screen, row, col, color):
    #     super().__init__(screen, row, col, color)
    #     self.yet_to_move = True

    def set_image(self):
        if self.color == "black":
            self.piece_img = b_pawn
        else:
            self.piece_img = w_pawn
    
    def valid_moves(self, board):
        moves = []
        i, j = self.row, self.col

        if self.color == "white":
            if i > 0:
                # forward by one
                if board[i - 1][j] == 0:
                    moves.append((i - 1, j))
                    # forward by two, only when it hasn't been moved and its front is empty
                    if i - 2 >= 0 and board[i - 2][j] == 0 and i == 6:
                        moves.append((i - 2, j))
                # left diag
                if j - 1 >= 0 and board[i - 1][j - 1] != 0 and board[i - 1][j - 1].color != "white":
                    moves.append((i - 1, j - 1))
                # right diag
                if j + 1 < NO_OF_COLS and board[i - 1][j + 1] != 0 and board[i - 1][j + 1].color != "white":
                    moves.append((i - 1, j + 1))

        # black
        else:
            if i < 7:
                # forward by one
                if board[i + 1][j] == 0:
                    moves.append((i + 1, j))
                    # forward by two only when +1 is empty
                    if i == 1 and board[i + 2][j] == 0:
                        moves.append((i + 2, j))
                # left diag
                if j + 1 < NO_OF_COLS and board[i + 1][j + 1] != 0 and board[i + 1][j + 1].color != "black":
                    moves.append((i + 1, j + 1))
                # right diag
                if j - 1 >= 0 and board[i + 1][j - 1] != 0 and board[i + 1][j - 1].color != "black":
                    moves.append((i + 1, j - 1))

        return moves

class King(Piece):
    def set_image(self):
        self.is_under_attack = False
        if self.color == "black":
            self.piece_img = b_king
        else:
            self.piece_img = w_king
    
    def valid_moves(self, board):
        moves = []
        i, j = self.row, self.col
        cur = board[i][j]

        # left
        if j - 1 >= 0 and (board[i][j - 1] == 0 or (board[i][j - 1].color != cur.color)):
            moves.append((i, j - 1))

        # top 
        if i - 1 >= 0:
            # top left
            if j - 1 >= 0 and (board[i - 1][j - 1] == 0 or (board[i - 1][j - 1].color != cur.color)):
                moves.append((i - 1, j - 1))

            # UP
            if board[i - 1][j] == 0 or board[i - 1][j].color != cur.color:
                moves.append((i - 1, j))

            # top right
            if j + 1 < NO_OF_COLS and (board[i - 1][j + 1] == 0 or (board[i - 1][j + 1].color != cur.color)):
                moves.append((i - 1, j + 1))

        if j + 1 < NO_OF_COLS:
            # down right
            if i + 1 < NO_OF_ROWS and (board[i + 1][j + 1] == 0 or board[i + 1][j + 1].color != cur.color):
                moves.append((i + 1, j + 1))

            #right
            if board[i][j + 1] == 0 or (board[i][j + 1].color != cur.color):
                moves.append((i, j + 1))
            
        # down
        if i + 1 < NO_OF_ROWS:
            # down
            if board[i + 1][j] == 0 or board[i + 1][j].color != cur.color:
                moves.append((i  + 1, j))

            # down left
            if j - 1 >= 0 and (board[i + 1][j - 1] == 0 or board[i + 1][j - 1].color != cur.color):
                moves.append((i + 1, j - 1))
        
        return moves

class Queen(Piece):
    def set_image(self):
        if self.color == "black":
            self.piece_img = b_queen
        else:
            self.piece_img = w_queen
    
    def valid_moves(self, board):
        moves = []
        i, j = self.row, self.col
        cur = board[i][j]

        #ROOK
        for x in range(i - 1, -1, -1):
            # add all the empty cells
            while x >= 0 and board[x][j] == 0:
                moves.append((x, j))
                x -= 1
            
            if x >= 0:
                # kill the first enemy and break
                if board[x][j].color != cur.color:
                    moves.append((x, j))
                break
            
        # down
        for x in range(i + 1, NO_OF_ROWS, 1):
            while x < NO_OF_ROWS and board[x][j] == 0:
                moves.append((x, j))
                x += 1

            if x < NO_OF_ROWS:
                if board[x][j].color != cur.color:
                    moves.append((x, j))
                break
        # left
        for x in range(j - 1, -1, -1):
            while x >= 0 and board[i][x] == 0:
                moves.append((i, x))
                x -= 1
            
            if x >= 0:
                if board[i][x].color != cur.color:
                    moves.append((i, x))
                break
        # right
        for x in range(j + 1, NO_OF_COLS, 1):
            while x < NO_OF_COLS and board[i][x] == 0:
                moves.append((i, x))
                x += 1
            
            if x < NO_OF_COLS:
                if board[i][x].color != cur.color:
                    moves.append((i, x))
                break

        # BISHOP
        # top left diag
        x, y = i - 1, j - 1
        while x >= 0 and y >= 0 and board[x][y] == 0:
            moves.append((x, y))
            x -= 1
            y -= 1
        
        if x >= 0 and y >= 0 and board[x][y].color != cur.color:
            moves.append((x, y))
        
        # top right diag
        x, y = i - 1, j + 1
        while x >= 0 and y < NO_OF_COLS and board[x][y] == 0:
            moves.append((x, y))
            x -= 1
            y += 1
        
        if x >= 0 and y < NO_OF_COLS and board[x][y].color != cur.color:
            moves.append((x, y))
            x -= 1
            y += 1

        # bottom left diag
        x, y = i + 1, j - 1
        while x < NO_OF_ROWS and y >= 0 and board[x][y] == 0:
            moves.append((x, y))
            x += 1
            y -= 1

        if x < NO_OF_ROWS and y >= 0 and board[x][y].color != cur.color:
            moves.append((x, y))
        
        # bottom right diag
        x, y = i + 1, j + 1
        while x < NO_OF_ROWS and y < NO_OF_COLS and board[x][y] == 0:
            moves.append((x, y))
            x += 1
            y += 1

        if x < NO_OF_ROWS and y < NO_OF_COLS and board[x][y].color != cur.color:
            moves.append((x, y))
            
        return moves

class Rook(Piece):
    def set_image(self):
        if self.color == "black":
            self.piece_img = b_rook
        else:
            self.piece_img = w_rook
    
    def valid_moves(self, board):
        moves = []
        i, j = self.row, self.col
        cur = board[i][j]
        # careful, have to break quite early
        # up
        for x in range(i - 1, -1, -1):
            # add all the empty cells
            while x >= 0 and board[x][j] == 0:
                moves.append((x, j))
                x -= 1
            
            if x >= 0:
                # kill the first enemy and break
                if board[x][j].color != cur.color:
                    moves.append((x, j))
                break
            
        # down
        for x in range(i + 1, NO_OF_ROWS, 1):
            while x < NO_OF_ROWS and board[x][j] == 0:
                moves.append((x, j))
                x += 1

            if x < NO_OF_ROWS:
                if board[x][j].color != cur.color:
                    moves.append((x, j))
                break
        # left
        for x in range(j - 1, -1, -1):
            while x >= 0 and board[i][x] == 0:
                moves.append((i, x))
                x -= 1
            
            if x >= 0:
                if board[i][x].color != cur.color:
                    moves.append((i, x))
                break
        # right
        for x in range(j + 1, NO_OF_COLS, 1):
            while x < NO_OF_COLS and board[i][x] == 0:
                moves.append((i, x))
                x += 1
            
            if x < NO_OF_COLS:
                if board[i][x].color != cur.color:
                    moves.append((i, x))
                break

        return moves

class Knight(Piece):
    def set_image(self):
        if self.color == "black":
            self.piece_img = b_knight
        else:
            self.piece_img = w_knight
    
    def valid_moves(self, board):
        moves = []
        i, j = self.row, self.col
        cur = board[i][j]

        if i + 1 < NO_OF_ROWS:
            if j + 2 < NO_OF_COLS and (board[i + 1][j + 2] == 0 or board[i + 1][j + 2].color != cur.color):
                moves.append((i + 1, j + 2))
            if j - 2 >= 0 and (board[i + 1][j - 2] == 0 or board[i + 1][j - 2].color != cur.color):
                moves.append((i + 1 , j - 2))
        
        if i + 2 < NO_OF_ROWS:
            if j - 1 >= 0 and (board[i + 2][j -  1] == 0 or board[i + 2][j - 1].color != cur.color):
                moves.append((i + 2, j - 1))
            if j + 1 < NO_OF_COLS and (board[i + 2][j + 1] == 0 or board[i + 2][j + 1].color != cur.color):
                moves.append((i + 2, j + 1))

        if i - 1 >= 0:
            if j + 2 < NO_OF_COLS and (board[i - 1][j + 2] == 0 or board[i - 1][j + 2].color != cur.color):
                moves.append((i - 1, j + 2))
            if j - 2 >= 0 and (board[i - 1][j - 2] == 0 or board[i - 1][j - 2].color != cur.color):
                moves.append((i - 1 , j - 2))
        
        if i - 2 >= 0:
            if j - 1 >= 0 and (board[i - 2][j -  1] == 0 or board[i - 2][j - 1].color != cur.color):
                moves.append((i - 2, j - 1))
            if j + 1 < NO_OF_COLS and (board[i - 2][j + 1] == 0 or board[i - 2][j + 1].color != cur.color):
                moves.append((i - 2, j + 1))

        return moves

class Bishop(Piece):
    def set_image(self):
        if self.color == "black":
            self.piece_img = b_bishop
        else:
            self.piece_img = w_bishop
    
    def valid_moves(self, board):
        moves = []
        i, j = self.row, self.col
        cur = board[i][j]

        # top left diag
        x, y = i - 1, j - 1
        while x >= 0 and y >= 0 and board[x][y] == 0:
            moves.append((x, y))
            x -= 1
            y -= 1
        
        if x >= 0 and y >= 0 and board[x][y].color != cur.color:
            moves.append((x, y))
        
        # top right diag
        x, y = i - 1, j + 1
        while x >= 0 and y < NO_OF_COLS and board[x][y] == 0:
            moves.append((x, y))
            x -= 1
            y += 1
        
        if x >= 0 and y < NO_OF_COLS and board[x][y].color != cur.color:
            moves.append((x, y))
            x -= 1
            y += 1

        # bottom left diag
        x, y = i + 1, j - 1
        while x < NO_OF_ROWS and y >= 0 and board[x][y] == 0:
            moves.append((x, y))
            x += 1
            y -= 1

        if x < NO_OF_ROWS and y >= 0 and board[x][y].color != cur.color:
            moves.append((x, y))
        
        # bottom right diag
        x, y = i + 1, j + 1
        while x < NO_OF_ROWS and y < NO_OF_COLS and board[x][y] == 0:
            moves.append((x, y))
            x += 1
            y += 1

        if x < NO_OF_ROWS and y < NO_OF_COLS and board[x][y].color != cur.color:
            moves.append((x, y))

        return moves