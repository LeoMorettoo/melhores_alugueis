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
	pass
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
			valor_mensal += val/12
			pass
		pass
	return valor_mensal

alugueis_disponiveis = alugueis.alugueisDisponiveis()
for aluguel in alugueis_disponiveis:

	for key,val in aluguel['descricoes']['sinopse'].items():
		# sinopse
		# itens_do_imovel
		# itens_do_edificio
		print(key,val)
		pass
	exit()
	geo = aluguel['geo'].split(',')
	aluguel['ranking_objects'] = {}
	aluguel['ranking_objects']['distancia'] = distancia(float(geo[0]),float(geo[1]))
	aluguel['ranking_objects']['valor_mensal'] = valor_mensal(aluguel['valores'])
	pass

