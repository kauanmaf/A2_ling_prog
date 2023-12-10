import os
import sys
project_root = os.path.dirname(os.path.dirname(__file__)) 
sys.path.append(project_root)

class Button():
	"""
	Classe cujas instâncias são os botões que fazem o menu funcionar

	Atributos:
	----------
	- ``__image`` (pygame.Surface):
		A imagem que representa o botão
	- ``__x_pos (int):``
		A posição do botão ao longo do eixo x
	- ``__y_pos (int):``
		A posição do botão ao longo do eixo y
	- ``__font (pygame.Font):``
		A fonte do texto do botão
	- ``__base_color (pygame.Color)``
		A cor normal do texto do botão
	- ``__text_input (str):``
		O texto do botão
	- ``__text (pygame.Surface):``
		O texto com a cor normal que deve ter
	- ``-rect (pygame.Rect)``
		O retângulo que representa a dimensão e a posição da imagem na tela
	- ``text_rec (pygame.rect)``
		O retângulo que representa a dimensão e a posição da imagem na tela

	Métodos:
	--------
	- ``update(screen)``:
		Atualiza o estado do botão, colocando-o na tela.

	- ``checkForInput(position)``:
		Verifica se o mouse está dentro do range do retângulo 

	- ``update(screen)``:
		Atualiza o estado do botão, colocando-o na tela.
	"""

	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)