"""
File Holding the animal class
"""
import pygame
import numpy as np
import math

class Animal:
    """ class contating all the animal varaibles and functions """
    def __init__(self, x, y, screen, god, color=(0,0,255), size=10, speed=20, energyCapacity=100, sight=40, age=0):
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.god = god
        self.age = age
        self.gotFoodOnce = False

        self.size = size
        self.speed = speed
        self.energyCapacity = energyCapacity
        self.sight = sight

        self.currentEnergy = self.energyCapacity
        self.limit = pygame.display.get_surface().get_size()[0]
    
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.size)

    def updatePosition(self, direction=None):
        dt = self.speed
        if direction == None:
            dx = (math.sqrt(dt) * np.random.normal())
            dy = (math.sqrt(dt) * np.random.normal())
            if not self.x+ dx >= self.limit and not self.x+ dx <= 0:
                self.x += dx
            if not self.y+ dy >= self.limit and not self.y+ dy <= 0:
                self.y += dy
        else:
            tx = direction[0]
            ty = direction[1]
            d = self.getDistancetoFood(tx,ty)
            if d < self.speed:
                self.x = tx
                self.y = ty
            else:
                if not tx == self.x:
                    theta = math.atan((ty-self.y)/(tx-self.x))
                    self.x += math.sqrt(self.speed)*math.cos(theta)
                    self.y +=  math.sqrt(self.speed)*math.sin(theta)
                else:
                    self.y += math.sqrt(self.speed)

    def update(self):
        updatedPosition = False
        self.currentEnergy -= 0.1
        self.age += 0.2
        if self.currentEnergy <= 0:
            self.god.deadAnimalAlert(self)

        if self.currentEnergy >= 50 and self.age > 100 and self.gotFoodOnce:
            c = 0
            animals = self.god.animals
            for a in animals:
                d = self.getDistancetoFood(a.x, a.y)
                if d <= self.sight and c <= 3:
                    self.god.addMatingRequest(self, a)
                    c += 1

        if self.currentEnergy <= 70:
            foods = self.god.foods
            min_ = 10000000000
            ff = None
            for f in foods:
                d = self.getDistancetoFood(f.x, f.y)
                if d < min_:
                    min_ = d
                    ff = f
            if min_ == 0:
                self.eatFood(ff)
            elif min_ <= self.sight:
                self.updatePosition((ff.x, ff.y))
                updatedPosition = True
                
        
        if not updatedPosition:
            self.updatePosition()
    
    def getDistancetoFood(self, food_x, food_y):
        d = math.sqrt((self.x-food_x)**2 + (self.y-food_y)**2)
        return d

    def eatFood(self, food):
        nutrition = food.nutrition
        self.currentEnergy += nutrition
        if self.currentEnergy > self.energyCapacity:
            self.currentEnergy = self.energyCapacity
        food.setEaten()
        self.gotFoodOnce = True

    def getDNA(self):
        return [self.x, self.y, self.screen, self.god, self.color,  self.size, self.speed, self.energyCapacity, self.sight]

    def setAge(self, age):
        self.age = age
        #