
class Player:
    def __init__(self, name, paddle):
        self.name = name
        self.score = 0
        self.x = self.y = 0
        self.paddle = None


class Ball:

    def __init__(self, x, y, dirX, dirY, ball):
        self.x = x
        self.y = y
        self.dirX = dirX
        self.dirY = dirY
        self.ball = None
