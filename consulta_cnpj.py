import requests
import json

def consulta_cnpj_lista(cnpjs):
    url = 'https://www.receitaws.com.br/v1/cnpj/'
    querystring = {"token": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"}
    resultados = []

    for cnpj in cnpjs:
        response = requests.get(url + cnpj, params=querystring)
        informacoes = json.loads(response.text)
        resultados.append(informacoes)

    return resultados

def imprimir_informacoes_cnpj(informacoes):
    if informacoes.get('status') == 'OK':
        print("=" * 30 + " Informações do CNPJ " + "=" * 30)
        print(f"CNPJ: {informacoes['cnpj']}")
        print(f"Nome: {informacoes['nome']}")
        print(f"Tipo: {informacoes['tipo']}")
        print(f"Porte: {informacoes['porte']}")
        print(f"Data de Abertura: {informacoes['abertura']}")
        print(f"Situação: {informacoes['situacao']}")
        print(f"Endereço: {informacoes['logradouro']}, {informacoes['numero']}")
        print(f"Complemento: {informacoes['complemento']}")
        print(f"Bairro: {informacoes['bairro']}")
        print(f"CEP: {informacoes['cep']}")
        print(f"Município: {informacoes['municipio']}")
        print(f"UF: {informacoes['uf']}")
        print(f"Email: {informacoes['email']}")
        print(f"Telefone: {informacoes['telefone']}")
        print(f"Capital Social: {informacoes['capital_social']}")
        print(f"Atividade Principal: {informacoes['atividade_principal'][0]['text']}")
        print("Atividades Secundárias:")
        for atividade in informacoes['atividades_secundarias']:
            print(f" - {atividade['text']}")
        print("Quadro de Sócios:")
        for socio in informacoes['qsa']:
            print(f" - Nome: {socio['nome']}, Qualificação: {socio['qual']}")
        print("=" * 76)
    else:
        print("Erro ao consultar CNPJ. Status:", informacoes.get('status'))

# Exemplo de uso
lista_cnpjs = ['06990590000123', '33372251006278', '43996693000127']
informacoes = consulta_cnpj_lista(lista_cnpjs)

for info in informacoes:
    imprimir_informacoes_cnpj(info)
