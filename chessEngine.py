class pieces():
    NONE = 0
    KING = 100000000
    QUEEN = 9
    ROOK = 5
    BISHOP = 3
    KNIGHT = 3
    PAWN = 1
     
class game_state():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['__', '__', '__', '__', '__', '__', '__', '__'],
            ['__', '__', '__', '__', '__', '__', '__', '__'],
            ['__', '__', '__', '__', '__', '__', '__', '__'],
            ['__', '__', '__', '__', '__', '__', '__', '__'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

        self.moveFunctions = {'p': self.getPawnMoves,
                            'R': self.getRookMoves,
                            'N': self.getKnightMoves,
                            'B': self.getBishopMoves,
                            'Q': self.getQueenMoves,
                            'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.bKingPos = (0, 4)
        self.wKingPos = (7, 4)
        self.wInCheck = False
        self.bInCheck = False
        self.pins = []
        self.checks = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '__'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        piece = move.pieceMoved[-1]
        next_moves = []
        self.moveFunctions[piece](move.endRow, move.endCol, next_moves)

        # update king's position if moved
        if piece == 'K':
            if self.whiteToMove:
                self.wKingPos = (move.endRow, move.endCol)
            else:
                self.bKingPos = (move.endRow, move.endCol)
        
        # check if king can be captured in the next move by the piece moved
        for m in next_moves:
            if self.whiteToMove:
                # print(m.endRow, m.endCol)
                if (m.endRow, m.endCol) == self.bKingPos:
                    print("Check!")
                    self.bInCheck = True
            
            else:
                if (m.endRow, m.endCol) == self.wKingPos:
                    print("Check!")
                    self.wInCheck = True

        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            piece = move.pieceMoved[-1]
            # update king's position if moved
            if piece == 'K':
                if self.whiteToMove:
                    self.wKingPos = (move.endRow, move.endCol)
                else:
                    self.bKingPos = (move.endRow, move.endCol)

    def getMovesInCheck(self, moves):
         # removing moves which doesn't block check or moves away from check
        #  for m in moves:

        pass
    
    def getAllPossibleMoves(self):
        moves = []
        # parse the board and then generate all the valid moves for the available pieces
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][-1]
                    self.moveFunctions[piece](r, c, moves)
        
        if self.bInCheck or self.wInCheck:
            self.getMovesInCheck(moves)

        return moves

 # Generating all pawn moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == '__':
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r-2][c] == '__':
                    moves.append(Move((r, c), (r - 2, c), self.board))
            
            if c - 1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))

            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        
        else:
            if self.board[r+1][c] == '__':
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r+2][c] == '__':
                    moves.append(Move((r, c), (r + 2, c), self.board))
            
            if c - 1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))

            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

 # Generating all rook moves

    def getRookMoves(self, r, c, moves):
        if self.whiteToMove:
            own_color = 'w'
            enemy_color = 'b'

        else:
            own_color = 'b'
            enemy_color = 'w'

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)] # up, left, down, right

        for d in directions:
            for i in range(1, 8):
                pos_r = r + d[0] * i
                pos_c = c + d[1] * i

                if 0 <= pos_r <= 7 and 0 <= pos_c <= 7:
                    if self.board[pos_r][pos_c][0] == enemy_color:
                        moves.append(Move((r, c), (pos_r, pos_c), self.board))
                        break
            
                    elif self.board[pos_r][pos_c][0] == own_color:
                        break

                    else:
                        moves.append(Move((r, c), (pos_r, pos_c), self.board))

                else:
                    break


 # Generating all knight moves

    def getKnightMoves(self, r, c, moves):
        if self.whiteToMove:
            own_color = 'w'
            enemy_color = 'b'

        else:
            own_color = 'b'
            enemy_color = 'w'

        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for m in knightMoves:
            pos_r = r + m[0]
            pos_c = c + m[1]

            if 0 <= pos_r <= 7 and 0 <= pos_c <= 7:
                if self.board[pos_r][pos_c][0] != own_color:
                    moves.append(Move((r, c), (pos_r, pos_c), self.board))

 # Generating all bishop moves

    def getBishopMoves(self, r, c, moves):
        if self.whiteToMove:
            own_color = 'w'
            enemy_color = 'b'

        else:
            own_color = 'b'
            enemy_color = 'w'
        
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # 4 diagonals

        for d in directions:
            for i in range(1, 8):
                pos_r = r + d[0] * i
                pos_c = c + d[1] * i

                if 0 <= pos_r <= 7 and 0 <= pos_c <= 7:
                    if self.board[pos_r][pos_c][0] == enemy_color:
                        moves.append(Move((r, c), (pos_r, pos_c), self.board))
                        break
            
                    elif self.board[pos_r][pos_c][0] == own_color:
                        break

                    else:
                        moves.append(Move((r, c), (pos_r, pos_c), self.board))

                else:
                    break

 # Generating all queen moves
    
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

 # Generating all king moves

    def getKingMoves(self, r, c, moves):
        if self.whiteToMove:
            own_color = 'w'
            enemy_color = 'b'

        else:
            own_color = 'b'
            enemy_color = 'w'

        kingMoves = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] # up, left, down, right and the 4 diagonals
        
        for m in kingMoves:
            pos_r = r + m[0]
            pos_c = c + m[1]

            if 0 <= pos_r <= 7 and 0 <= pos_c <= 7:
                if self.board[pos_r][pos_c][0] != own_color:
                    moves.append(Move((r, c), (pos_r, pos_c), self.board))
        

class Move():

    ranksToRows = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}

    filesToCols = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        
        return False
    
    def getChessNotation(self):
        notation = ''
        if(self.pieceMoved[-1] != 'p'):
            notation = self.pieceMoved[-1]
        notation += (self.colsToFiles[self.endCol] + self.rowsToRanks[self.endRow])

        return notation