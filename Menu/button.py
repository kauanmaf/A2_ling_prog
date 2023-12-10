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
		self.__image = image
		self.__x_pos = pos[0]
		self.__y_pos = pos[1]
		self.__font = font
		self.__base_color, self.__hovering_color = base_color, hovering_color
		self.__text_input = text_input
		# criando texto
		self.__text = self.__font.render(self.__text_input, True, self.__base_color)
		# definindo texto como botão se não tiver imagem
		if self.__image is None:
			self.__image = self.__text
		self.__rect = self.__image.get_rect(center=(self.__x_pos, self.__y_pos))
		self.__text_rect = self.__text.get_rect(center=(self.__x_pos, self.__y_pos))

	def update(self, screen):
		if self.__image is not None:
			screen.blit(self.__image, self.__rect)
		screen.blit(self.__text, self.__text_rect)

	def checkForInput(self, position):
		# verificando se o mouse está dentro dos limites do retangulo
		if position[0] in range(self.__rect.left, self.__rect.right) and position[1] in range(self.__rect.top, self.__rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.__rect.left, self.__rect.right) and position[1] in range(self.__rect.top, self.__rect.bottom):
			self.__text = self.__font.render(self.__text_input, True, self.__hovering_color)
		else:
			self.__text = self.__font.render(self.__text_input, True, self.__base_color)