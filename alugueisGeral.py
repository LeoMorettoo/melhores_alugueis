import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import re

def achou(item):
	return item is not None

def acharNumeroDeBanheiros(soup,item_para_achar):
	itens_achados = soup.find_all(text=re.compile(item_para_achar))
	patterns = ['((^[Bb]anheiros?)\s*)([1-9]*)','(([1-9]*)\s*)([Bb]anheiros?)']
	for banheiro in itens_achados:
		for pattern in patterns:
			numero_de_banheiros = re.search(pattern, banheiro)
			if achou(numero_de_banheiros):
				return numero_de_banheiros.group()

def acharNumeroDeQuartos(soup,item_para_achar):
	itens_achados = soup.find_all(text=re.compile(item_para_achar))
	patterns = ['((^[Qq]uartos?)\s*)([1-9]*)','(([1-9]*)\s*)([Qq]uartos?)']
	for quarto in itens_achados:
		for pattern in patterns:
			numero_de_quartos = re.search(pattern, quarto)
			if achou(numero_de_quartos):
				return numero_de_quartos.group()

def acharNumeroDeSuites(soup,item_para_achar):
	itens_achados = soup.find_all(text=re.compile(item_para_achar))
	patterns = ['((^[Ss]uítes?)\s*)([1-9]*)','(([1-9]*)\s*)([Ss]uítes?)']
	for suite in itens_achados:
		for pattern in patterns:
			numero_de_suites = re.search(pattern, suite)
			if achou(numero_de_suites):
				return numero_de_suites.group()

url = 'https://www.gpsimoveis.imb.br/imovel/casa-com-4-quartos-para-locacao-r-4-500-00-jardim-portal-dos-ipes-indaiatuba-sp/CA10386-CS0'
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
req = requests.get(url,timeout=5,headers=headers)
if req.status_code == 200:
	soup = BeautifulSoup(req.content, 'html5lib')
	[s.extract() for s in soup('script')]
	banheiros = acharNumeroDeBanheiros(soup, '[Bb]anheiros?')
	quartos = acharNumeroDeQuartos(soup, '[Qq]uartos?')
	suites = acharNumeroDeSuites(soup, '[Ss]uítes?')
	print(banheiros)
	print(quartos)
	print(suites)
	exit()
