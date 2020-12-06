class Dirt:
    color = (102, 51, 0)


class Air:
    color = (255, 255, 255)

class Rock:
    color = (128, 128, 128)

class Player:
    color = (0, 102, 255)
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Bomb:
    color = (0, 0, 0)
    def __init__(self, live = 200):
        self.live = live


    def tick(self):
        self.live -= 1
        return self.live <= 0

class Fire:
    color = (255, 102, 0)
    def __init__(self, live = 10):
        self.live = live


    def tick(self):
        self.live -= 1
        return self.live <= 0