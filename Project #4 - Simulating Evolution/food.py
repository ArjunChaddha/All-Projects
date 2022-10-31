import pygame

class Food:
    def __init__(self, x, y, screen, god):
        self.x = x
        self.y = y
        self.screen = screen
        self.eaten = False
        self.color = (0,255,0)
        self.size = 4
        self.god = god
        self.nutrition = 20
    
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.size)

    def setEaten(self):
        self.god.deadPlantAlert(self)
    #