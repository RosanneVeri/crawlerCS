
import requests
import json
from bs4 import BeautifulSoup

CNPJ = "34.020.354/0001-10"

processos = [
    '0000881-39.2016.4.05.0000',
    '0013996-35.2011.4.05.8300',
    '0000007-41.2011.4.05.8403',
    '0009865-80.2014.4.05.0000',
    '0014481-40.2010.4.05.0000',
    '0005037-07.2013.4.05.8300',
    '0007575-16.2003.4.05.8201'
]


def obter_por_nr_processo(nr_processo):
    url = "https://www5.trf5.jus.br/cp/cp.do"

    response = requests.post(
        url,
        data={
            'tipo': 'xmlproc',
            'filtro': nr_processo
        },
        timeout=30
    )

    response.raise_for_status()

    return BeautifulSoup(response.content, 'html.parser')


def obter_por_cpf_cnpj(cnpj):
    url = "https://www5.trf5.jus.br/cp/"

    response = requests.post(
        url,
        data={
            'tipo': 'tipo_xmlcpf',
            'filtro': cnpj
        },
        timeout=30
    )

    response.raise_for_status()

    return BeautifulSoup(response.content, 'html.parser')


def obter_dt_autuado(table):
    tds = table.find_all('td')

    if len(tds) < 2:
        return ''

    return tds[1].get_text(strip=True)[11:]


def obter_processo(body):
    paragrafos = body.find_all('p')

    if len(paragrafos) < 2:
        return ''

    return paragrafos[1].get_text(strip=True)[12:]

def obter_nr_legado(body):
    paragrafos = body.find_all('p')

    if len(paragrafos) > 2:
        return paragrafos[2].get_text(strip=True).strip('()')

    return ""

def obter_papel_envolvidos(tr):
    tds = tr.find_all('td')

    if not tds:
        return ''

    return tds[0].get_text(strip=True)


def obter_nome_envolvidos(tr):
    nome = tr.find('b')

    if nome is None:
        return ''

    return nome.get_text(strip=True)


def obter_data_movimentacoes(tr):
    data = tr.find('a')

    if data is None:
        return ''

    return data.get_text(strip=True)


def obter_texto_movimentacoes(tr):
    tds = tr.find_all('td')

    if len(tds) < 2:
        return ''

    return tds[1].get_text(strip=True)


# Grava os processos no arquivo JSONL
with open('processos.jsonl', 'w', encoding='utf-8') as arquivo:

    for processo in processos:

        try:
            print(f'\nConsultando processo: {processo}')

            objectBS4 = obter_por_nr_processo(processo)

            tables = objectBS4.find_all('table')

            if len(tables) < 3:
                print(f'Não foram encontradas tabelas para {processo}')
                continue

            body = objectBS4.find('body')

            if body is None:
                print(f'Página sem conteúdo para {processo}')
                continue

            nr_processo = obter_processo(body)

            nr_legado = obter_nr_legado(body)

            dt_autuado = obter_dt_autuado(tables[0])

            table3 = tables[2]

            envolvidos = []

            for tr in table3.find_all('tr'):

                papel = obter_papel_envolvidos(tr)
                nome = obter_nome_envolvidos(tr)

                if not papel or not nome:
                    continue

                if papel == "RELATOR":

                    nome = nome.split(':', 1)[-1].strip(12)
                    envolvidos.append(nome)

                else:

                    envolvidos.append({
                        papel: nome
                    })

            list_movimentacoes = []

            for table in tables[5:]:

                coTrs = table.find_all('tr')

                if not coTrs:
                    continue

                data = obter_data_movimentacoes(coTrs[0])

                texto = ''

                for tr in coTrs[1:]:

                    texto += obter_texto_movimentacoes(tr) + ' '

                if data:

                    list_movimentacoes.append({
                        'data': data.replace('Em ', ''),
                        'texto': texto.strip()
                    })

            dados_processo = {
                'Processo': nr_processo,
                "Número legado" : nr_legado,
                'Data de autuação': dt_autuado,
                'Envolvidos': envolvidos,
                'Movimentações': list_movimentacoes
            }

            # Salvar os dados
            arquivo.write(
                json.dumps(dados_processo, ensure_ascii=False) + '\n'
            )

            arquivo.flush()

            print(f'Processo salvo: {nr_processo}')

        except requests.RequestException as erro:
            print(f'Erro na consulta de {processo}: {erro}')

        except Exception as erro:
            print(f'Erro ao processar {processo}: {erro}')

print('\nCrawler finalizado!')
