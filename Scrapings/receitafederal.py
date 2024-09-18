import time
import csv
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('baladapp-1fa8424aeb8f.json', scope)
client = gspread.authorize(creds)

sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1_MlNW_Ce6_5fLvqs6U-mMLCzsqPMPc0oIm_ZkE9IFIM/edit?gid=0#gid=0').sheet1

def limpar_cnpj(cnpj):
    return re.sub(r'\D', '', cnpj)

def consultar_cnpj(cnpj):
    cnpj_limpo = limpar_cnpj(cnpj)
    url = f'https://receitaws.com.br/v1/cnpj/{cnpj_limpo}'

    headers = {
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        return {'status': 'ERROR', 'message': f'Erro: {response.status_code}'}

def ler_cnpjs(sheet):
    return sheet.col_values(1)

def salvar_csv(dados, nome_arquivo):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["status", "ultima_atualizacao", "cnpj", "tipo", "porte", "nome", "fantasia", "abertura",
                         "atividade_principal", "atividades_secundarias", "natureza_juridica", "logradouro",
                         "numero", "complemento", "cep", "bairro", "municipio", "uf", "email", "telefone", "efr",
                         "situacao", "data_situacao", "motivo_situacao", "situacao_especial", "data_situacao_especial",
                         "capital_social", "qsa", "billing"])

        for dado in dados:
            if dado['status'] == 'OK':
                writer.writerow([
                    dado.get("status", ""),
                    dado.get("ultima_atualizacao", ""),
                    dado.get("cnpj", ""),
                    dado.get("tipo", ""),
                    dado.get("porte", ""),
                    dado.get("nome", ""),
                    dado.get("fantasia", ""),
                    dado.get("abertura", ""),
                    "|".join([f"{atv['code']} - {atv['text']}" for atv in dado.get("atividade_principal", [])]),
                    "|".join([f"{atv['code']} - {atv['text']}" for atv in dado.get("atividades_secundarias", [])]),
                    dado.get("natureza_juridica", ""),
                    dado.get("logradouro", ""),
                    dado.get("numero", ""),
                    dado.get("complemento", ""),
                    dado.get("cep", ""),
                    dado.get("bairro", ""),
                    dado.get("municipio", ""),
                    dado.get("uf", ""),
                    dado.get("email", ""),
                    dado.get("telefone", ""),
                    dado.get("efr", ""),
                    dado.get("situacao", ""),
                    dado.get("data_situacao", ""),
                    dado.get("motivo_situacao", ""),
                    dado.get("situacao_especial", ""),
                    dado.get("data_situacao_especial", ""),
                    dado.get("capital_social", ""),
                    "|".join([f"{q.get('nome', '')} - {q.get('qual', '')} - {q.get('pais_origem', '')} - {q.get('nome_rep_legal', '')} - {q.get('qual_rep_legal', '')}" for q in dado.get("qsa", [])]),
                    f"free: {dado['billing'].get('free', '')}, database: {dado['billing'].get('database', '')}"
                ])
            else:
                writer.writerow([dado['status'], dado.get('message', '')] + [''] * 27)

cnpjs = ler_cnpjs(sheet)

dados_coletados = []
for i in range(0, len(cnpjs), 3):
    for cnpj in cnpjs[i:i+3]:
        dados_coletados.append(consultar_cnpj(cnpj))
    time.sleep(60)


salvar_csv(dados_coletados, 'dados_cnpjs.csv')
