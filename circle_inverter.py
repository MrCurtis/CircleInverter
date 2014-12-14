import pygame
import sys
import random
import cmath

def PixToCoor(pixx, image, rescale, width, height, portrait):
	z = pixx[0]*1.0 - pixx[1]*1.0j # y coor is negative to take in to account change from 'computer science' to 'mathematical' coordinates.
	if portrait == 1:
		z = rescale/width * (z - width/2 + height*1j/2) # takes centre of image to origin and rescales
	else:
		z = rescale/height * (z - width/2 + height*1j/2)
	return z

def CoorToPix(z, image, rescale, width, height, portrait):
	if portrait == 1:
		z = width/rescale * z + width/2 - height*1j/2
 	else:
		z = height/rescale * z + width/2 - height*1j/2
	return (round(z.real),round(-z.imag))

pygame.init()

screen_res = (1280, 800)

screen = pygame.display.set_mode(screen_res)

image1 = pygame.image.load('Add your file here')
image2 = pygame.Surface(image1.get_size())

height = image1.get_height()*1.0 - 1
width = image1.get_width()*1.0 - 1
if width < height:
	portrait = 1 
else:
	portrait = 0

image1.lock()
for x in range(0,image1.get_width()):
	for y in range(0,image1.get_height()):
		z = PixToCoor((x,y), image1, 6, width, height, portrait)
		if z == 0:
			image2.set_at((0,0),(100,100,100,255))
		else:
			z = 1/z
			pix = CoorToPix(z,image1,6, width, height, portrait)
			if pix[0] >= 0 and pix[0] < image1.get_width() and pix[1] >= 0 and pix[1] < image1.get_height():
				image2.set_at((x,y),image1.get_at(pix))
			else:
				image2.set_at((x,y),(100,100,100,255))
image1.unlock()

if image2.get_height() > screen.get_height():
	scale = screen.get_height()*1.0/image2.get_height()
	image2 = pygame.transform.rotozoom(image2,0,scale)

loop = 1
while(loop):
	for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				sys.exit()
				loop = 0
	screen.blit(image2,(0,0))
	pygame.display.flip()
	pygame.time.delay(200)
