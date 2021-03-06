import re
import json
from time import sleep

from funcoesAuxiliares import *

def findOccurrencesByBasicTexts(raw_item):
	return page_content.find_all(text=re.compile(raw_item))

def dataExtractionPatterns(itensBasicPattern,patternClassType):
	lib_of_patterns = {}
	lib_of_patterns['number_of'] = ['(\s?)(:?)(\s?)([0-9]+)(\s?)(PATTERHERE\s*)|(PATTERHERE\s*)(\s?)(:?)(\s?)([0-9]+)(\s?)']
	lib_of_patterns['cost_of'] =  ['((PATTERHERE)\s)(\s?R\$\s?)?(\d+(?:\.\d{3})?)(,?\d{2})?(\s?R\$\s?)?','(\s?R\$\s?)?(\d+(?:\.\d{3})?)(,?\d{2})?(\s?R\$\s?)?']
	if isinstance(itensBasicPattern, list):
		result_patterns = []
		for itenPattern in itensBasicPattern:
			for pattern in lib_of_patterns[patternClassType]:
				result_patterns.append(pattern.replace('PATTERHERE',itenPattern))
		return result_patterns
	else:
		return [patterns.replace('PATTERHERE',itensBasicPattern) for patterns in lib_of_patterns[patternClassType] ]

def applyComplexRegexPatterByClassType(itens,patternClassType):
	if isEmpty(itens):
		return None

	found_itens = []
	for iten in itens:
		for pattern in patternClassType:
			try:
				search = re.search(pattern, iten.string)
				if not isEmpty(search):
					found_itens.append(search)
			except Exception as e:
				pass

	if not isEmpty(found_itens):
		return found_itens

	return None

def findPossibleNearCorrectValue(itens,patterns):
	raw_itens = []
	for iten in itens:

		parent = iten.find_parent()
		if not isEmpty(parent):
			raw_itens.append(applyComplexRegexPatterByClassType(parent,patterns))

		uncles = parent.find_next_sibling()
		if not isEmpty(uncles):
			raw_itens.append(applyComplexRegexPatterByClassType(uncles,patterns))

		grandParent = parent.find_parent()
		if not isEmpty(grandParent):
			raw_itens.append(applyComplexRegexPatterByClassType(grandParent,patterns))
	return raw_itens

def filterPossibleResult(results):
	ns = []
	for result in results:
		try:
			for x in result:
				ns.append(onlyNumbers(x.group()))
			removeDuplicates = lambda x : list(dict.fromkeys(x))
			maiorValor = lambda x : max(x)
			ns = removeDuplicates(ns)
			ns = maiorValor(ns)
			return ns
		except Exception as e:
			return None

def findByText(itensBasicPattern,patternClassType,patterns = []):
	basic_itens = []
	results = []
	if isinstance(itensBasicPattern, list):
		for iten in itensBasicPattern:
			basic_itens.append(findOccurrencesByBasicTexts(iten))
	else:
		basic_itens.append(findOccurrencesByBasicTexts(itensBasicPattern))

	for iten in basic_itens:
		patterns = dataExtractionPatterns(itensBasicPattern,patternClassType)

		raw_result = applyComplexRegexPatterByClassType(iten,patterns)
		if not isEmpty(raw_result):
			results.append(raw_result)

		raw_result = findPossibleNearCorrectValue(iten,patterns)
		if not isEmpty(raw_result):
			results.append(raw_result)

	result = filterPossibleResult(results)
	return result

urls = [
		# 'https://www.gpsimoveis.imb.br/imovel/casa-com-2-quartos-para-alugar-120-m-por-1300-jardim-morada-do-sol-indaiatuba-sp/CA1608-CS0'
		'http://www.visaoimoveisindaiatuba.com.br/alugar/Indaiatuba/Casa/Padrao/Jardim-Sao-Conrado/893402'
		]
imoveis = []
for url in urls:
	imovel = {}
	try:
		page_content = parseHtml(getContentFromPage(url))
		imovel['numero_de_banheiros'] = findByText('[Bb]anheiros?', patternClassType="number_of")
		imovel['numero_de_quartos'] = findByText(['[Qq]uartos?','[Dd]ormitórios?'], patternClassType="number_of")
		imovel['numero_de_suites'] = findByText('[Ss]uítes?', patternClassType="number_of")
		imovel['valor_de_locacao'] = findByText(['[Aa]luguel','[Ll]ocação'] , patternClassType="cost_of")
		imovel['valor_de_condominio'] = findByText('[Cc]ondomínio' , patternClassType="cost_of")
		imovel['valor_de_IPTU'] = findByText('IPTU', patternClassType="cost_of")
		imoveis.append(imovel)
	except Exception as e:
		raise e
	sleep(2)

print(json.dumps(imoveis,indent=4))
exit()
