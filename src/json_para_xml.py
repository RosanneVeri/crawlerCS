import json
import xml.etree.ElementTree as ET

def nome_tag(nome):
    return nome.replace(' ', '_').replace('/', '_')

def adicionar_elemento(pai, nome, valor):
    elemento = ET.SubElement(pai, nome_tag(nome))

    if isinstance(valor, dict):
        for chave, valor_chave in valor.items():
            adicionar_elemento(elemento, chave, valor_chave)

    elif isinstance(valor, list):
        for item in valor:
            adicionar_elemento(elemento, 'item', item)

    else:
        elemento.text = str(valor)

with open('src/processos.jsonl', 'r', encoding='utf-8') as arquivo:
    processos = []

    for linha in arquivo:
        processos.append(json.loads(linha))

print(f'Processos encontrados: {len(processos)}')

raiz = ET.Element('processos')

for processo in processos:
    elemento_processo = ET.SubElement(raiz, 'processo')

    for chave, valor in processo.items():
        adicionar_elemento(elemento_processo, chave, valor)

arvore = ET.ElementTree(raiz)

arvore.write(
    'src/processos.xml',
    encoding='utf-8',
    xml_declaration=True
)