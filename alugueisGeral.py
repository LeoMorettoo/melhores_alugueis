import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import re

def achou(item):
	return item is not None

def soNumeros(valor):
	soNumerosPadraoBrasil = '(\d+(?:\.\d{3})?)(,?\d{2})?'
	return float(re.search(soNumerosPadraoBrasil,valor).group().replace('.','').replace(',','.'))

def acharItem(soup,item_para_achar,patterns,apenasNUmeros = True):
	itens_achados = soup.find_all(text=re.compile(item_para_achar))
	for iten in itens_achados:
		for pattern in patterns:
			numero_de_itens = re.search(pattern, iten)
			if achou(numero_de_itens):
				return soNumeros(numero_de_itens.group()) if apenasNUmeros == True else numero_de_itens.group()
	return None

def acharNumeroDeBanheiros(soup,item_para_achar):
	patterns = ['((^' + item_para_achar + ')\s*)([1-9]*)','(([1-9]*)\s*)(' + item_para_achar + ')']
	return acharItem(soup,item_para_achar,patterns)

def acharNumeroDeQuartos(soup,item_para_achar):
	patterns = ['((^' + item_para_achar + ')\s*)([1-9]*)','(([1-9]*)\s*)(' + item_para_achar + ')']
	return acharItem(soup,item_para_achar,patterns)

def acharNumeroDeSuites(soup,item_para_achar):
	patterns = ['((^' + item_para_achar + ')\s*)([1-9]*)','(([1-9]*)\s*)(' + item_para_achar + ')']
	return acharItem(soup,item_para_achar,patterns)

def acharValorCondominio(soup,item_para_achar):
	patterns = ['((' + item_para_achar + ')\s)(\s?R\$\s?)?(\d+(?:\.\d{3})?)(,?\d{2})?(\s?R\$\s?)?']
	return acharItem(soup,item_para_achar,patterns)

def acharValorLocacao(soup,item_para_achar):
	if isinstance(item_para_achar, list):
		retorno = []
		for item in item_para_achar:
			patterns = ['((' + item + ')\s)(\s?R\$\s?)?(\d+(?:\.\d{3})?)(,?\d{2})?(\s?R\$\s?)?']
			temp = acharItem(soup,item,patterns)
			if (temp is not None):
				retorno.append(temp)
		if len(retorno) == 1:
			retorno = retorno[0]
	else:
		retorno = ''
		patterns = ['((' + item_para_achar + ')\s)(\s?R\$\s?)?(\d+(?:\.\d{3})?)(,?\d{2})?(\s?R\$\s?)?']
		retorno = acharItem(soup,item_para_achar,patterns)
	return retorno

url = 'https://www.gpsimoveis.imb.br/imovel/casa-com-4-quartos-para-locacao-r-4-500-00-jardim-portal-dos-ipes-indaiatuba-sp/CA10386-CS0'
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
req = requests.get(url,timeout=5,headers=headers)
if req.status_code == 200:
	soup = BeautifulSoup(req.content, 'html5lib')
	[s.extract() for s in soup('script')]
	banheiros = acharNumeroDeBanheiros(soup, '[Bb]anheiros?')
	quartos = acharNumeroDeQuartos(soup, '[Qq]uartos?')
	suites = acharNumeroDeSuites(soup, '[Ss]uítes?')
	locacao = acharValorLocacao(soup, ['[Aa]luguel','[Ll]ocação'])
	condominio = acharValorCondominio(soup, '[Cc]ondominio')
	print(condominio)
	print(banheiros)
	print(quartos)
	print(suites)
	print(locacao)
	exit()
