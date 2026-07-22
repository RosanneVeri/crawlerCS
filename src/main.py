import requests
from bs4 import BeautifulSoup


processos = ['0000881-39.2016.4.05.0000',
              '0013996-35.2011.4.05.8300',
              '0000007-41.2011.4.05.8403',
              '0009865-80.2014.4.05.0000',
              '0014481-40.2010.4.05.0000',
              '0005037-07.2013.4.05.8300'
]

def obter_por_nr_processo(nr_processo):
  url = "https://www5.trf5.jus.br/cp/cp.do"
  session = requests.session()
  session =session.post(url, data={'tipo': 'xmlproc', 'filtro': nr_processo})
  return BeautifulSoup(session.content, 'html.parser')

def obter_por_cpf_cnpj(nr_cnpj):

  url = "https://www5.trf5.jus.br/cp/"
  session = requests.session()
  session = session.post(url, data={'tipo':'xmlcpf','filtro':'34.020.354/0001-10'})
  return BeautifulSoup(session.content, 'html.parser')
  
  
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

papeis = []
def obter_papel_envolvidos(table3):
  papel = table3.find_all('td')[0] 

  return papel.text.strip()  

def obter_nome_envolvidos(table3):
  nome = table3.find('b')
  return nome.text.strip()




   




 
for processo in processos:
  objectBS4 = obter_por_nr_processo(processo)
  table1 = objectBS4.find_all('table')[0]
  table3 = objectBS4.find_all('table')[2]
  body = objectBS4.find('body')

  nr_processo = obter_processo(body)
  dt_autuado = obter_dt_autuado(table1)
  papel_envolvido = obter_papel_envolvidos(table3)  
  nome_envolvido = obter_nome_envolvidos(table3)  


  print(nr_processo)
  print(dt_autuado)
  print(papel_envolvido)
  print(nome_envolvido)
 
#print(ler_processos())


#for _i, table in enumerate(tables):
#  print(f"Table {_i}:")
  #print(table.prettify())
 