import pygame
import numpy as np
import math
from animal import Animal
from food import Food
import pickle

class God:
    """ class contating all the animal varaibles and functions """
    def __init__(self, screen):
        self.screen = screen
        self.limit = pygame.display.get_surface().get_size()[0]
        self.matingRequests = []
        self.avgSpeed = []
        self.avgCapacity = []
        self.avgSight = []
        self.numberOfAnimals = []
        self.numberOfPlants = []
#
    def generateAnimals(self, n):
        self.animals = []
        colors = [(0,0,255), (0,255,0), (255,0,0)]
        for i in range(0, n):
            x = np.random.uniform(0, self.limit-1)
            y = np.random.uniform(0, self.limit-1)
            self.animals.append(Animal(x, y, self.screen, self, color=colors[i%3]))
        # return self.animals

    def generateFood(self, n):
        self.foods = []
        for i in range(0, n):
            x = np.random.uniform(0, self.limit-1)
            y = np.random.uniform(0, self.limit-1)
            food = Food(x, y, self.screen, self)
            food.draw()
            self.foods.append(food)
        # return self.foods

    def update(self):
        self.screen.fill((255, 255, 255))
        # print("UPDATED")
        for animal in self.animals:
            animal.update()
            # animal.draw()

        self.handleMating()

        for animal in self.animals:
            animal.draw()

        for i in range(0,1):
            p = np.random.uniform()
            if p <0.8:
                x = np.random.uniform(0, self.limit-1)
                y = np.random.uniform(0, self.limit-1)
                food = Food(x, y, self.screen, self)
                food.draw()
                self.foods.append(food)

        for food in self.foods:
            food.draw()

        self.log()

    def deadAnimalAlert(self, animal):
        if animal in self.animals:
            self.animals.remove(animal)

    def deadPlantAlert(self, food):
        if food in self.foods:
            self.foods.remove(food)

    def addMatingRequest(self, from_, to):
        self.matingRequests.append((from_, to))

    def handleMating(self, percent=0.1):
        final = self.getFinalMatingList()
        self.reproduce(final, percent)


    def getFinalMatingList(self):
        final = []
        mating = []
        for r in self.matingRequests:
            from_ = r[0]
            to = r[1]
            for rr in self.matingRequests:
                if not r == rr and not rr[0] in mating and not r[0] in mating:
                    if rr[0] == to and rr[1] == from_:
                        final.append((r[0], r[1]))
                        mating.append(r[0])
                        mating.append(r[1])
        return final

    def reproduce(self, final, percent):
        for animals in final:
            a1 = animals[0]
            a2 = animals[1]
            a1.setAge(0)
            a2.setAge(0)
            dna1 = a1.getDNA()
            dna2 = a2.getDNA()
            c1 = dna1[4]
            c2 = dna2[4]
            cc1 = c1[0]/2 + c2[0]/2
            cc2 = c1[1]/2 + c2[1]/2
            cc3 = c1[2]/2 + c2[2]/2
            # print(c1, c2, (cc1, cc2, cc3), a1==a2)

            dnaChild = [int(np.random.uniform(0,self.limit)), int(np.random.uniform(0,self.limit)), dna1[2], dna1[3], (cc1,cc2,cc3), dna1[5]]

            i = 6
            while i < len(dna1):
                p = np.random.uniform(0, 1)
                if p < 0.5:
                    dnaChild.append(np.random.normal(dna1[i], dna1[i]*percent))
                elif p<=1:
                    dnaChild.append(np.random.normal(dna2[i], dna2[i]*percent))
                i += 1
            self.animals.append(Animal(dnaChild[0], dnaChild[1], dnaChild[2], dnaChild[3], dnaChild[4], dnaChild[5], dnaChild[6], dnaChild[7], dnaChild[8]))
            # print("ADDED ANIMAL BROOO")
        self.matingRequests = []

    def log(self):
        speeds = 0
        capacties = 0
        sights = 0
        for a in self.animals:
            speeds += a.speed
            capacties += a.energyCapacity
            sights += a.sight
        if len(self.animals) > 0:
            self.avgSpeed.append(speeds/len(self.animals))
            self.avgCapacity.append(capacties/len(self.animals))
            self.avgSight.append(sights/len(self.animals))
            self.numberOfAnimals.append(len(self.animals))
            self.numberOfPlants.append(len(self.foods))

    def pickleFile(self, name='LOGS'):
        db = {}
        db['Speed'] = self.avgSpeed
        db['EnergyCapacity'] = self.avgCapacity
        db['Sight'] = self.avgSight
        db['Number of Animals'] = self.numberOfAnimals
        db['Number of Plants'] = self.numberOfPlants

        dbfile = open(name, 'ab')

        pickle.dump(db, dbfile)
        dbfile.close()