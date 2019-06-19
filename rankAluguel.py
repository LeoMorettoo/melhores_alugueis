import alugueis
from math import sin, cos, sqrt, atan2, radians

def distancia(lat,lon):
	R = 6373.0

	lat1 = radians(-23.0857949)
	lon1 = radians(-47.2162222)
	lat2 = radians(lat)
	lon2 = radians(lon)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance

def valor_mensal(valores):
	valor_mensal = 0
	for key,val in valores.items():
		val = float(val.replace('.','').replace(',','.').replace('R$ ', ''))
		if key == 'locacao':
			valor_mensal += val
			pass
		elif key == 'condominio' :
			valor_mensal += val
			pass
		elif key == 'iptu':
			valor_mensal += val # já está dividido
			pass
		pass
	return valor_mensal

def nota_sinopse(sinopse):
	nota_final = 0
	remove_from_sinopse = ['operacao','cidade','condominio','iptu']
	dormitorios_nota = lambda n: n*1
	banheiros_nota = lambda n: n*2
	suites_nota = lambda n: n*4
	tipo_nota = lambda tipo: 10 if tipo != 'padrao' else 5
	area_util_nota = lambda area: 1 if area > 0 and area < 50 else 2 if area >= 50 and area < 100 else 3 if area >= 100 and area< 150 else 5
	only_number = lambda string: [int(s) for s in string.split() if s.isdigit()]
	for item in sinopse:
		if not item in remove_from_sinopse :
			try:
				if item == 'dormitorios':
					nota_final += dormitorios_nota(only_number(sinopse[item])[0])
					pass
				elif item == 'banheiros':
					nota_final += banheiros_nota(only_number(sinopse[item])[0])
					pass
				elif item == 'suites':
					nota_final += suites_nota(only_number(sinopse[item])[0])
					pass
				elif item == 'tipo do imovel':
					nota_final += tipo_nota(sinopse[item])
					pass
				elif item == 'area util':
					nota_final += area_util_nota(float(sinopse[item].replace('m2','')))
					pass
				pass
			except Exception as e:
				pass
			pass
		pass
	return nota_final

def nota_itens(itens):
	return len(itens)

alugueis_disponiveis = alugueis.alugueisDisponiveis()
for aluguel in alugueis_disponiveis:
	notas = []
	geo = aluguel['geo'].split(',')
	aluguel['ranking_objects'] = {}
	aluguel['ranking_objects']['distancia'] = distancia(float(geo[0]),float(geo[1]))
	aluguel['ranking_objects']['valor_mensal'] = valor_mensal(aluguel['valores'])
	notas.append(nota_sinopse(aluguel['descricoes']['sinopse']))
	notas.append(nota_itens(aluguel['descricoes']['itens_do_imovel']))
	try:
		if len(aluguel['descricoes']['itens_do_edificio']) > 0:
			notas.append(nota_itens(aluguel['descricoes']['itens_do_edificio']))
	except Exception as e:
		pass

	print(notas)
pass

