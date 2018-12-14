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

from objects import (
    Player,
    Ball
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
  
def drawBall(ball_mesh):
    pygame.draw.rect(DISPLAYSURF, GREY, ball_mesh)

# moves the ball, returns new position
def moveBall(ball, ball_mesh):
    ball_mesh.x += (ball.dirX * MODIFIER)
    ball_mesh.y += (ball.dirY * MODIFIER)

# checks for a collision with a wall, and 'bounces' off it.
def checkEdgeCollision(ball, ball_mesh):
    if ball_mesh.top == (LINETHICKNESS) or ball_mesh.bottom == (HEIGHT - LINETHICKNESS):
        ball.dirY = ball.dirY * -1
    if ball_mesh.left == (LINETHICKNESS) or ball_mesh.right == (WIDTH - LINETHICKNESS):
        ball.dirX = ball.dirX * -1

# checks if the ball has hit a paddle, and 'bounces' off it.     
def checkPaddleCollision(ball, ball_mesh, paddle1, paddle2):
    if ball.dirX == -1 and paddle1.right == ball_mesh.left and paddle1.top < ball_mesh.top and paddle1.bottom > ball_mesh.bottom:
        ball.dirX = ball.dirX * -1
    elif ball.dirX == 1 and paddle2.left == ball_mesh.right and paddle2.top < ball_mesh.top and paddle2.bottom > ball_mesh.bottom:
        ball.dirX = ball.dirX * -1
    else:
         ball.dirX = ball.dirX * 1

# computer "ai"      
def computerMove(ball, ball_mesh, paddle2):
    # if the ball is moving away from the paddle, center
    if ball.dirX == -1:
        if paddle2.centery < (HEIGHT/2):
            paddle2.y +=  MODIFIER - random.choice(DIFFICULTY)
        elif paddle2.centery > (HEIGHT/2):
            paddle2.y -=  MODIFIER - random.choice(DIFFICULTY)
    # if the ball moving towards the paddle, track its movement. 
    elif ball.dirX == 1:
        if paddle2.centery < ball_mesh.centery:
            paddle2.y +=  MODIFIER - random.choice(DIFFICULTY)
        else:
            paddle2.y -=  MODIFIER - random.choice(DIFFICULTY)
    return paddle2

# checks to see if a point has been scored, returns new score
def checkScore(ball_mesh, p1_score, p2_score):
    hit = False
    # reset points if left wall is hit
    if ball_mesh.left == LINETHICKNESS: 
        p2_score += 1
        hit = True
    # awards 1 point to the player if the right wall is hit
    elif ball_mesh.right == WIDTH - LINETHICKNESS:
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
    ball = Ball(
        x = ORIGIN_X, y = ORIGIN_Y,
        dirX = -1, dirY = -1
    )
    ball_mesh = pygame.Rect(ball.x, ball.y, LINETHICKNESS, LINETHICKNESS)

    playerOnePosition = playerTwoPosition = int((HEIGHT - PADDLESIZE) /2)
    p1_score = p2_score = 0
    game_over = False

    # creates Rectangles for ball and paddles
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)

    # draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball_mesh)

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
            drawBall(ball_mesh)

            moveBall(ball, ball_mesh)
            checkEdgeCollision(ball, ball_mesh)
            checkPaddleCollision(ball, ball_mesh, paddle1, paddle2)
            
            p1_score, p2_score, hit = checkScore(ball_mesh, p1_score, p2_score)
            paddle2 = computerMove (ball, ball_mesh, paddle2)
            
            displayScore(p1_score, p2_score)
            game_over = p1_score + p2_score == MAX_SCORE

            if hit:
                ball.x = ball_mesh.x = ORIGIN_X
                ball.y = ball_mesh.y = ORIGIN_Y
                hit = False
                pygame.time.wait(1000)
        else:
            gameOver()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()