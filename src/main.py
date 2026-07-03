import requests
from bs4 import BeautifulSoup


def obter_por_nr_processo(nr_processo):
  url = "https://www5.trf5.jus.br/cp/cp.do"
  session = requests.session()
  session =session.post(url, data={'tipo': 'xmlproc', 'filtro': nr_processo})
  return BeautifulSoup(session.content, 'html.parser')

def obter_por_cpf_cnpj():

  url = "https://www5.trf5.jus.br/cp/"
  session = requests.session()
  session = session.post(url, data={'tipo':'xmlcpf','filtro':'34.020.354/0001-10'})
  
  
""" link = "https://www5.trf5.jus.br/cp/cp.do"
session = requests.session()
session =session.post(link, data={'tipo': 'xmlproc', 'filtro': '0014481-40.2010.4.05.0000'})


objectBS4 = BeautifulSoup(session.content, 'html.parser') """


""" f = open('output.html', 'w', encoding='utf-8')
f.write(objectBS4.prettify())
f.close()
 """
 
#body = objectBS4.find('body')
# = body.find_all('table')

def obter_dt_autuado(table):
  dt = table.find_all('td')[1].text
  return dt[11:].strip()


def obter_processo(body):
  processo = body.find('body').find_all('p')[1]
  return processo.text.strip()[12:]

def ler_processos():
  with open('processos.txt', 'r') as f:
    processos = f.readlines()
  return [processo.strip() for processo in processos]

processos = ['0000881-39.2016.4.05.0000',
              '0013996-35.2011.4.05.8300',
              '0000007-41.2011.4.05.8403',
              '0009865-80.2014.4.05.0000',
              '0014481-40.2010.4.05.0000',
              '0005037-07.2013.4.05.8300']

for processo in processos:
  objectBS4 = obter_por_nr_processo(processo)
  table_dt_autuado = objectBS4.find_all('table')[0]
  body = objectBS4.find('body')

  dt_autuado = obter_dt_autuado(table_dt_autuado)
  nr_processo = obter_processo(body)
  print(dt_autuado)
  print(nr_processo)
#print(ler_processos())


#for _i, table in enumerate(tables):
#  print(f"Table {_i}:")
  #print(table.prettify())
 