import pygame
import random
import sys

from pygame.locals import *

from config import (
    FPS,
    MODIFIER,
    WIDTH,
    HEIGHT,
    LINETHICKNESS,
    PADDLESIZE,
    PADDLEOFFSET,
    BLACK,
    GREY,
    ORIGIN_X,
    ORIGIN_Y,
    DIFFICULTY,
    MAX_SCORE
)

def drawArena():
    DISPLAYSURF.fill((0, 0, 0))
    # draw the outline of arena
    pygame.draw.rect(DISPLAYSURF, GREY, ((0 ,0), (WIDTH, HEIGHT)), LINETHICKNESS*2)
    # draw the middle line
    pygame.draw.line(DISPLAYSURF, GREY, (int(WIDTH/2), 0), (int(WIDTH/2), HEIGHT), int(LINETHICKNESS/4))

def drawPaddle(paddle):
    # checks boundaries
    if paddle.bottom > HEIGHT - LINETHICKNESS:
        paddle.bottom = HEIGHT - LINETHICKNESS
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    # draws the paddle
    pygame.draw.rect(DISPLAYSURF, GREY, paddle)
  
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, GREY, ball)

# moves the ball, returns new position
def moveBall(ball, ballDirX, ballDirY):
    ball.x += (ballDirX * MODIFIER)
    ball.y += (ballDirY * MODIFIER)
    return ball

# checks for a collision with a wall, and 'bounces' off it.
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (HEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == (LINETHICKNESS) or ball.right == (WIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

# checks if the ball has hit a paddle, and 'bounces' off it.     
def checkPaddleCollision(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else:
        return 1

# computer "ai"      
def computerMove(ball, ballDirX, paddle2):
    # if the ball is moving away from the paddle, center
    if ballDirX == -1:
        if paddle2.centery < (HEIGHT/2):
            paddle2.y +=  MODIFIER - random.choice(DIFFICULTY)
        elif paddle2.centery > (HEIGHT/2):
            paddle2.y -=  MODIFIER - random.choice(DIFFICULTY)
    # if the ball moving towards the paddle, track its movement. 
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y +=  MODIFIER - random.choice(DIFFICULTY)
        else:
            paddle2.y -=  MODIFIER - random.choice(DIFFICULTY)
    return paddle2

# checks to see if a point has been scored, returns new score
def checkScore(ball, p1_score, p2_score):
    hit = False
    # reset points if left wall is hit
    if ball.left == LINETHICKNESS: 
        p2_score += 1
        hit = True
    # awards 1 point to the player if the right wall is hit
    elif ball.right == WIDTH - LINETHICKNESS:
        p1_score += 1
        hit = True
    # if no points scored, return score unchanged
    return p1_score, p2_score, hit

# displays the current score on the screen
def displayScore(p1_score, p2_score):
    # player
    resultP1Surf = BASICFONT.render('Player %s' %(p1_score), True, GREY)
    resultP1Rect = resultP1Surf.get_rect()
    resultP1Rect.topright = (100, 25)
    DISPLAYSURF.blit(resultP1Surf, resultP1Rect)
   
    # computer
    resultP2Surf = BASICFONT.render('Computer %s' %(p2_score), True, GREY)
    resultP2Rect = resultP2Surf.get_rect()
    resultP2Rect.topleft = (WIDTH - 150, 25)
    DISPLAYSURF.blit(resultP2Surf, resultP2Rect)

# displays the end of the game
def gameOver():
    finalSurf = BASICFONT.render('GAME OVER', True, GREY)
    finalSurfRect = finalSurf.get_rect()
    finalSurfRect.topright = (WIDTH/2 + 59, HEIGHT/2 - 50)
    DISPLAYSURF.blit(finalSurf, finalSurfRect)

# main function
def main():
    pygame.init()
    global DISPLAYSURF

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption('Pongame')
   
    # font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
   
    # initiate variables and set starting positions
    # for any future changes made within rectangles
    ballX = ORIGIN_X
    ballY = ORIGIN_Y
    playerOnePosition = playerTwoPosition = int((HEIGHT - PADDLESIZE) /2)
    p1_score = p2_score = 0
    game_over = False

    # keeps track of the ball's direction
    ballDirX = -1   # -1 = left 1 = right
    ballDirY = -1   # -1 = up 1 = down

    # creates Rectangles for ball and paddles
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    # draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    pygame.mouse.set_visible(0)
    while True: 
        # main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # mouse movement commands
            elif event.type == pygame.MOUSEMOTION and not game_over:
                mousex, mousey = event.pos
                paddle1.y = mousey

        if not game_over:
            drawArena()
            drawPaddle(paddle1)
            drawPaddle(paddle2)
            drawBall(ball)

            ball = moveBall(ball, ballDirX, ballDirY)
            ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
            ballDirX = ballDirX * checkPaddleCollision(ball, paddle1, paddle2, ballDirX)
            p1_score, p2_score, hit = checkScore(ball, p1_score, p2_score)
            paddle2 = computerMove (ball, ballDirX, paddle2)
            displayScore(p1_score, p2_score)
            game_over = p1_score + p2_score == MAX_SCORE

            if hit:
                ball.x = ballX = ORIGIN_X
                ball.y = ballY = ORIGIN_Y
                hit = False
                pygame.time.wait(1000)
        else:
            gameOver()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()