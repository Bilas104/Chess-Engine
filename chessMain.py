import pygame as p
import chessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8

SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
images = {}

def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']

    for piece in pieces:
        filename = (r"C:\Users\Bilas\vscode\Projects\Chess Engine\Chess Pieces\\" + piece + r".png")
        images[piece] = p.transform.scale(p.image.load(filename), (SQ_SIZE, SQ_SIZE))
    # images['light_sq'] = p.transform.scale(p.image.load(r"C:\Users\Bilas\vscode\Projects\Chess Engine\Chess Pieces\light_brown.png"), (SQ_SIZE, SQ_SIZE))
    # images['dark_sq'] = p.transform.scale(p.image.load(r"C:\Users\Bilas\vscode\Projects\Chess Engine\Chess Pieces\dark_brown.png"), (SQ_SIZE, SQ_SIZE))

def draw_board(screen):
    colors = [p.Color("floralwhite"), p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '__':
                screen.blit(images[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)

def squareHighlight(screen, r, c, piece, checked):
    # if king is in check highlight it with red
    if checked == True:
        highlight_color = p.Color("firebrick1")
        p.draw.rect(screen, highlight_color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        screen.blit(images[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # highlighting the clicked piece
    else:
        highlight_color = p.Color("lightblue")
        p.draw.rect(screen, highlight_color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        screen.blit(images[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = chessEngine.game_state()
    load_images()
    validMoves = gs.getAllPossibleMoves()
    moveMade = False
    running_status = True
    sqSelected = () # keep track of last user click (tuple : (row, col))
    playerClicks = [] # we will store the tuples of last two valid user clicks so a move can be made

    while(running_status):
        for e in p.event.get():
            if e.type == p.QUIT:
                running_status = False
            
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                row = location[1]//SQ_SIZE
                col = location[0]//SQ_SIZE

                if sqSelected == (row, col): # deselect operation
                    sqSelected = ()
                    playerClicks = []

                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                    if len(playerClicks) == 1 and gs.board[row][col] == '__':
                        sqSelected = ()
                        playerClicks = []

                    if len(playerClicks) == 2:
                        move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                            print(move.getChessNotation())
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected] # fix : wrong notation still getting printed

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when z is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getAllPossibleMoves()
            moveMade = False

        draw_game_state(screen, gs)
        if len(playerClicks) == 1:
            squareHighlight(screen, playerClicks[0][0], playerClicks[0][1], gs.board[playerClicks[0][0]][playerClicks[0][1]], False)
        if gs.bInCheck == True:
            squareHighlight(screen, gs.bKingPos[0], gs.bKingPos[1], 'bK', True)
        if gs.wInCheck == True:
            squareHighlight(screen, gs.wKingPos[0], gs.wKingPos[1], 'wK', True)
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()