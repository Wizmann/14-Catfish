#!/usr/bin/env python
# -*- encoding: utf-8 -*- 

import pygame
import random
from Global import load_image
import Global
import time

class Deck(pygame.sprite.Sprite):
	def __init__(self, x, y, type='pile'):
		pygame.sprite.Sprite.__init__(self)

		self.image, self.rect = load_image('empty.png')
		self.list_cards = list()
		
		if(type=='pile'):
			self.image, self.rect = load_image('empty-ball.png')
			self.pile = True
		else:
			self.pile = False
		
		self.type = type
		self.x = x
		self.y = y

		self.rect.x = x
		self.rect.y = y
	def fill_deck(self,cards_num):
		for i in xrange(cards_num):
			card=Global.cards_pile.pop()
			self.list_cards.append(card)
		self.refresh_deck()
	def refresh_deck(self):
		for i in xrange(len(self.list_cards)):
			card=self.list_cards[i]
			card.rect.x = self.x
			card.rect.y = self.y
		
			if self.type!='pile':
				card.rect.y += i * 24
			else:
				card.back=True
				card.rect.y += i * 0.3
				card.rect.x -= i * 0.3
			card.deck = self
			self.list_cards[i]=card
	def is_add_ok(self,card):
		if(self.type!='fish'):
			return False
		sum=0
		for item in self.list_cards:
			sum+=item.suit[1]
		print sum
		if(sum+card.suit[1]<14):
			card.deck.list_cards.remove(card)
			card.deck=self
			self.list_cards.append(card)
			print card.deck.type
			return True
		elif(sum+card.suit[1]==14):
			
			card.deck.list_cards.remove(card)
			card.deck=self
			self.list_cards.append(card)
			#time.sleep(1)
			Global.score+=len(self.list_cards)
			self.list_cards=[]
			return True
		else:
			return False
	def deck_sum(self):
		sum=0
		for item in self.list_cards:
			sum+=item.suit[1]
		return sum
