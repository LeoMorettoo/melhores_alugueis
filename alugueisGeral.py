import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import re

def itemfound(item):
	return True if item is not None and not item == [] else False

def onlyNumbers(val):
	pattern_only_numbers_brazil_pattern = '(\d+(?:\.\d{3})?)(,?\d{2})?'
	return float(re.search(pattern_only_numbers_brazil_pattern,val).group().replace('.','').replace(',','.'))

def getItenWithREGEX(itens_achados,patterns):
	for iten in itens_achados:
		for pattern in patterns:
			try:
				numero_de_itens = re.search(pattern, iten)
			except Exception as e:
				return None
			if itemfound(numero_de_itens):
				return numero_de_itens.group()
	return None

def getNearElemements(itens_achados):
	array_near_elements = []
	for item in itens_achados:
		item_parent = item.find_parent()
		if itemfound(item_parent):
			item_parent_siblings = item_parent.find_next_sibling()
			if itemfound(item_parent_siblings):
				array_near_elements += item_parent_siblings
	return array_near_elements

def getItem(soup,item_para_achar,patterns,apenasNUmeros = True):
	itens_achados = soup.find_all(text=re.compile(item_para_achar))
	if not itemfound(itens_achados):
		return None
	item = getItenWithREGEX(itens_achados,patterns)
	if itemfound(item):
		return onlyNumbers(item) if apenasNUmeros == True else item
	else:
		patterns = ['((' + item_para_achar + ')\s)(\s?R\$\s?)?(\d+(?:\.\d{3})?)(,?\d{2})?(\s?R\$\s?)?','(\s?R\$\s?)?(\d+(?:\.\d{3})?)(,?\d{2})?(\s?R\$\s?)?']
		item = getItenWithREGEX(getNearElemements(itens_achados),patterns)
		if itemfound(item):
			return onlyNumbers(item) if apenasNUmeros == True else item
	return None

def getBanheiros(soup,item_para_achar):
	patterns = ['(\s?)(:?)(\s?)([0-9]+)(\s?)(' + item_para_achar + '\s*)|(' + item_para_achar + '\s*)(\s?)(:?)(\s?)([0-9]+)(\s?)']
	return getItem(soup,item_para_achar,patterns)

def getQuartos(soup,item_para_achar):
	patterns = ['(\s?)(:?)(\s?)([0-9]+)(\s?)(' + item_para_achar + '\s*)|(' + item_para_achar + '\s*)(\s?)(:?)(\s?)([0-9]+)(\s?)']
	return getItem(soup,item_para_achar,patterns)

def getSuites(soup,item_para_achar):
	patterns = ['(\s?)(:?)(\s?)([0-9]+)(\s?)(' + item_para_achar + '\s*)|(' + item_para_achar + '\s*)(\s?)(:?)(\s?)([0-9]+)(\s?)']
	return getItem(soup,item_para_achar,patterns)

def acharCondominio(soup,item_para_achar):
	patterns = ['(\s?)(:?)(\s?)([0-9]+)(\s?)(' + item_para_achar + '\s*)|(' + item_para_achar + '\s*)(\s?)(:?)(\s?)([0-9]+)(\s?)']
	return getItem(soup,item_para_achar,patterns)

def getLocacao(soup,item_para_achar):
	if isinstance(item_para_achar, list):
		retorno = []
		for item in item_para_achar:
			patterns = ['((' + item + ')\s)(\s?R\$\s?)?(\d+(?:\.\d{3})?)(,?\d{2})?(\s?R\$\s?)?']
			temp = getItem(soup,item,patterns)
			if itemfound(temp):
				retorno.append(temp)
		if len(retorno) == 1:
			retorno = retorno[0]
	else:
		retorno = ''
		patterns = ['((' + item_para_achar + ')\s)(\s?R\$\s?)?(\d+(?:\.\d{3})?)(,?\d{2})?(\s?R\$\s?)?']
		retorno = getItem(soup,item_para_achar,patterns)
	return retorno if itemfound(retorno) else None

urls = ['https://www.gpsimoveis.imb.br/imovel/casa-com-4-quartos-para-locacao-r-4-500-00-jardim-portal-dos-ipes-indaiatuba-sp/CA10386-CS0','http://www.visaoimoveisindaiatuba.com.br/alugar/Indaiatuba/Casa/Padrao/Jardim-Sao-Conrado/893402']
imoveis = []
for url in urls:
	imovel = {}
	headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
	req = requests.get(url,timeout=10,headers=headers)
	if req.status_code == 200:
		page_content = BeautifulSoup(req.content, 'html5lib')
		[s.extract() for s in page_content('script')]
		try:
			imovel['numero_de_banheiros'] = getBanheiros(page_content, '[Bb]anheiros?')
			imovel['numero_de_quartos'] = getQuartos(page_content, '[Qq]uartos?')
			imovel['numero_de_suites'] = getSuites(page_content, '[Ss]uítes?')
			imovel['valor_de_locacao'] = getLocacao(page_content, ['[Aa]luguel','[Ll]ocação'])
			imovel['valor_de_condominio'] = acharCondominio(page_content, '[Cc]ondomínio')
			imovel['valor_de_IPTU'] = acharCondominio(page_content, 'IPTU')
		except Exception as e:
			raise e
		imoveis.append(imovel)
print(imoveis)
exit()
