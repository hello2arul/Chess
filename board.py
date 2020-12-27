import pygame
import sys
from tkinter import Tk, Button, OptionMenu, StringVar, messagebox
from pieces import Piece, Pawn, King, Queen, Rook, Bishop, Knight
from constants import NO_OF_ROWS, NO_OF_COLS, CUBE_SIZE, WIDTH, HEIGHT
from constants import BLACK, WHITE, RED, GREEN

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.is_whites_turn = True
        self.board = [[0 for j in range(NO_OF_COLS)] for i in range(NO_OF_ROWS)]

        self.board[0][0] = Rook(screen, 0, 0, "black")
        self.board[0][1] = Knight(screen, 0, 1, "black")
        self.board[0][2] = Bishop(screen, 0, 2, "black")
        self.board[0][3] = Queen(screen, 0, 3, "black")
        self.board[0][4] = King(screen, 0, 4, "black")
        self.board[0][5] = Bishop(screen, 0, 5, "black")
        self.board[0][6] = Knight(screen, 0, 6, "black")
        self.board[0][7] = Rook(screen, 0, 7, "black")

        self.board[7][0] = Rook(screen, 7, 0, "white")
        self.board[7][1] = Knight(screen, 7, 1, "white")
        self.board[7][2] = Bishop(screen, 7, 2, "white")
        self.board[7][3] = Queen(screen, 7, 3, "white")
        self.board[7][4] = King(screen, 7, 4, "white")
        self.board[7][5] = Bishop(screen, 7, 5, "white")
        self.board[7][6] = Knight(screen, 7, 6, "white")
        self.board[7][7] = Rook(screen, 7, 7, "white")

        for j in range(NO_OF_COLS):
            self.board[1][j] = Pawn(screen, 1, j, "black")

        for j in range(NO_OF_COLS):
            self.board[6][j] = Pawn(screen, 6, j, "white")

        self.to_highlight = []


    def draw(self):
        self.screen.fill(BLACK)
        for i in range(NO_OF_ROWS):
            for j in range(i % 2, NO_OF_COLS, 2):  
                pygame.draw.rect(self.screen, WHITE, (i * CUBE_SIZE, j * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE))
        
        for pos in self.to_highlight:
            x = pos[1] * CUBE_SIZE
            y = pos[0] * CUBE_SIZE
            pygame.draw.rect(self.screen, GREEN, (x, y, CUBE_SIZE, CUBE_SIZE), 3)
            
        for row in self.board:
            for piece in row:
                if isinstance(piece, Piece):
                    piece.draw()
    
    def select(self, i, j):
        prev = (-1, -1)
        cur = self.board[i][j]
        changed = False
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.selected:
                    prev = (piece.row, piece.col)
           
        # if new pos is empty and a piece was already selected or new pos is an enemy
        if prev != (-1, -1) and (cur == 0 or self.board[prev[0]][prev[1]].color != cur.color):
            valid_moves = self.board[prev[0]][prev[1]].moves
            if (i, j) in valid_moves:
                changed = self.move(prev, (i, j))
                # switching between diff colors
                if not changed:
                    self.make_selected((i, j))

            # switching between different colors
            elif cur != 0:
                self.make_selected((i, j))
        elif prev == (i, j):
            self.reset_selected()
        else:
            # selecting a new piece
            if prev == (-1, -1) :
                self.make_selected((i, j))
            else:
                # switching between same colors
                    self.make_selected((i, j))   
        # if changed to a new pos reset selected
        if changed:
            self.reset_selected()
            color = "white" if self.board[i][j].color == "black" else "black"

            if self.is_under_check(color):
                print("check")
                self.update_moves()
                cur = self.board[i][j]
                danger_moves = cur.moves
                # for row in self.board:
                #     for piece in row:
                #         if isinstance(piece, Piece) and piece.color == color :
                #             to_remove = []
                #             for idx, pos in enumerate(piece.moves):
                #                 if pos not in danger_moves:
                #                     to_remove.append(idx)
                #                 # king cannot move to the danger moves from a danger pos
                #                 elif isinstance(piece, King):
                #                     to_remove.append(idx)
                #             print(f"{piece.moves} , {to_remove}")
                #             for idx in reversed(to_remove):
                #                 piece.moves.pop(idx)
                            

                #self.change_check_status(color, True)
                # self.make_king_in_danger(color)
                # if self.is_checkmate(color):
                #     self.winner("black" if color == "white" else "white")
            #elif self.is_stalemate()
            else:
                self.reset_danger()

    def move(self, prev, to): 
        # prev wont be equal to to
        cur_selected = self.board[prev[0]][prev[1]]  
        # restricting movement to one player at a time
        if self.is_whites_turn and cur_selected.color != "white":
            return False
        elif not self.is_whites_turn and cur_selected.color != "black":
            return False

        cur_selected.update_pos(to)
        self.board[to[0]][to[1]] = cur_selected
        self.board[prev[0]][prev[1]] = 0

        # when pawn reaches the other end
        if isinstance(cur_selected, Pawn):
            if to[0] == 7 or to[0] == 0:
                self.board[to[0]][to[1]] = self.ask_for_pawn()(self.screen, to[0], to[1], cur_selected.color)
        
        self.is_whites_turn = not self.is_whites_turn
        return True

    def make_selected(self, pos):
        self.reset_selected()
        i, j = pos
        cur = self.board[i][j]
        if cur != 0:
            cur.selected = True
            cur.update_valid_moves(self.board)
            self.to_highlight = cur.moves
            # dont highlight if its the wrong player
            if (self.is_whites_turn and cur.color != "white") or (not self.is_whites_turn and cur.color != "black"):
                self.to_highlight = []   

    def update_moves(self):
        for row in self.board:
            for piece in row:
                if piece != 0:
                    piece.update_valid_moves(self.board) 

    def reset_selected(self):
        self.to_highlight = []
        for row in self.board:
            for piece in row:
                if piece != 0:
                    piece.selected = False

    def reset_danger(self):
        for row in self.board:
            for piece in row:
                if isinstance(piece, King):
                    piece.is_under_attack = False

    def is_under_check(self, color, board=None):
        king_pos = (-1, -1)
        king = 0
        enemy_moves = []
        if board == None:
            board = self.board

        for row in board:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    king_pos = piece.row, piece.col
                    king = self.board[piece.row][piece.col]
                elif piece != 0 and piece.color != color:
                    piece.update_valid_moves(self.board)
                    enemy_moves.extend(piece.moves)

        for pos in enemy_moves:
            if pos == king_pos:
                king.is_under_attack = True
                return True
        return False
    
    def is_checkmate(self, color):
        moves_available = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    piece.update_valid_moves(self.board)
                    moves_available.extend(piece.moves)
        
        return len(moves_available) == 0

    def change_check_status(self, color, boolean):
        for row in self.board:
            for piece in row:
                if isinstance(piece, Piece) and piece.color == color:
                    piece.is_under_check = boolean

    def ask_for_pawn(self):
        window = Tk()
        window.geometry("200x100")
        window.resizable(width=False, height=False)
        window.title("Options")

        selected = StringVar()
        options = ["Queen", "Bishop", "Rook", "Knight"]
        map = [Queen, Bishop, Rook, Knight]
        selected.set(options[0])
        drop_down = OptionMenu(window, selected, *options)
        btn = Button(window, text="Confirm", command=window.destroy)
        btn.pack()

        drop_down.pack()
        window.mainloop()
        option = selected.get()

        return map[options.index(option)]

    def winner(self, color):
        root = Tk()
        root.overrideredirect(1)
        root.withdraw()
        yes = messagebox.askokcancel(f"{color} won!", "Want to play again?")

        if yes:
            self.__init__(self.screen)
        else:
            pygame.quit()
            sys.exit()



                


        
