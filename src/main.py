import requests
from bs4 import BeautifulSoup


processos = [
    '0000881-39.2016.4.05.0000',
    '0013996-35.2011.4.05.8300',
    '0000007-41.2011.4.05.8403',
    '0009865-80.2014.4.05.0000',
    '0014481-40.2010.4.05.0000',
    '0005037-07.2013.4.05.8300'
]


def obter_por_nr_processo(nr_processo):
    url = "https://www5.trf5.jus.br/cp/cp.do"

    session = requests.session()

    session = session.post(
        url,
        data={
            'tipo': 'xmlproc',
            'filtro': nr_processo
        }
    )

    return BeautifulSoup(session.content, 'html.parser')


def obter_por_cpf_cnpj(nr_cnpj):
    url = "https://www5.trf5.jus.br/cp/"

    session = requests.session()

    session = session.post(
        url,
        data={
            'tipo': 'xmlcpf',
            'filtro': nr_cnpj
        }
    )

    return BeautifulSoup(session.content, 'html.parser')


def obter_dt_autuado(table):
    dt = table.find_all('td')[1].text

    return dt[11:].strip()


def obter_processo(body):
    processo = body.find('body').find_all('p')[1]

    return processo.text.strip()[12:]


def obter_papel_envolvidos(tr):
    papel = tr.find_all('td')[0]

    return papel.text.strip()


def obter_nome_envolvidos(tr):
    nome = tr.find('b')

    return nome.text.strip()


def obter_data_movimentacoes(tr):
    data = tr.find('a')

    return data.text.strip()


def obter_texto_movimentacoes(tr):
    texto = tr.find_all('td')[1]

    return texto.text.strip()[3:]


for processo in processos:

    objectBS4 = obter_por_nr_processo(processo)

    tables = objectBS4.find_all('table')

    table1 = tables[0]
    table3 = tables[2]

    body = objectBS4.find('body')

    nr_processo = obter_processo(body)

    dt_autuado = obter_dt_autuado(table1)

    envolvidos = []
    

    for tr in table3.find_all('tr'):

        papel = obter_papel_envolvidos(tr)

        nome = obter_nome_envolvidos(tr)

        if papel == "RELATOR":

            nome = nome.split(':', 1)[1].strip()

            envolvidos.append(nome)

        else:

            envolvidos.append({
                papel: nome
            })


    list_movimentacoes = []

    for table in tables[4:]:

        for tr in table.find_all('tr'):

            tds = tr.find_all('td')

            link = tr.find('a')

            if len(tds) >= 2 and link:

                data = obter_data_movimentacoes(tr)

                texto = obter_texto_movimentacoes(tr)

                list_movimentacoes.append({
                    'data': data,
                    'texto': texto
                })


    print('Processo:', nr_processo)
    print('Data de autuação:', dt_autuado)
    print('Envolvidos:', envolvidos)
    print('Movimentações:', list_movimentacoes)
    print('--------------------------------')