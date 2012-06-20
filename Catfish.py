#!/usr/bin/env python
# -*- encoding: utf-8 -*- 

import sys,os
import pygame
from Cards import Cards
import Global
from pygame.locals import *
from Deck import *

class Catfish:
	def __init__(self,width=800,height=600):
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))

		self.background = pygame.image.load("images/background.jpg")
		self.backgroundRect = self.background.get_rect()
		self.screen.blit(self.background, self.backgroundRect)
		pygame.display.set_caption("小喵钓鱼")
		pygame.display.flip()
		
		self.fill_card_pile()
	
		self.victory = False
	def fill_card_pile(self):
		for suit in Global.suits:
			for num in Global.numbers:
				Global.cards_pile.append(Cards(suit=(suit,num)))
		Global.cards_pile=Global.randomize(Global.cards_pile)
		'''
		for item in cards_pile:
			item.show()
		'''
		self.deck_packages = {
			# user cards_packages
			'deck_cat_0':			 Deck(160, 400, type="cat"),
			'deck_cat_1':			 Deck(320, 400, type="cat"),
			'deck_cat_2':			 Deck(480, 400, type="cat"),
			'deck_cat_3':			 Deck(640, 400, type="cat"),
			
			# computer cards_package
			'deck_pile':		Deck(15, 210, type="pile"),
			
			# fish cards_packages
			'deck_fish_0':		Deck(160, 20, type="fish"),
			'deck_fish_1':		Deck(320, 20, type="fish"),
			'deck_fish_2':		Deck(480, 20, type="fish"),
			'deck_fish_3':		Deck(640, 20, type="fish"),
		}
		
		self.deck_packages['deck_pile'].fill_deck(42)
		for deck in self.deck_packages:
			if(deck!='deck_pile'):
				self.deck_packages[deck].fill_deck(1)
	
	def restart(self):
		self.fill_card_pile()
		Global.score=0
		self.update_sprites()
		self.victory = False

	
	def update_sprites(self,refresh=False):
		decks = list()

		# Adding cards_packages in the Group of Sprites
		decks.extend(self.deck_packages.values())
		for deck in self.deck_packages:
			deck_type=deck.split('_')[1]
			if(refresh):
				self.deck_packages[deck].refresh_deck()
			for card in self.deck_packages[deck].list_cards:
				if(deck_type!='pile' and card.back==False):
					card.show_front()
				else:
					card.show_back()
				decks.append(card)
		decks = tuple(decks)
		self.cards_sprites = pygame.sprite.LayeredUpdates(decks)
	
	def change_cards(self):
		try:
			cat_name='deck_cat_%d' % random.randint(0,3)
			#print cat_name
			now_card=self.deck_packages[cat_name].list_cards.pop()
			if(now_card.back==True):
				self.deck_packages[cat_name].list_cards.append(now_card)
				return
			else:
				now_card.back=True
				now_card.show_back()
			new_card=self.deck_packages['deck_pile'].list_cards.pop()
			
			
			#print now_card.back,new_card.back
			
			now_card.back=True
			now_card.deck=self.deck_packages['deck_pile']
			
			new_card.back=True
			new_card.deck=self.deck_packages[cat_name]
			
			now_card_list=[]
			now_card_list.append(now_card)
			new_card_list=[]
			new_card_list.append(new_card)
			now_card_list.extend(self.deck_packages['deck_pile'].list_cards)
			new_card_list.extend(self.deck_packages[cat_name].list_cards)
			self.deck_packages['deck_pile'].list_cards=now_card_list
			self.deck_packages['deck_pile'].refresh_deck()
			self.deck_packages[cat_name].list_cards=new_card_list
			self.deck_packages[cat_name].refresh_deck()
			
		except:
			print 'change_cards exception'
			return
			
	def check_empty_deck(self):
		if(not self.deck_packages['deck_pile'].list_cards):
			#print 'deck_pile is empty'
			return
		cat_list=['deck_cat_%d' % i for i in xrange(4)]
		for item in cat_list:
			#print item,self.deck_packages[item].list_cards
			if(not self.deck_packages[item].list_cards):
				#print item
				new_card=self.deck_packages['deck_pile'].list_cards.pop()
				new_card.back=True
				new_card.deck=self.deck_packages[item]
				self.deck_packages[item].list_cards.append(new_card)
				self.deck_packages['deck_pile'].refresh_deck()
				self.deck_packages[item].refresh_deck()
				
				#for test in self.deck_packages[item].list_cards:
				#	print test.suit
	def check_victory(self):
		fish_card_list=[]
		fish_list=['deck_fish_%d' % i for i in xrange(4)]
		for item in fish_list:
			fish_card_list.append(self.deck_packages[item].deck_sum())
		cat_card_list=[]
		cat_list=['deck_cat_%d' % i for i in xrange(4)]
		cat_list.append('deck_pile')
		for item in cat_list:
			cat_card_list.extend(self.deck_packages[item].list_cards)
		
		for cat in cat_card_list:
			for fish in fish_card_list:
				#print cat.suit[1],fish
				if(cat.suit[1]+fish<=14):
					return False
		#print 'vi'
		return True
				
	def remove_all_cards(self):
		for key in self.deck_packages:
			self.deck_packages[key].list_cards=[]
		
	def MainLoop(self):
		running = True
		self.update_sprites()
		self.victory = False
		
		clicked_card = None
		click_offset = ''
		pos_initial_card_click = None
		clicked = 0
		self.victory = False
		
		while running:
			refresh=False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					running = False
				elif event.type == KEYDOWN and event.key == K_v:
					self.victory=True
				elif event.type == KEYDOWN and event.key == K_RETURN:
					if self.victory == True:
						self.victory = False
						self.restart()
				elif event.type == MOUSEBUTTONDOWN:
					if(self.victory): break
					
					click_x, click_y = event.pos
					#print "Click: (x: %d, y: %d)" % (click_x, click_y)
					
					sprites = self.cards_sprites.sprites()
					sprites.reverse()
					for sprite in sprites:
						pos_card_x = sprite.rect.x
						pos_card_y = sprite.rect.y

						size_card_x = sprite.rect.width
						size_card_y = sprite.rect.height
						
						if click_x > pos_card_x and click_x < pos_card_x+size_card_x \
							and click_y > pos_card_y and click_y < pos_card_y+size_card_y:
							
							clicked_card = sprite
							if(sprite.__class__.__name__=='Deck'):
								clicked_card=None
								break
								
							#sprite.move_to_front(self.cards_sprites)
							#self.cards_sprites.move_to_front(sprite)
							if(sprite.deck.type=='pile'):
								clicked_card=None
								self.change_cards()
								break
							else:
								if(sprite.deck.type=='cat'):
									sprite.move_to_front(self.cards_sprites)
									#self.cards_sprites.move_to_front(sprite)
									#print id(self.cards_sprites.get_top_sprite())
									#print id(sprite)
									if(sprite.back==True):
										sprite.show_front()
							click_offset = [click_x-pos_card_x, click_y-pos_card_y]
							pos_initial_card_click = [pos_card_x, pos_card_y]
							
							
							#print "The card position: (x: %d, y: %d)" % (pos_card_x, pos_card_y)
							#print "click_offset: (x: %d, y: %d)" % (click_offset[0], click_offset[1])
							
							break
					clicked = 1
				elif event.type == MOUSEMOTION:
					x, y = event.pos
					if clicked == 1 and clicked_card!=None:
						clicked_card.move(x-click_offset[0], y-click_offset[1])
				elif event.type == MOUSEBUTTONUP:
					if self.victory == True:
						break
					x, y = event.pos
					
					if clicked == 1 and clicked_card!=None:
						move_back = True
						
						sprites = self.cards_sprites.sprites()
						sprites.reverse()

						for sprite in sprites:
							if (x > sprite.rect.x and x < (sprite.rect.x + sprite.rect.width)) \
								and (y > sprite.rect.y and y < (sprite.rect.y + sprite.rect.height)) \
								and clicked_card != sprite and clicked_card.deck.type=='cat':

								cards_dest = sprite
								if sprite.__class__.__name__ == "Cards":
									cards_dest = sprite.deck
									
								move_back = cards_dest.is_add_ok(clicked_card)
								break
							
						if move_back is True:
							clicked_card.move(pos_initial_card_click[0], pos_initial_card_click[1])
					self.check_empty_deck()
					self.victory=self.check_victory()
					clicked = 0
					clicked_card = None
					refresh = True

			self.screen.blit(self.background, self.backgroundRect)
			self.container_fish = pygame.image.load("images/container.png")
			self.containerRect_fish = self.container_fish.get_rect()
			self.containerRect_fish.y = 4
			self.containerRect_fish.x = 152
			self.screen.blit(self.container_fish, self.containerRect_fish)
			
			self.container_cat = pygame.image.load("images/container.png")
			self.containerRect_cat = self.container_cat.get_rect()
			self.containerRect_cat.y = 382
			self.containerRect_cat.x = 152
			self.screen.blit(self.container_cat, self.containerRect_cat)
			if(self.victory):
				self.remove_all_cards()
				self.update_sprites(True)
				self.victory_screen = pygame.image.load("images/victory.png")
				self.victory_screenRect = self.victory_screen.get_rect()
				sr = self.screen.get_rect()
				self.victory_screenRect.centerx = sr.centerx
				self.victory_screenRect.centery = sr.centery
				self.screen.blit(self.victory_screen, self.victory_screenRect)
				
				font = pygame.font.Font("Helvetica.otf", 24)
				text = font.render('You caught %d fish. Good job!' % Global.score, True, (0, 0, 0))
				textRect = text.get_rect()
				textRect.centerx = self.victory_screenRect.centerx + 130
				textRect.centery = self.victory_screenRect.centery + 84
				self.screen.blit(text, textRect)
			if(refresh): self.update_sprites(refresh)
			self.cards_sprites.draw(self.screen)
			pygame.display.flip()
