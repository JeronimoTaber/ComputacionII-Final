import pygame, sys
from classes.settings import *
from classes.level import Level
from classes.debug import debug
class Game:
	def __init__(self):
		  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		#game name
  
		pygame.display.set_caption('MP GAME')
		self.clock = pygame.time.Clock()

		self.level = Level()
	
	def run(self, reader, writer):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			debug('hello')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)
   