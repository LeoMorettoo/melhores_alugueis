import requests
import pandas as pd
from bs4 import BeautifulSoup
from unicodedata import normalize

def normalizeText(texto):
	return normalize('NFKD', texto).encode('ASCII','ignore').decode('ASCII')

def getSinopse(sinopse):
	descricao_attributos = {}
	for y in sinopse.find_all('li'):
		descricao_piece = normalizeText(y.getText().strip().lower())
		descricao_piece_array = descricao_piece.split(':')
		descricao_attributos[descricao_piece_array[0]] = descricao_piece_array[1]
	pass
	return descricao_attributos



base_url = 'http://www.visaoimoveisindaiatuba.com.br/'
busca_centro = 'pesquisa-de-imoveis/?locacao_venda=L&id_cidade%5B%5D=103&id_bairro%5B%5D=340&finalidade=residencial&dormitorio=0&garagem=1&vmi=&vma='
req = requests.get(base_url + busca_centro)
if req.status_code == 200:
	soup = BeautifulSoup(req.content, 'html.parser')
	alugueis = soup.find_all('div',class_='info')
	links = []
	for x in alugueis:
		links.append(x.find('a')['href'])
		pass

	for link in links:
		req = requests.get(base_url + link)
		if req.status_code == 200:
			soup = BeautifulSoup(req.content, 'html.parser')
			geo = soup.find('meta',{"name":"ICBM"})['content']
			valores = soup.find_all('div', class_='price-block')
			preco = valores[0].find('span').find('div').find_next_sibling().getText()
			condominio = valores[1].find('span').getText()
			iptu = valores[2].find('span').getText()

			descricoes = soup.find_all('ul', class_='property-amenities-list')
			descricoes_itens = {}
			sinopse_temp1 = getSinopse(descricoes[0])
			sinopse_temp2 = getSinopse(descricoes[1])
			descricoes_itens['sinopse'] = dict(**sinopse_temp1,**sinopse_temp2)
			print(descricoes_itens)
			exit()
		pass
