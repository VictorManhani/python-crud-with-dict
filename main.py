# -*- encoding: utf-8 -*-

# CONSULTA JSON
# https://pt.stackoverflow.com/questions/225725/arquivo-para-dicion%C3%A1rio

# ELIMINAR VALOR DE UM DICIONARIO
# https://pt.stackoverflow.com/questions/355886/eliminar-valor-de-um-dicion%C3%A1rio-em-python

# ALTERAR RETIRAR ITEM DICIONARIO EM PYTHON 
# https://www.pythonprogressivo.net/2018/10/Como-Adicionar-Alterar-Retirar-Item-Dicionario.html

import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, NoTransition
from kivy.uix.button import Button

import json

Config.set('graphics', 'width', str('400'))
Config.set('graphics', 'height', str('500'))

#with open('main.kv', encoding='utf-8') as f:
#	Builder.load_string(f.read())

Builder.load_string('''
<Inicio>:
	BoxLayout:
		orientation: 'vertical'
		Label:
			id: info
			text: 'Hello World'
			size_hint: 1, .1
			align: 'center'
			valign: 'center'
			halign: 'center'
		BoxLayout:
			orientation: 'vertical'
			ScrollView:
				do_scroll_x: False
				do_scroll_y: True
				size_hint: 1, .6
				BoxLayout:
					id: box
					orientation: 'vertical'
					size_hint: 1, None
					height: self.minimum_height
					spacing: dp('5')
					padding: dp('5')
		BoxLayout:
			size_hint: 1, .15
			TextInput:
				id: valor
				size_hint: .2, 1
				text_hint: 'Valor'
				font_size: sp('30')
			Button:
				text: 'C'
				size_hint: .2, 1
				on_release:
					root.salvar()
					#root.mudar_tela('sobre', 'no', 'left')
			Button:
				text: 'R'
				size_hint: .2, 1
				on_release:
					root.ler()
					#root.mudar_tela('sobre', 'no', 'left')
			Button:
				text: 'U'
				size_hint: .2, 1
				on_release:
					root.atualizar()
					#root.mudar_tela('sobre', 'no', 'left')
			Button:
				text: 'D'
				size_hint: .2, 1
				on_release:
					root.deletar()
					#root.mudar_tela('sobre', 'no', 'left')
		BoxLayout:
			size_hint: 1, .15
			TextInput:
				id: texto
				text_hint: 'Salvar'
				font_size: sp('30')
				text_size: self.size

<Sobre>:
	BoxLayout:
		orientation: 'vertical'
		Label:
			text: 'GESTOR: Versão 0.1'
		Button:
			text: 'Inicio'
			on_release:
				self.parent.parent.mudar_tela('inicio', 'no', 'left')
''')

bd = dict()

class Geral():
	def mudar_tela(self, nome_tela, tipo_transicao = 'Slide', direcao = 'left'):
		if (tipo_transicao == 'Slide'):
			self.manager.transition = SlideTransition()
		else:
			self.manager.transition = NoTransition()
		self.manager.transition.direction = direcao
		self.manager.current = nome_tela

class Inicio(Screen, Geral):
	n = 1
	def salvar(self):
		if not bd.get(self.ids.texto.text):
			bd[self.n] = self.ids.texto.text
			self.ids.info.text = bd[self.n]
			self.n += 1
			self.ids.info.text = "Salvo!"
			self.puxar_todos(bd)
			self.criar_botoes(bd)
				
	def deletar(self):
		n = int(self.ids.valor.text)
		if bd.get(n):
			bd.pop(n)
			self.ids.info.text = str(bd.items())
		else:
			self.ids.info.text = "Item não existe"
		self.puxar_todos(bd)
		self.criar_botoes(bd)

	def atualizar(self):
		if self.ids.valor.text != None and self.ids.valor.text != '':
			n = int(self.ids.valor.text)
			if bd.get(n):
				bd[n] = self.ids.texto.text
				self.ids.info.text = "Atualizado!"
		self.puxar_todos(bd)
		self.criar_botoes(bd)
		
	def ler(self):
		#n = int(self.ids.valor.text)
		#if bd.get(n):
		#	self.ids.info.text = bd[n]
		#self.criar_botoes(bd)
		self.consulta_tudo()
	
	def consulta_arquivo(self):
		with open('data.json', "r") as arquivo:
			for li in arquivo:
				li = li.replace("'", "\"")
				li = li.replace("/n", "")
				li = json.loads(li)
				
	def consulta_tudo(self):
		with open('data.json', 'r', encoding = 'utf-8') as arquivo:
			dic = {}
			for linha in arquivo:
				linha = linha.replace("'", "")
				
				b = linha.split(',')
				
				for i in b:
					c  = i.split(':')
					c[0] = c[0].replace("{","")
					c[0] = c[0].replace("}","")
					c[0] = c[0].replace(":","")
					c[1] = c[1].replace("{","")
					c[1] = c[1].replace("}","")
					c[1] = c[1].replace(":","")
					dic[c[0]] = c[1]
		self.criar_botoes(dic)
		
	def puxar_todos(self, dicionario):
		for i, j in dicionario.items():
			self.ids.info.text = f"{i}:{j} \n"
			
	def criar_botoes(self, dicionario):
		self.ids.box.clear_widgets()
		for i, j in dicionario.items():
			self.ids.box.add_widget(Builder.load_string(f'''
Button:
	text: {i}
	size_hint: 1, None
	height: dp('30')
'''))
			self.ids.box.add_widget(Builder.load_string(f'''
Label:
	text: {j}
	size_hint: 1, None
	height: dp('30')
'''))

	def load(self):
		with open('data.json', 'r', encoding = 'utf-8') as arq:
			doc = json.load(arq) # Ler o arq json
			self.ids.texto.text = doc
			self.ids.label.text = 'Arquivo Carregado!'
	
	def save(self):
		with open('data.json', 'w', encoding = 'utf-8') as arq:
			docTexto = self.ids.texto.text
			docJson = json.dumps(docTexto) # Converter o data em json
			arq.write(docJson) # Escrever no arq json
			self.ids.label.text = 'Arquivo Salvo!'
            
class Sobre(Screen, Geral):
	pass

sm = ScreenManager()
sm.add_widget(Inicio(name = 'inicio'))
#sm.add_widget(Configuracao(name = 'configuracao'))
sm.add_widget(Sobre(name = 'sobre'))

class MainApp(App):
	#icon = 'icones\logo.png'
	title = 'Gestor'
	def build(self):
		return sm

if __name__ == "__main__":
	MainApp().run()

