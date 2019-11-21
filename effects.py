import pygame as pg
import pygame.gfxdraw
from settings import *
import random
vec = pg.math.Vector2

class JumpFx(pg.sprite.Sprite):
	def __init__(self, game, x, y, dir):
		self.groups = game.all_sprites, game.players
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game

		self.pos = vec(x, y)
		if dir == 1:
			self.pos = vec(x - 32, y + 16)
			self.angle = 0
		elif dir == 2:
			self.angle = 90
		elif dir == 3:
			self.angle = -90

		# self.angle = 0

		self.load_images()

		self.image = self.frames[0]
		self.rect = self.image.get_rect()

		self.current_frame = 0
		self.last_update = 0

	def load_images(self):
		self.frames = [self.game.spritesheet['impactJump'].get_image(52, 8, 293, 34),
								self.game.spritesheet['impactJump'].get_image(22, 89, 359, 67),
								self.game.spritesheet['impactJump'].get_image(26, 170, 355, 80),
								self.game.spritesheet['impactJump'].get_image(24, 272, 384, 128),
		]
		for i, a in enumerate(self.frames):
			self.frames[i] = pg.transform.scale(self.frames[i], (64, 16))
			self.frames[i] = pg.transform.rotate(self.frames[i], self.angle)

	def animate(self):
		now = pg.time.get_ticks()
		if now - self.last_update > 100:
			self.last_update = now
			self.current_frame = (self.current_frame + 1) % len(self.frames)
			bottom = self.rect.bottom
			self.image = self.frames[self.current_frame]
			self.rect.bottom = bottom

	def update(self):
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		if self.current_frame >= len(self.frames) -1:
			self.kill()
		self.animate()

class Explosion(pg.sprite.Sprite):
	def __init__(self, game, x, y, size=300):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game

		self.size = size
		self.image = pg.Surface((size, size), pg.SRCALPHA)
		self.rect = self.image.get_rect()
		self.pos = vec(x - int(self.size/3.3), y - int(self.size/3.3))
		# self.image.fill(WHITE)
		# pg.gfxdraw.filled_circle(self.image, int(self.size/3.3), int(self.size/3.3), int(self.size/3.3), BLACK)
		# pg.draw.circle(self.image, BLACK, (self.pos.x, self.pos.y), int(self.size/3.3))
		# self.image.blit(self.image)
		self.spawn_time = pg.time.get_ticks()
	def update(self):
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		if pg.time.get_ticks() - self.spawn_time < 80:
			pg.gfxdraw.filled_circle(self.image, int(self.size/3.3), int(self.size/3.3), int(self.size/3.3), BLACK)
		if pg.time.get_ticks() - self.spawn_time > 80:
			pg.gfxdraw.filled_circle(self.image, int(self.size/3.3), int(self.size/3.3), int(self.size/3.3), WHITE)
		if pg.time.get_ticks() - self.spawn_time > 160:
			self.kill()

class LoadingBar(pg.sprite.Sprite):
	def __init__(self, game, x, y, time):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.time = time
		self.image = pg.Surface((80, 10))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.left = x
		self.top = y
		self.maxwidth = 80
		self.progress = 0
		self.height = 10
		self.time = time
		self.start_time = pg.time.get_ticks()
	def update(self):
		now = pg.time.get_ticks()
		self.progress = now - self.start_time
		print(self.progress)
		pg.draw.rect(self.image, (255,255,255), pygame.Rect(self.left,self.top,self.maxwidth*self.progress,self.height))
