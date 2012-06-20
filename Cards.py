#!/usr/bin/env python
# -*- encoding: utf-8 -*- 

import pygame
import random

from Global import load_image
from Deck import *


class Cards(pygame.sprite.Sprite):
	def __init__(self, x=0, y=0, suit=("heart", 1), deck=None):
		pygame.sprite.Sprite.__init__(self)
		self.back_image, self.back_rect = load_image('card-back.png')
		self.front_image, self.front_rect = load_image('cards/%s/%s.png' % suit)
		self.image, self.rect = self.back_image, self.back_rect

		self.rect.x = x
		self.rect.y = y
		self.back = False
		
		if(deck!=None):
			if(deck.type=='pile'):
				self.back = True
			else:
				self.back = False
		self.deck = deck
		self.suit = suit
	
	'''
	def show(self):
		print self.suit
	'''
	
	def move(self, x, y):
		if self.back == False and self.deck.type=='cat':
			self.rect.x = x
			self.rect.y = y
		'''	
			# A trick to show the cards underneath the current card
			i = 0
			for cards in self.next_cards():
				cards.rect.x = x
				cards.rect.y = y + (i * 25)
				i += 1
		'''
			
	def show_front(self):
		self.image = self.front_image
		self.back = False
	
	def show_back(self):
		self.image = self.back_image
		self.back = True
	
	def last_card_on_deck(self):
		if self in self.deck.list_cards[-1:]:
			return True
		else:
			return False  
	def move_to_front(self, cards_sprites):
		# Change the z value of the cards
		for card in self.next_cards():
			cards_sprites.move_to_front(card)
		
	def next_cards(self):
		cards = list()
		card_index = self.deck.list_cards.index(self)
		last_card_index = len(self.deck.list_cards)
		if card_index < last_card_index:
			for i in xrange(card_index , last_card_index):
				cards.append(self.deck.list_cards[i])
		return cards
