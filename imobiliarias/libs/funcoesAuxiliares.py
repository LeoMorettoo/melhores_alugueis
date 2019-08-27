import re
import requests
import os

from bs4 import BeautifulSoup
from bs4.element import Comment
from user_agent import generate_user_agent
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from unicodedata import normalize

def isEmpty(item):
	return True if item is None or item == [] else False

def onlyNumbers(val):
	pattern_only_numbers_brazil_pattern = '(\d+(?:\.\d{3})?)(,?\d{2})?'
	return float(re.search(pattern_only_numbers_brazil_pattern,val).group().replace('.','').replace(',','.')) if not isEmpty(val) else None

def normalizeText(texto):
	return normalize('NFKD', texto).encode('ASCII','ignore').decode('ASCII')

def fileName(name):
	return  name.replace('http://','').replace('https://','').replace('/','').replace('.','')+'.html'

def saveFile(file,name):
	savePath = os.path.dirname(os.path.abspath(__file__)) + r'/cache/'
	name = savePath + fileName(name)
	with open(name,'w+') as f:
		f.write(file)
	f.close()
	return name

def checkFile(name):
	fullPath = os.path.dirname(os.path.abspath(__file__)) + r'/cache/' + fileName(name)
	return os.path.exists(fullPath)

def openFile(name):
	fullPath = os.path.dirname(os.path.abspath(__file__)) + r'/cache/' + fileName(name)
	f = open(fullPath, "r")
	return f.read()

def getContentFromPage(url):
	if isEmpty(url):
		return None


	if checkFile(url):
		return openFile(url)

	try:
		headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
		session = requests.Session()
		retry = Retry(connect=3, backoff_factor=0.5)
		adapter = HTTPAdapter(max_retries=retry)
		session.mount('http://', adapter)
		session.mount('https://', adapter)
		req = session.get(url,timeout=5,headers=headers)
		if req.status_code == 200:
			saveFile(req.text,url)
			return req.content
		return None
	except Exception as e:
		return None

def parseHtml(html):
	removeTagArray = ['b','strong','i','em','mark','del','small','ins','sub','sup']
	page_content = BeautifulSoup(html, 'html5lib')

	for script in page_content(["script", "style","noscript"]):
		script.extract()

	for comentarios in page_content(text=lambda text: isinstance(text, Comment)):
		comentarios.extract()

	for toRemoveTag in page_content(removeTagArray):
		try:
			toRemoveTag.unwrap()
		except Exception as e:
			pass

	return BeautifulSoup(str(page_content), 'html5lib')
