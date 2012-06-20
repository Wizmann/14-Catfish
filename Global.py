import os,sys
import pygame

cards_pile=[]
suits = ["heart", "diamond", "club", "spade"]
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
score=0

def randomize(i_list):
	import random
	list_random = list()
	while i_list:
		element = random.choice(i_list)
		list_random.append(element)
		i_list.remove(element)
	return list_random

def load_image(name):
    fullname = os.path.join('images')
    fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert_alpha()
    return image, image.get_rect()
