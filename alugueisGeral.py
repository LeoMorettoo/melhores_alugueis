import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import re

def achou(item):
	return item != []

def acharNumeroDeBanheiros(soup,item_para_achar):
	itens_achados = soup.find_all(text=re.compile(item_para_achar))
	patterns = ['/((^([Bb])anheiros?)\s*)([1-9]*)/g','/((([1-9]*))\s*(([Bb])anheiros?))/g']
	for banheiro in itens_achados:
		for pattern in patterns:
			print(banheiro)
			print(re.search('Banheiros', banheiro))
			if achou(banheiro):
				print('achou')
				pass
			else:
				print('nao achou')
				pass
			pass
		#print(banheiros)
	exit()
	#return soup.find_all(text=re.compile('Banheiros')

url = 'https://www.gpsimoveis.imb.br/imovel/casa-com-4-quartos-para-locacao-r-4-500-00-jardim-portal-dos-ipes-indaiatuba-sp/CA10386-CS0'
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
req = requests.get(url,timeout=5,headers=headers)
if req.status_code == 200:
	soup = BeautifulSoup(req.content, 'html5lib')
	[s.extract() for s in soup('script')]
	banheiros = acharNumeroDeBanheiros(soup, '[Bb]anheiros?')
	print(banheiros)
	exit()
