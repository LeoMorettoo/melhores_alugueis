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
	toMeters = lambda x: round(x * 1000,2)
	return toMeters(distance)

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

def nota_valor_mensal(valor):
	if valor < 500:
		return 1500
	elif valor > 500 and valor <= 600:
		return 1000
	elif valor > 600 and valor <= 700:
		return 950
	elif valor > 700 and valor <= 800:
		return 900
	elif valor > 800 and valor <= 900:
		return 850
	elif valor > 900 and valor <= 1000:
		return 800
	elif valor > 1000 and valor <= 1100:
		return 750
	elif valor > 1100 and valor <= 1200:
		return 700
	elif valor > 1200 and valor <= 1300:
		return 650
	elif valor > 1300 and valor <= 1400:
		return 600
	elif valor > 1400 and valor <= 1500:
		return 550
	elif valor > 1500 and valor <= 1600:
		return 500
	elif valor > 1600 and valor <= 1700:
		return 450
	elif valor > 1700 and valor <= 1800:
		return 400
	elif valor > 1800 and valor <= 1900:
		return 350
	elif valor > 1900 and valor <= 2000:
		return 300
	else:
		return 200

def nota_distancia(distancia):
	vel_pessoa_andando = round(1.38889,2) #m/s
	tempoSegundos = distancia/vel_pessoa_andando
	tempoMinutos = lambda x: round(x/60,2)
	tempoCaminhando = tempoMinutos(tempoSegundos)
	if tempoCaminhando < 1:
		return 155
	if tempoCaminhando > 1 and tempoCaminhando <= 1.30:
		return 150
	if tempoCaminhando > 1.30 and tempoCaminhando <= 2.00:
		return 145
	if tempoCaminhando > 2.00 and tempoCaminhando <= 2.30:
		return 140
	if tempoCaminhando > 2.30 and tempoCaminhando <= 3.00:
		return 135
	if tempoCaminhando > 3.00 and tempoCaminhando <= 3.30:
		return 130
	if tempoCaminhando > 3.30 and tempoCaminhando <= 4.00:
		return 125
	if tempoCaminhando > 4.00 and tempoCaminhando <= 4.30:
		return 120
	if tempoCaminhando > 4.30 and tempoCaminhando <= 5.00:
		return 115
	if tempoCaminhando > 5.00 and tempoCaminhando <= 5.30:
		return 110
	if tempoCaminhando > 5.30 and tempoCaminhando <= 6.00:
		return 105
	if tempoCaminhando > 6.00 and tempoCaminhando <= 6.30:
		return 100
	if tempoCaminhando > 6.30 and tempoCaminhando <= 7.00:
		return 95
	if tempoCaminhando > 7.00 and tempoCaminhando <= 7.30:
		return 90
	if tempoCaminhando > 7.30 and tempoCaminhando <= 8.00:
		return 85
	if tempoCaminhando > 8.00 and tempoCaminhando <= 8.30:
		return 80
	if tempoCaminhando > 8.30 and tempoCaminhando <= 9.00:
		return 75
	if tempoCaminhando > 9.00 and tempoCaminhando <= 9.30:
		return 70
	if tempoCaminhando > 9.30 and tempoCaminhando <= 10.00:
		return 65
	if tempoCaminhando > 10.00 and tempoCaminhando <= 10.30:
		return 60
	if tempoCaminhando > 10.30 and tempoCaminhando <= 11.00:
		return 55
	if tempoCaminhando > 11.00 and tempoCaminhando <= 11.30:
		return 50
	if tempoCaminhando > 11.30 and tempoCaminhando <= 12.00:
		return 45
	if tempoCaminhando > 12.00 and tempoCaminhando <= 12.30:
		return 40
	if tempoCaminhando > 12.30 and tempoCaminhando <= 13.00:
		return 35
	if tempoCaminhando > 13.00 and tempoCaminhando <= 13.30:
		return 30
	if tempoCaminhando > 13.30 and tempoCaminhando <= 14.00:
		return 25
	if tempoCaminhando > 14.00 and tempoCaminhando <= 14.30:
		return 20
	if tempoCaminhando > 14.30 and tempoCaminhando <= 15.00:
		return 15
	else:
		return 10

def nota_total(notas):
	nota_total = 0
	for tipo,nota in notas.items():
		nota_total += nota
		pass
	return nota_total

def set_notas():
	notas= []
	for aluguel in alugueis.alugueisDisponiveis():
		nota = {}

		nota['nota_valor_mensal'] = nota_valor_mensal(valor_mensal(aluguel['valores']))
		nota['nota_distancia'] = nota_distancia(distancia(aluguel['geo']['lat'],aluguel['geo']['lon']))
		nota['nota_sinopse'] = nota_sinopse(aluguel['descricoes']['sinopse'])
		nota['nota_itens_imovel'] = nota_itens(aluguel['descricoes']['itens_do_imovel'])
		try:
			if 'itens_do_edificio' in aluguel['descricoes']:
				nota['nota_itens_edificil'] = nota_itens(aluguel['descricoes']['itens_do_edificio'])
		except Exception as e:
			pass
		nota['nota_total'] = nota_total(nota)
		notas.append(nota)

	return notas

def ordernar_por_nota_total(notas):
	return notas.sort(key = lambda x: print(x)) 

print(ordernar_por_nota_total(set_notas()))


