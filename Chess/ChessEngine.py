"""
This class is responsible for storing all the information about the current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""


class GameState():
    def __init__(self):
        # Board is 8x8 2d list, each element of the list has 2 characters.
        # First character- color of piece, 'b' for black, 'w' for white
        # Second Character- type of piece, 'K'=King,'Q'=Queen,...etc.
        # "--" represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "wR", "--", "--", "bB", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, "K": self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players

    '''
    undo the last move made
    '''

    def undoMove(self):
        if len(self.moveLog) != 0:  # there is move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    '''
    All moves considering checks
    '''

    def getValidMoves(self):
        return self.getAllPossibleMoves()  # for now we will not worry about checks
        pass

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # alls the appropriate move funciton based on piece types
        return moves

    '''
    Get all the pawn moves for the pawn located at (r,c), and add moves to list
    '''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves
            if self.board[r - 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # captures left diagonal
                if self.board[r - 1][c - 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # captures right diagonal
                if self.board[r - 1][c + 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:  # black pawn moves
            if self.board[r + 1][c] == "--":  # 1 square move
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))  # 2 square move
            # captures
            if c - 1 >= 0:  # capture to the left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # capture to the right
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    '''
    Get all the Rook moves for the rook located at row, col and add these moves to the list
    '''

    def getRookMoves(self, r, c, moves):
        if self.whiteToMove:  # white rook moves
            for j in range(c + 1, len(self.board[r])):  # check right
                if self.board[r][j] != "--":  # if space not empty break for loop
                    if self.board[r][j][0] == 'b':  # if black piece blocking, capture, else, break
                        print("ADDED CAPTURE PIECE ROOK")
                        moves.append(Move((r, c), (r, j), self.board))
                    break
                moves.append(Move((r, c), (r, j), self.board))

            for j in range(c-1, -1, -1):  # check left
                if self.board[r][j] != "--":
                    if self.board[r][j][0] == 'b':
                        moves.append(Move((r, c), (r, j), self.board))
                    break
                moves.append(Move((r, c), (r, j), self.board))

            for i in range(r + 1, len(self.board)):  # check below
                if self.board[i][c] != "--":
                    if self.board[i][c][0] == 'b':
                        moves.append(Move((r, c), (i, c), self.board))
                    break
                moves.append(Move((r, c), (i, c), self.board))

            for i in range(r-1, -1, -1):  # check above
                if self.board[i][c] != "--":
                    if self.board[i][c][0] == 'b':
                        moves.append(Move((r, c), (i, c), self.board))
                    break
                moves.append(Move((r, c), (i, c), self.board))
        else: #black rook moves
            for j in range(c + 1, len(self.board[r])):  # check right
                if self.board[r][j] != "--":  # if space not empty break for loop
                    if self.board[r][j][0] == 'w':  # if white piece blocking, capture, else, break
                        print("ADDED CAPTURE PIECE ROOK")
                        moves.append(Move((r, c), (r, j), self.board))
                    break
                moves.append(Move((r, c), (r, j), self.board))

            for j in range(c-1, -1, -1):  # check left
                if self.board[r][j] != "--":
                    if self.board[r][j][0] == 'w':
                        moves.append(Move((r, c), (r, j), self.board))
                    break
                moves.append(Move((r, c), (r, j), self.board))

            for i in range(r + 1, len(self.board)):  # check below
                if self.board[i][c] != "--":
                    if self.board[i][c][0] == 'w':
                        moves.append(Move((r, c), (i, c), self.board))
                    break
                moves.append(Move((r, c), (i, c), self.board))

            for i in range(r-1, -1, -1):  # check above
                if self.board[i][c] != "--":
                    if self.board[i][c][0] == 'w':
                        moves.append(Move((r, c), (i, c), self.board))
                    break
                moves.append(Move((r, c), (i, c), self.board))

    '''
        Get all the Knight moves for the rook located at row, col adn add these moves to the list
        '''

    def getKnightMoves(self, r, c, moves):
        pass

    '''
        Get all the Bishop moves for the rook located at row, col adn add these moves to the list
        '''

    def getBishopMoves(self, r, c, moves):
        pass

    '''
        Get all the Queen moves for the rook located at row, col adn add these moves to the list
        '''

    def getQueenMoves(self, r, c, moves):
        pass

    '''
        Get all the King moves for the rook located at row, col adn add these moves to the list
        '''

    def getKingMoves(self, r, c, moves):
        pass


class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}  # reverses dictionary
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # change to make it more chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
