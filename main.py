import pygame, sys, random
from pygame.locals import *
Window_Width = 1000  # width of the main window of the game
Window_Height = 600  # height of the main window of the game
Board_Width = 5  # number of squares in each column
Board_Height = 5  # number of squares in each rows
Square_Size = 100  # size of each square in the game
Speed = 2000  # speed of moving squares
BLANK = None  # the empty square
###############################################
EFFFFF = (239, 255, 255)
White = (255,255,255)
Teal = (0,102,102)
Blue = (0,153,153)
Black = (0, 0, 0)
##############################################
Background_Color = EFFFFF
Square_Color = Blue
Text_Color = White
Border_Color = Teal
Font_Size = 20
Title_Color = Black
Button_Color= EFFFFF
##############################################
X = int((Window_Width - (Square_Size * Board_Width + (Board_Width - 1))) / 2)  # to put the window in the center
Y = int((Window_Height - (Square_Size * Board_Height + (Board_Height - 1))) / 2)  # to put the window in the center
##############################################
Up = 'up'
Down = 'down'
Left = 'left'
Right = 'right'

#_______________________________________________ Noura _____________________________________________________________
def main():
    global Speed_Clock, Display_SURF, Font, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    Speed_Clock = pygame.time.Clock()
    Display_SURF = pygame.display.set_mode((Window_Width, Window_Height))
    pygame.display.set_caption('Slide Puzzle')
    Font = pygame.font.Font('freesansbold.ttf', Font_Size)

    # Store the option buttons and their rectangles in OPTIONS.

    NEW_SURF,   NEW_RECT   = makeText('New Game', Title_Color, Button_Color, Window_Width - 120, Window_Height - 60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve',   Title_Color, Button_Color, Window_Width - 120, Window_Height - 30)
#_______________________________________________ Rania _____________________________________________________________
    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard() # a solved board is the same as the board in a start state.
    allMoves = [] # list of moves made from the solved configuration
#_____________________________________________ Hader _______________________________________________________________
    while True: # main game loop
        slideTo = None # the direction, if any, a tile should slide
        msg = 'Click tile or press arrow keys to slide.' # contains the message to show in the upper left corner.
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'

        drawBoard(mainBoard, msg)
#___________________________________________ Omnia __________________________________________________________________
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button

                    if NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80) # clicked on New Game button
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on Solve button
                        allMoves = []
                else:
                    # check if the clicked tile was next to the blank spot

                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = Left
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = Right
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = Up
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = Down


        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8) # show slide on screen
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # record the slide
        pygame.display.update()
        Speed_Clock.tick(Speed)
#___________________________________________ Rewas & Rania ___________________________________________________________

def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present

#______________________________________________ Noura___________________________________________________________________

def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(Board_Width):
        column = []
        for y in range(Board_Height):
            column.append(counter)
            counter += Board_Width
        board.append(column)
        counter -= Board_Width * (Board_Height - 1) + Board_Width - 1

    board[Board_Width-1][Board_Height-1] = BLANK
    return board
#____________________________________________ Nour ____________________________________________________________________

def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(Board_Width):
        for y in range(Board_Height):
            if board[x][y] == BLANK:
                return (x, y)
#_________________________________________ Rewas ______________________________________________________________________

def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    if move == Up:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == Down:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == Left:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == Right:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]

#____________________________________________ Rania ___________________________________________________________________
def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == Up and blanky != len(board[0]) - 1) or \
           (move == Down and blanky != 0) or \
           (move == Left and blankx != len(board) - 1) or \
           (move == Right and blankx != 0)
#____________________________________________ Noura _____________________________________________________________________

def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [Up, Down, Left, Right]

    # remove moves from the list as they are disqualified
    if lastMove == Up or not isValidMove(board, Down):
        validMoves.remove(Down)
    if lastMove == Down or not isValidMove(board, Up):
        validMoves.remove(Up)
    if lastMove == Left or not isValidMove(board, Right):
        validMoves.remove(Right)
    if lastMove == Right or not isValidMove(board, Left):
        validMoves.remove(Left)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)

#_____________________________________________ Hader __________________________________________________________________

def getLeftTopOfTile(tileX, tileY):
    left = X + (tileX * Square_Size) + (tileX - 1)
    top = Y + (tileY * Square_Size) + (tileY - 1)
    return (left, top)
#____________________________________________ Omnia ___________________________________________________________________

def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, Square_Size, Square_Size)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

#_____________________________________________ Rewas ___________________________________________________________________

def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(Display_SURF, Square_Color, (left + adjx, top + adjy, Square_Size, Square_Size))
    textSurf = Font.render(str(number), True, Text_Color)
    textRect = textSurf.get_rect()
    textRect.center = left + int(Square_Size / 2) + adjx, top + int(Square_Size / 2) + adjy
    Display_SURF.blit(textSurf, textRect)

#____________________________________________ Nour _____________________________________________________________________
def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = Font.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)
#__________________________________________ Rania ______________________________________________________________________

def drawBoard(board, message):
    Display_SURF.fill(Background_Color)
    if message:
        textSurf, textRect = makeText(message, Title_Color, Background_Color, 5, 5)
        Display_SURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = Board_Width * Square_Size
    height = Board_Height * Square_Size
    pygame.draw.rect(Display_SURF, Border_Color, (left - 5, top - 5, width + 11, height + 11), 4)


    Display_SURF.blit(NEW_SURF, NEW_RECT)
    Display_SURF.blit(SOLVE_SURF, SOLVE_RECT)
#_______________________________________________ Rewas _________________________________________________________________

def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == Up:
        movex = blankx
        movey = blanky + 1
    elif direction == Down:
        movex = blankx
        movey = blanky - 1
    elif direction == Left:
        movex = blankx + 1
        movey = blanky
    elif direction == Right:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = Display_SURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, Background_Color, (moveLeft, moveTop, Square_Size, Square_Size))

    for i in range(0, Square_Size, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        Display_SURF.blit(baseSurf, (0, 0))
        if direction == Up:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == Down:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == Left:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == Right:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        Speed_Clock.tick(Speed)
#_________________________________________________ Omnia _______________________________________________________________

def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500) # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(Square_Size / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)

#______________________________________________________ Hadeer _________________________________________________________
def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:] # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == Up:
            oppositeMove = Down
        elif move == Down:
            oppositeMove = Up
        elif move == Right:
            oppositeMove = Left
        elif move == Left:
            oppositeMove = Right
        slideAnimation(board, oppositeMove, '', animationSpeed=int(Square_Size / 2))
        makeMove(board, oppositeMove)


if __name__ == '__main__':
     main()