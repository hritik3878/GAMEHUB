import pygame,sys,random,time
from pygame.locals import *
pygame.init()
displaysurf=pygame.display.set_mode((1347,720))
pygame.display.set_caption("GAME HUB")
icon=pygame.image.load("gameicon.png")
pygame.display.set_icon(icon)
back=pygame.image.load("back4.jpg")
pygame.mixer.music.load("gameaudio.mp3")
memopuzz=pygame.image.load("memopuzz.jpg")
memo_rect=memopuzz.get_rect()
memo_rect.topleft=(580,300)
tet=pygame.image.load("tet.jpg")
tet_rect=tet.get_rect()
tet_rect.topleft=(580,440)
slide=pygame.image.load("slide.jpg")
slide_rect=slide.get_rect()
slide_rect.topleft=(580,580)
gamehub=pygame.image.load("head.jpg")
pygame.mixer.music.play(-1,0.0)
while 1:
    
    displaysurf.blit(back,(0,0))
    displaysurf.blit(gamehub,(355,10))
    displaysurf.blit(memopuzz,memo_rect)
    displaysurf.blit(tet,tet_rect)
    displaysurf.blit(slide,slide_rect)
   
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
                pos=pygame.mouse.get_pos()

                if memo_rect.collidepoint(pos):
                    
                    pygame.mixer.music.stop()
                    FPS = 30 # frames per second, the general speed of the program
                    WINDOWWIDTH = 640 # size of window's width in pixels
                    WINDOWHEIGHT = 480 # size of windows' height in pixels
                    REVEALSPEED = 8 # speed boxes' sliding reveals and covers
                    BOXSIZE = 40 # size of box height & width in pixels
                    GAPSIZE = 10 # size of gap between boxes in pixels
                    BOARDWIDTH = 10 # number of columns of icons
                    BOARDHEIGHT = 7 # number of rows of icons
                    assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
                    XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
                    YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

                    #            R    G    B
                    GRAY     = (100, 100, 100)
                    NAVYBLUE = ( 60,  60, 100)
                    WHITE    = (255, 255, 255)
                    RED      = (255,   0,   0)
                    GREEN    = (  0, 255,   0)
                    BLUE     = (  0,   0, 255)
                    YELLOW   = (255, 255,   0)
                    ORANGE   = (255, 128,   0)
                    PURPLE   = (255,   0, 255)
                    CYAN     = (  0, 255, 255)

                    BGCOLOR = NAVYBLUE
                    LIGHTBGCOLOR = GRAY
                    BOXCOLOR = WHITE
                    HIGHLIGHTCOLOR = BLUE

                    DONUT = 'donut'
                    SQUARE = 'square'
                    DIAMOND = 'diamond'
                    LINES = 'lines'
                    OVAL = 'oval'

                    ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
                    ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
                    assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

                    def main():
                        global FPSCLOCK, DISPLAYSURF
                        pygame.init()
                        FPSCLOCK = pygame.time.Clock()
                        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

                        mousex = 0 # used to store x coordinate of mouse event
                        mousey = 0 # used to store y coordinate of mouse event
                        pygame.display.set_caption('Memory Game')

                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        firstSelection = None # stores the (x, y) of the first box clicked.

                        DISPLAYSURF.fill(BGCOLOR)
                        startGameAnimation(mainBoard)

                        while True: # main game loop
                            mouseClicked = False

                            DISPLAYSURF.fill(BGCOLOR) # drawing the window
                            drawBoard(mainBoard, revealedBoxes)

                            for event in pygame.event.get(): # event handling loop
                                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == MOUSEMOTION:
                                    mousex, mousey = event.pos
                                elif event.type == MOUSEBUTTONUP:
                                    mousex, mousey = event.pos
                                    mouseClicked = True

                            boxx, boxy = getBoxAtPixel(mousex, mousey)
                            if boxx != None and boxy != None:
                                # The mouse is currently over a box.
                                if not revealedBoxes[boxx][boxy]:
                                    drawHighlightBox(boxx, boxy)
                                if not revealedBoxes[boxx][boxy] and mouseClicked:
                                    revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                                    revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                                    if firstSelection == None: # the current box was the first box clicked
                                        firstSelection = (boxx, boxy)
                                    else: # the current box was the second box clicked
                                        # Check if there is a match between the two icons.
                                        icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                                        icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                                        if icon1shape != icon2shape or icon1color != icon2color:
                                            # Icons don't match. Re-cover up both selections.
                                            pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                                            coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                                            revealedBoxes[boxx][boxy] = False
                                        elif hasWon(revealedBoxes): # check if all pairs found
                                            gameWonAnimation(mainBoard)
                                            pygame.time.wait(2000)

                                            # Reset the board
                                            mainBoard = getRandomizedBoard()
                                            revealedBoxes = generateRevealedBoxesData(False)

                                            # Show the fully unrevealed board for a second.
                                            drawBoard(mainBoard, revealedBoxes)
                                            pygame.display.update()
                                            pygame.time.wait(1000)

                                            # Replay the start game animation.
                                            startGameAnimation(mainBoard)
                                        firstSelection = None # reset firstSelection variable

                            # Redraw the screen and wait a clock tick.
                            pygame.display.update()
                            FPSCLOCK.tick(FPS)


                    def generateRevealedBoxesData(val):
                        revealedBoxes = []
                        for i in range(BOARDWIDTH):
                            revealedBoxes.append([val] * BOARDHEIGHT)
                        return revealedBoxes


                    def getRandomizedBoard():
                        # Get a list of every possible shape in every possible color.
                        icons = []
                        for color in ALLCOLORS:
                            for shape in ALLSHAPES:
                                icons.append( (shape, color) )

                        random.shuffle(icons) # randomize the order of the icons list
                        numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
                        icons = icons[:numIconsUsed] * 2 # make two of each
                        random.shuffle(icons)

                        # Create the board data structure, with randomly placed icons.
                        board = []
                        for x in range(BOARDWIDTH):
                            column = []
                            for y in range(BOARDHEIGHT):
                                column.append(icons[0])
                                del icons[0] # remove the icons as we assign them
                            board.append(column)
                        return board


                    def splitIntoGroupsOf(groupSize, theList):
                        # splits a list into a list of lists, where the inner lists have at
                        # most groupSize number of items.
                        result = []
                        for i in range(0, len(theList), groupSize):
                            result.append(theList[i:i + groupSize])
                        return result


                    def leftTopCoordsOfBox(boxx, boxy):
                        # Convert board coordinates to pixel coordinates
                        left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
                        top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
                        return (left, top)


                    def getBoxAtPixel(x, y):
                        for boxx in range(BOARDWIDTH):
                            for boxy in range(BOARDHEIGHT):
                                left, top = leftTopCoordsOfBox(boxx, boxy)
                                boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                                if boxRect.collidepoint(x, y):
                                    return (boxx, boxy)
                        return (None, None)


                    def drawIcon(shape, color, boxx, boxy):
                        quarter = int(BOXSIZE * 0.25) # syntactic sugar
                        half =    int(BOXSIZE * 0.5)  # syntactic sugar

                        left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
                        # Draw the shapes
                        if shape == DONUT:
                            pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
                            pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
                        elif shape == SQUARE:
                            pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
                        elif shape == DIAMOND:
                            pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
                        elif shape == LINES:
                            for i in range(0, BOXSIZE, 4):
                                pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
                                pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
                        elif shape == OVAL:
                            pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


                    def getShapeAndColor(board, boxx, boxy):
                        # shape value for x, y spot is stored in board[x][y][0]
                        # color value for x, y spot is stored in board[x][y][1]
                        return board[boxx][boxy][0], board[boxx][boxy][1]


                    def drawBoxCovers(board, boxes, coverage):
                        # Draws boxes being covered/revealed. "boxes" is a list
                        # of two-item lists, which have the x & y spot of the box.
                        for box in boxes:
                            left, top = leftTopCoordsOfBox(box[0], box[1])
                            pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
                            shape, color = getShapeAndColor(board, box[0], box[1])
                            drawIcon(shape, color, box[0], box[1])
                            if coverage > 0: # only draw the cover if there is an coverage
                                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)


                    def revealBoxesAnimation(board, boxesToReveal):
                        # Do the "box reveal" animation.
                        for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
                            drawBoxCovers(board, boxesToReveal, coverage)


                    def coverBoxesAnimation(board, boxesToCover):
                        # Do the "box cover" animation.
                        for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
                            drawBoxCovers(board, boxesToCover, coverage)


                    def drawBoard(board, revealed):
                        # Draws all of the boxes in their covered or revealed state.
                        for boxx in range(BOARDWIDTH):
                            for boxy in range(BOARDHEIGHT):
                                left, top = leftTopCoordsOfBox(boxx, boxy)
                                if not revealed[boxx][boxy]:
                                    # Draw a covered box.
                                    pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
                                else:
                                    # Draw the (revealed) icon.
                                    shape, color = getShapeAndColor(board, boxx, boxy)
                                    drawIcon(shape, color, boxx, boxy)


                    def drawHighlightBox(boxx, boxy):
                        left, top = leftTopCoordsOfBox(boxx, boxy)
                        pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


                    def startGameAnimation(board):
                        # Randomly reveal the boxes 8 at a time.
                        coveredBoxes = generateRevealedBoxesData(False)
                        boxes = []
                        for x in range(BOARDWIDTH):
                            for y in range(BOARDHEIGHT):
                                boxes.append( (x, y) )
                        random.shuffle(boxes)
                        boxGroups = splitIntoGroupsOf(8, boxes)

                        drawBoard(board, coveredBoxes)
                        for boxGroup in boxGroups:
                            revealBoxesAnimation(board, boxGroup)
                            coverBoxesAnimation(board, boxGroup)


                    def gameWonAnimation(board):
                        # flash the background color when the player has won
                        coveredBoxes = generateRevealedBoxesData(True)
                        color1 = LIGHTBGCOLOR
                        color2 = BGCOLOR

                        for i in range(13):
                            color1, color2 = color2, color1 # swap colors
                            DISPLAYSURF.fill(color1)
                            drawBoard(board, coveredBoxes)
                            pygame.display.update()
                            pygame.time.wait(300)


                    def hasWon(revealedBoxes):
                        # Returns True if all the boxes have been revealed, otherwise False
                        for i in revealedBoxes:
                            if False in i:
                                return False # return False if any boxes are covered.
                        return True


                    if __name__ == '__main__':
                        main()

                elif slide_rect.collidepoint(pos):
                    pygame.mixer.music.stop()
                    BOARDWIDTH = 4  # number of columns in the board
                    BOARDHEIGHT = 4 # number of rows in the board
                    TILESIZE = 80
                    WINDOWWIDTH = 640
                    WINDOWHEIGHT = 480
                    FPS = 30
                    BLANK = None

                    #                 R    G    B
                    BLACK =         (  0,   0,   0)
                    WHITE =         (255, 255, 255)
                    BRIGHTBLUE =    (  0,  50, 255)
                    DARKTURQUOISE = (  3,  54,  73)
                    GREEN =         (  0, 204,   0)

                    BGCOLOR = DARKTURQUOISE
                    TILECOLOR = GREEN
                    TEXTCOLOR = WHITE
                    BORDERCOLOR = BRIGHTBLUE
                    BASICFONTSIZE = 20

                    BUTTONCOLOR = WHITE
                    BUTTONTEXTCOLOR = BLACK
                    MESSAGECOLOR = WHITE

                    XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
                    YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

                    UP = 'up'
                    DOWN = 'down'
                    LEFT = 'left'
                    RIGHT = 'right'

                    def main():
                        global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

                        pygame.init()
                        FPSCLOCK = pygame.time.Clock()
                        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
                        pygame.display.set_caption('Slide Puzzle')
                        BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

                        # Store the option buttons and their rectangles in OPTIONS.
                        RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
                        NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
                        SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        SOLVEDBOARD = getStartingBoard() # a solved board is the same as the board in a start state.
                        allMoves = [] # list of moves made from the solved configuration

                        while True: # main game loop
                            slideTo = None # the direction, if any, a tile should slide
                            msg = 'Click tile or press arrow keys to slide.' # contains the message to show in the upper left corner.
                            if mainBoard == SOLVEDBOARD:
                                msg = 'Solved!'

                            drawBoard(mainBoard, msg)

                            checkForQuit()
                            for event in pygame.event.get(): # event handling loop
                                if event.type == MOUSEBUTTONUP:
                                    spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                                    if (spotx, spoty) == (None, None):
                                        # check if the user clicked on an option button
                                        if RESET_RECT.collidepoint(event.pos):
                                            resetAnimation(mainBoard, allMoves) # clicked on Reset button
                                            allMoves = []
                                        elif NEW_RECT.collidepoint(event.pos):
                                            mainBoard, solutionSeq = generateNewPuzzle(80) # clicked on New Game button
                                            allMoves = []
                                        elif SOLVE_RECT.collidepoint(event.pos):
                                            resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on Solve button
                                            allMoves = []
                                    else:
                                        # check if the clicked tile was next to the blank spot

                                        blankx, blanky = getBlankPosition(mainBoard)
                                        if spotx == blankx + 1 and spoty == blanky:
                                            slideTo = LEFT
                                        elif spotx == blankx - 1 and spoty == blanky:
                                            slideTo = RIGHT
                                        elif spotx == blankx and spoty == blanky + 1:
                                            slideTo = UP
                                        elif spotx == blankx and spoty == blanky - 1:
                                            slideTo = DOWN

                                elif event.type == KEYUP:
                                    # check if the user pressed a key to slide a tile
                                    if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                                        slideTo = LEFT
                                    elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                                        slideTo = RIGHT
                                    elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                                        slideTo = UP
                                    elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                                        slideTo = DOWN

                            if slideTo:
                                slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8) # show slide on screen
                                makeMove(mainBoard, slideTo)
                                allMoves.append(slideTo) # record the slide
                            pygame.display.update()
                            FPSCLOCK.tick(FPS)


                    def terminate():
                        pygame.quit()
                        sys.exit()


                    def checkForQuit():
                        for event in pygame.event.get(QUIT): # get all the QUIT events
                            terminate() # terminate if any QUIT events are present
                        for event in pygame.event.get(KEYUP): # get all the KEYUP events
                            if event.key == K_ESCAPE:
                                terminate() # terminate if the KEYUP event was for the Esc key
                            pygame.event.post(event) # put the other KEYUP event objects back


                    def getStartingBoard():
                        # Return a board data structure with tiles in the solved state.
                        # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
                        # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
                        counter = 1
                        board = []
                        for x in range(BOARDWIDTH):
                            column = []
                            for y in range(BOARDHEIGHT):
                                column.append(counter)
                                counter += BOARDWIDTH
                            board.append(column)
                            counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

                        board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
                        return board


                    def getBlankPosition(board):
                        # Return the x and y of board coordinates of the blank space.
                        for x in range(BOARDWIDTH):
                            for y in range(BOARDHEIGHT):
                                if board[x][y] == BLANK:
                                    return (x, y)


                    def makeMove(board, move):
                        # This function does not check if the move is valid.
                        blankx, blanky = getBlankPosition(board)

                        if move == UP:
                            board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
                        elif move == DOWN:
                            board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
                        elif move == LEFT:
                            board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
                        elif move == RIGHT:
                            board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


                    def isValidMove(board, move):
                        blankx, blanky = getBlankPosition(board)
                        return (move == UP and blanky != len(board[0]) - 1) or \
                               (move == DOWN and blanky != 0) or \
                               (move == LEFT and blankx != len(board) - 1) or \
                               (move == RIGHT and blankx != 0)


                    def getRandomMove(board, lastMove=None):
                        # start with a full list of all four moves
                        validMoves = [UP, DOWN, LEFT, RIGHT]

                        # remove moves from the list as they are disqualified
                        if lastMove == UP or not isValidMove(board, DOWN):
                            validMoves.remove(DOWN)
                        if lastMove == DOWN or not isValidMove(board, UP):
                            validMoves.remove(UP)
                        if lastMove == LEFT or not isValidMove(board, RIGHT):
                            validMoves.remove(RIGHT)
                        if lastMove == RIGHT or not isValidMove(board, LEFT):
                            validMoves.remove(LEFT)

                        # return a random move from the list of remaining moves
                        return random.choice(validMoves)


                    def getLeftTopOfTile(tileX, tileY):
                        left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
                        top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
                        return (left, top)


                    def getSpotClicked(board, x, y):
                        # from the x & y pixel coordinates, get the x & y board coordinates
                        for tileX in range(len(board)):
                            for tileY in range(len(board[0])):
                                left, top = getLeftTopOfTile(tileX, tileY)
                                tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
                                if tileRect.collidepoint(x, y):
                                    return (tileX, tileY)
                        return (None, None)


                    def drawTile(tilex, tiley, number, adjx=0, adjy=0):
                        # draw a tile at board coordinates tilex and tiley, optionally a few
                        # pixels over (determined by adjx and adjy)
                        left, top = getLeftTopOfTile(tilex, tiley)
                        pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
                        textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
                        textRect = textSurf.get_rect()
                        textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
                        DISPLAYSURF.blit(textSurf, textRect)


                    def makeText(text, color, bgcolor, top, left):
                        # create the Surface and Rect objects for some text.
                        textSurf = BASICFONT.render(text, True, color, bgcolor)
                        textRect = textSurf.get_rect()
                        textRect.topleft = (top, left)
                        return (textSurf, textRect)


                    def drawBoard(board, message):
                        DISPLAYSURF.fill(BGCOLOR)
                        if message:
                            textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
                            DISPLAYSURF.blit(textSurf, textRect)

                        for tilex in range(len(board)):
                            for tiley in range(len(board[0])):
                                if board[tilex][tiley]:
                                    drawTile(tilex, tiley, board[tilex][tiley])

                        left, top = getLeftTopOfTile(0, 0)
                        width = BOARDWIDTH * TILESIZE
                        height = BOARDHEIGHT * TILESIZE
                        pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

                        DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
                        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
                        DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


                    def slideAnimation(board, direction, message, animationSpeed):
                        # Note: This function does not check if the move is valid.

                        blankx, blanky = getBlankPosition(board)
                        if direction == UP:
                            movex = blankx
                            movey = blanky + 1
                        elif direction == DOWN:
                            movex = blankx
                            movey = blanky - 1
                        elif direction == LEFT:
                            movex = blankx + 1
                            movey = blanky
                        elif direction == RIGHT:
                            movex = blankx - 1
                            movey = blanky

                        # prepare the base surface
                        drawBoard(board, message)
                        baseSurf = DISPLAYSURF.copy()
                        # draw a blank space over the moving tile on the baseSurf Surface.
                        moveLeft, moveTop = getLeftTopOfTile(movex, movey)
                        pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

                        for i in range(0, TILESIZE, animationSpeed):
                            # animate the tile sliding over
                            checkForQuit()
                            DISPLAYSURF.blit(baseSurf, (0, 0))
                            if direction == UP:
                                drawTile(movex, movey, board[movex][movey], 0, -i)
                            if direction == DOWN:
                                drawTile(movex, movey, board[movex][movey], 0, i)
                            if direction == LEFT:
                                drawTile(movex, movey, board[movex][movey], -i, 0)
                            if direction == RIGHT:
                                drawTile(movex, movey, board[movex][movey], i, 0)

                            pygame.display.update()
                            FPSCLOCK.tick(FPS)


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
                            slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3))
                            makeMove(board, move)
                            sequence.append(move)
                            lastMove = move
                        return (board, sequence)


                    def resetAnimation(board, allMoves):
                        # make all of the moves in allMoves in reverse.
                        revAllMoves = allMoves[:] # gets a copy of the list
                        revAllMoves.reverse()

                        for move in revAllMoves:
                            if move == UP:
                                oppositeMove = DOWN
                            elif move == DOWN:
                                oppositeMove = UP
                            elif move == RIGHT:
                                oppositeMove = LEFT
                            elif move == LEFT:
                                oppositeMove = RIGHT
                            slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
                            makeMove(board, oppositeMove)


                    if __name__ == '__main__':
                        main()
                elif tet_rect.collidepoint(pos):
                    pygame.mixer.music.stop()
                    FPS = 25
                    WINDOWWIDTH = 640
                    WINDOWHEIGHT = 480
                    BOXSIZE = 20
                    BOARDWIDTH = 10
                    BOARDHEIGHT = 20
                    BLANK = '.'

                    MOVESIDEWAYSFREQ = 0.15
                    MOVEDOWNFREQ = 0.1

                    XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
                    TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

                    #               R    G    B
                    WHITE       = (255, 255, 255)
                    GRAY        = (185, 185, 185)
                    BLACK       = (  0,   0,   0)
                    RED         = (155,   0,   0)
                    LIGHTRED    = (175,  20,  20)
                    GREEN       = (  0, 155,   0)
                    LIGHTGREEN  = ( 20, 175,  20)
                    BLUE        = (  0,   0, 155)
                    LIGHTBLUE   = ( 20,  20, 175)
                    YELLOW      = (155, 155,   0)
                    LIGHTYELLOW = (175, 175,  20)

                    BORDERCOLOR = BLUE
                    BGCOLOR = BLACK
                    TEXTCOLOR = WHITE
                    TEXTSHADOWCOLOR = GRAY
                    COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
                    LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
                    assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

                    TEMPLATEWIDTH = 5
                    TEMPLATEHEIGHT = 5

                    S_SHAPE_TEMPLATE = [['.....',
                                         '.....',
                                         '..OO.',
                                         '.OO..',
                                         '.....'],
                                        ['.....',
                                         '..O..',
                                         '..OO.',
                                         '...O.',
                                         '.....']]

                    Z_SHAPE_TEMPLATE = [['.....',
                                         '.....',
                                         '.OO..',
                                         '..OO.',
                                         '.....'],
                                        ['.....',
                                         '..O..',
                                         '.OO..',
                                         '.O...',
                                         '.....']]

                    I_SHAPE_TEMPLATE = [['..O..',
                                         '..O..',
                                         '..O..',
                                         '..O..',
                                         '.....'],
                                        ['.....',
                                         '.....',
                                         'OOOO.',
                                         '.....',
                                         '.....']]

                    O_SHAPE_TEMPLATE = [['.....',
                                         '.....',
                                         '.OO..',
                                         '.OO..',
                                         '.....']]

                    J_SHAPE_TEMPLATE = [['.....',
                                         '.O...',
                                         '.OOO.',
                                         '.....',
                                         '.....'],
                                        ['.....',
                                         '..OO.',
                                         '..O..',
                                         '..O..',
                                         '.....'],
                                        ['.....',
                                         '.....',
                                         '.OOO.',
                                         '...O.',
                                         '.....'],
                                        ['.....',
                                         '..O..',
                                         '..O..',
                                         '.OO..',
                                         '.....']]

                    L_SHAPE_TEMPLATE = [['.....',
                                         '...O.',
                                         '.OOO.',
                                         '.....',
                                         '.....'],
                                        ['.....',
                                         '..O..',
                                         '..O..',
                                         '..OO.',
                                         '.....'],
                                        ['.....',
                                         '.....',
                                         '.OOO.',
                                         '.O...',
                                         '.....'],
                                        ['.....',
                                         '.OO..',
                                         '..O..',
                                         '..O..',
                                         '.....']]

                    T_SHAPE_TEMPLATE = [['.....',
                                         '..O..',
                                         '.OOO.',
                                         '.....',
                                         '.....'],
                                        ['.....',
                                         '..O..',
                                         '..OO.',
                                         '..O..',
                                         '.....'],
                                        ['.....',
                                         '.....',
                                         '.OOO.',
                                         '..O..',
                                         '.....'],
                                        ['.....',
                                         '..O..',
                                         '.OO..',
                                         '..O..',
                                         '.....']]

                    PIECES = {'S': S_SHAPE_TEMPLATE,
                              'Z': Z_SHAPE_TEMPLATE,
                              'J': J_SHAPE_TEMPLATE,
                              'L': L_SHAPE_TEMPLATE,
                              'I': I_SHAPE_TEMPLATE,
                              'O': O_SHAPE_TEMPLATE,
                              'T': T_SHAPE_TEMPLATE}


                    def main():
                        global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
                        pygame.init()
                        FPSCLOCK = pygame.time.Clock()
                        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
                        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
                        BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
                        pygame.display.set_caption('Tetromino')

                        showTextScreen('Tetromino')
                        while True: # game loop
                            if random.randint(0, 1) == 0:
                                pygame.mixer.music.load('tetrisb.mid')
                            else:
                                pygame.mixer.music.load('tetrisc.mid')
                            pygame.mixer.music.play(-1, 0.0)
                            runGame()
                            pygame.mixer.music.stop()
                            showTextScreen('Game Over')


                    def runGame():
                        # setup variables for the start of the game
                        board = getBlankBoard()
                        lastMoveDownTime = time.time()
                        lastMoveSidewaysTime = time.time()
                        lastFallTime = time.time()
                        movingDown = False # note: there is no movingUp variable
                        movingLeft = False
                        movingRight = False
                        score = 0
                        level, fallFreq = calculateLevelAndFallFreq(score)

                        fallingPiece = getNewPiece()
                        nextPiece = getNewPiece()

                        while True: # game loop
                            if fallingPiece == None:
                                # No falling piece in play, so start a new piece at the top
                                fallingPiece = nextPiece
                                nextPiece = getNewPiece()
                                lastFallTime = time.time() # reset lastFallTime

                                if not isValidPosition(board, fallingPiece):
                                    return # can't fit a new piece on the board, so game over

                            checkForQuit()
                            for event in pygame.event.get(): # event handling loop
                                if event.type == KEYUP:
                                    if (event.key == K_p):
                                        # Pausing the game
                                        DISPLAYSURF.fill(BGCOLOR)
                                        pygame.mixer.music.stop()
                                        showTextScreen('Paused') # pause until a key press
                                        pygame.mixer.music.play(-1, 0.0)
                                        lastFallTime = time.time()
                                        lastMoveDownTime = time.time()
                                        lastMoveSidewaysTime = time.time()
                                    elif (event.key == K_LEFT or event.key == K_a):
                                        movingLeft = False
                                    elif (event.key == K_RIGHT or event.key == K_d):
                                        movingRight = False
                                    elif (event.key == K_DOWN or event.key == K_s):
                                        movingDown = False

                                elif event.type == KEYDOWN:
                                    # moving the piece sideways
                                    if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                                        fallingPiece['x'] -= 1
                                        movingLeft = True
                                        movingRight = False
                                        lastMoveSidewaysTime = time.time()

                                    elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                                        fallingPiece['x'] += 1
                                        movingRight = True
                                        movingLeft = False
                                        lastMoveSidewaysTime = time.time()

                                    # rotating the piece (if there is room to rotate)
                                    elif (event.key == K_UP or event.key == K_w):
                                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                                        if not isValidPosition(board, fallingPiece):
                                            fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                                    elif (event.key == K_q): # rotate the other direction
                                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                                        if not isValidPosition(board, fallingPiece):
                                            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                                    # making the piece fall faster with the down key
                                    elif (event.key == K_DOWN or event.key == K_s):
                                        movingDown = True
                                        if isValidPosition(board, fallingPiece, adjY=1):
                                            fallingPiece['y'] += 1
                                        lastMoveDownTime = time.time()

                                    # move the current piece all the way down
                                    elif event.key == K_SPACE:
                                        movingDown = False
                                        movingLeft = False
                                        movingRight = False
                                        for i in range(1, BOARDHEIGHT):
                                            if not isValidPosition(board, fallingPiece, adjY=i):
                                                break
                                        fallingPiece['y'] += i - 1

                            # handle moving the piece because of user input
                            if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
                                if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                                    fallingPiece['x'] -= 1
                                elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                                    fallingPiece['x'] += 1
                                lastMoveSidewaysTime = time.time()

                            if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
                                fallingPiece['y'] += 1
                                lastMoveDownTime = time.time()

                            # let the piece fall if it is time to fall
                            if time.time() - lastFallTime > fallFreq:
                                # see if the piece has landed
                                if not isValidPosition(board, fallingPiece, adjY=1):
                                    # falling piece has landed, set it on the board
                                    addToBoard(board, fallingPiece)
                                    score += removeCompleteLines(board)
                                    level, fallFreq = calculateLevelAndFallFreq(score)
                                    fallingPiece = None
                                else:
                                    # piece did not land, just move the piece down
                                    fallingPiece['y'] += 1
                                    lastFallTime = time.time()

                            # drawing everything on the screen
                            DISPLAYSURF.fill(BGCOLOR)
                            drawBoard(board)
                            drawStatus(score, level)
                            drawNextPiece(nextPiece)
                            if fallingPiece != None:
                                drawPiece(fallingPiece)

                            pygame.display.update()
                            FPSCLOCK.tick(FPS)


                    def makeTextObjs(text, font, color):
                        surf = font.render(text, True, color)
                        return surf, surf.get_rect()


                    def terminate():
                        pygame.quit()
                        sys.exit()


                    def checkForKeyPress():
                        # Go through event queue looking for a KEYUP event.
                        # Grab KEYDOWN events to remove them from the event queue.
                        checkForQuit()

                        for event in pygame.event.get([KEYDOWN, KEYUP]):
                            if event.type == KEYDOWN:
                                continue
                            return event.key
                        return None


                    def showTextScreen(text):
                        # This function displays large text in the
                        # center of the screen until a key is pressed.
                        # Draw the text drop shadow
                        titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
                        titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
                        DISPLAYSURF.blit(titleSurf, titleRect)

                        # Draw the text
                        titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
                        titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
                        DISPLAYSURF.blit(titleSurf, titleRect)

                        # Draw the additional "Press a key to play." text.
                        pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
                        pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
                        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

                        while checkForKeyPress() == None:
                            pygame.display.update()
                            FPSCLOCK.tick()


                    def checkForQuit():
                        for event in pygame.event.get(QUIT): # get all the QUIT events
                            terminate() # terminate if any QUIT events are present
                        for event in pygame.event.get(KEYUP): # get all the KEYUP events
                            if event.key == K_ESCAPE:
                                terminate() # terminate if the KEYUP event was for the Esc key
                            pygame.event.post(event) # put the other KEYUP event objects back


                    def calculateLevelAndFallFreq(score):
                        # Based on the score, return the level the player is on and
                        # how many seconds pass until a falling piece falls one space.
                        level = int(score / 10) + 1
                        fallFreq = 0.27 - (level * 0.02)
                        return level, fallFreq

                    def getNewPiece():
                        # return a random new piece in a random rotation and color
                        shape = random.choice(list(PIECES.keys()))
                        newPiece = {'shape': shape,
                                    'rotation': random.randint(0, len(PIECES[shape]) - 1),
                                    'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                                    'y': -2, # start it above the board (i.e. less than 0)
                                    'color': random.randint(0, len(COLORS)-1)}
                        return newPiece


                    def addToBoard(board, piece):
                        # fill in the board based on piece's location, shape, and rotation
                        for x in range(TEMPLATEWIDTH):
                            for y in range(TEMPLATEHEIGHT):
                                if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                                    board[x + piece['x']][y + piece['y']] = piece['color']


                    def getBlankBoard():
                        # create and return a new blank board data structure
                        board = []
                        for i in range(BOARDWIDTH):
                            board.append([BLANK] * BOARDHEIGHT)
                        return board


                    def isOnBoard(x, y):
                        return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


                    def isValidPosition(board, piece, adjX=0, adjY=0):
                        # Return True if the piece is within the board and not colliding
                        for x in range(TEMPLATEWIDTH):
                            for y in range(TEMPLATEHEIGHT):
                                isAboveBoard = y + piece['y'] + adjY < 0
                                if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                                    continue
                                if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                                    return False
                                if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                                    return False
                        return True

                    def isCompleteLine(board, y):
                        # Return True if the line filled with boxes with no gaps.
                        for x in range(BOARDWIDTH):
                            if board[x][y] == BLANK:
                                return False
                        return True


                    def removeCompleteLines(board):
                        # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
                        numLinesRemoved = 0
                        y = BOARDHEIGHT - 1 # start y at the bottom of the board
                        while y >= 0:
                            if isCompleteLine(board, y):
                                # Remove the line and pull boxes down by one line.
                                for pullDownY in range(y, 0, -1):
                                    for x in range(BOARDWIDTH):
                                        board[x][pullDownY] = board[x][pullDownY-1]
                                # Set very top line to blank.
                                for x in range(BOARDWIDTH):
                                    board[x][0] = BLANK
                                numLinesRemoved += 1
                                # Note on the next iteration of the loop, y is the same.
                                # This is so that if the line that was pulled down is also
                                # complete, it will be removed.
                            else:
                                y -= 1 # move on to check next row up
                        return numLinesRemoved


                    def convertToPixelCoords(boxx, boxy):
                        # Convert the given xy coordinates of the board to xy
                        # coordinates of the location on the screen.
                        return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


                    def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
                        # draw a single box (each tetromino piece has four boxes)
                        # at xy coordinates on the board. Or, if pixelx & pixely
                        # are specified, draw to the pixel coordinates stored in
                        # pixelx & pixely (this is used for the "Next" piece).
                        if color == BLANK:
                            return
                        if pixelx == None and pixely == None:
                            pixelx, pixely = convertToPixelCoords(boxx, boxy)
                        pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
                        pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


                    def drawBoard(board):
                        # draw the border around the board
                        pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

                        # fill the background of the board
                        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
                        # draw the individual boxes on the board
                        for x in range(BOARDWIDTH):
                            for y in range(BOARDHEIGHT):
                                drawBox(x, y, board[x][y])


                    def drawStatus(score, level):
                        # draw the score text
                        scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
                        scoreRect = scoreSurf.get_rect()
                        scoreRect.topleft = (WINDOWWIDTH - 150, 20)
                        DISPLAYSURF.blit(scoreSurf, scoreRect)

                        # draw the level text
                        levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
                        levelRect = levelSurf.get_rect()
                        levelRect.topleft = (WINDOWWIDTH - 150, 50)
                        DISPLAYSURF.blit(levelSurf, levelRect)


                    def drawPiece(piece, pixelx=None, pixely=None):
                        shapeToDraw = PIECES[piece['shape']][piece['rotation']]
                        if pixelx == None and pixely == None:
                            # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
                            pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

                        # draw each of the boxes that make up the piece
                        for x in range(TEMPLATEWIDTH):
                            for y in range(TEMPLATEHEIGHT):
                                if shapeToDraw[y][x] != BLANK:
                                    drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


                    def drawNextPiece(piece):
                        # draw the "next" text
                        nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
                        nextRect = nextSurf.get_rect()
                        nextRect.topleft = (WINDOWWIDTH - 120, 80)
                        DISPLAYSURF.blit(nextSurf, nextRect)
                        # draw the "next" piece
                        drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)


                    if __name__ == '__main__':
                        main()

                        
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
            


