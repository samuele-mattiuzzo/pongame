import pygame
import sys

from pygame.locals import *

from config import (
    FPS,
    WIDTH,
    HEIGHT,
    LINETHICKNESS,
    PADDLESIZE,
    PADDLEOFFSET,
    BLACK,
    WHITE
)

def drawArena():
    DISPLAYSURF.fill((0, 0, 0))
    # draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0 ,0), (WIDTH, HEIGHT)), LINETHICKNESS*2)
    # draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, (int(WIDTH/2), 0), (int(WIDTH/2), HEIGHT), int(LINETHICKNESS/4))

def drawPaddle(paddle):
    # stops paddle moving too low
    if paddle.bottom > HEIGHT - LINETHICKNESS:
        paddle.bottom = HEIGHT - LINETHICKNESS
    # stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    # draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)
  
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

#moves the ball returns new position
def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball


#Main function
def main():
    pygame.init()
    global DISPLAYSURF

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption('Pong')

    #Initiate variable and set starting positions
    #any future changes made within rectangles
    ballX = WIDTH/2 - LINETHICKNESS/2
    ballY = HEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = int((HEIGHT - PADDLESIZE) /2)
    playerTwoPosition = int((HEIGHT - PADDLESIZE) /2)

    #Keeps track of ball direction
    ballDirX = -1 ## -1 = left 1 = right
    ballDirY = -1 ## -1 = up 1 = down

    #Creates Rectangles for ball and paddles.
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS,PADDLESIZE)
    paddle2 = pygame.Rect(WIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    #Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    while True: #main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()