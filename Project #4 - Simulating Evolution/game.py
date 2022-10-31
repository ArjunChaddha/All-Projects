"""
Area where the main logic is done and the pygame screen is dealt with
"""
import pygame
from animal import Animal
import numpy as np
from Rules import God

size = 500
pygame.init()
screen = pygame.display.set_mode([size, size])

GOD = God(screen)
GOD.generateAnimals(50)
GOD.generateFood(60)

RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    GOD.update()
    pygame.display.flip()
GOD.pickleFile("LOG")
pygame.quit()
#