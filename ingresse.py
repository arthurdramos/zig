import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# URLs das APIs
url_events = "https://api-site.ingresse.com/custom-categories/list/events"
url_experiences = "https://api-site.ingresse.com/custom-categories/experiences"

# Parâmetros da requisição
params = {
    "iso_code": "BRA",
    "language": "pt_br"
}

# Headers da requisição
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.5",
    "Origin": "https://www.ingresse.com",
    "Referer": "https://www.ingresse.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site"
}

# Função para fazer a requisição e processar os dados da API
def get_events_data(url):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        eventos = []
        for categoria in data:
            categoria_nome = categoria.get("name", "Sem Categoria")
            for evento in categoria.get("events", []):
                eventos.append({
                    "Categoria": categoria_nome,
                    "Evento ID": evento.get("event_id", "Sem ID"),
                    "Título": evento.get("title", "Sem Título"),
                    "Cidade": evento.get("place", {}).get("city", "Sem Cidade"),
                    "Estado": evento.get("place", {}).get("state", "Sem Estado"),
                    "Rua": evento.get("place", {}).get("street", "Sem Rua"),
                    "Data": evento.get("event_date", "Sem Data"),
                    "Imagem (small)": evento.get("images", {}).get("small", ""),
                    "Imagem (medium)": evento.get("images", {}).get("medium", ""),
                    "Imagem (large)": evento.get("images", {}).get("large", "")
                })
        return eventos
    else:
        print(f"Erro na requisição: {response.status_code}")
        return []

# Obter eventos de ambas as APIs
eventos_api = get_events_data(url_events)
experiences_api = get_events_data(url_experiences)

# Combinar os eventos de ambas as requisições
todos_eventos = eventos_api + experiences_api

# Converter para DataFrame
df_eventos_api = pd.DataFrame(todos_eventos)

# Autenticação com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('baladapp-1fa8424aeb8f.json', scope)
client = gspread.authorize(creds)

# Abrir a planilha
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1HOQAVdBBH8Oien3vLzuUdKtX6VfpJmH91i1UW-6QXWo/edit?gid=0')
worksheet = sheet.get_worksheet(0)  # Selecionar a primeira aba

# Ler os dados atuais da planilha e obter a coluna D (ID dos eventos)
existing_data = worksheet.get_all_values()
df_planilha = pd.DataFrame(existing_data[1:], columns=existing_data[0])  # Ignorar o cabeçalho na primeira linha

# Garantir que a coluna de ID seja do tipo inteiro, se possível
df_planilha['Evento ID'] = pd.to_numeric(df_planilha['Evento ID'], errors='coerce').dropna().astype(int)
ids_existentes = df_planilha['Evento ID'].tolist()

# Filtrar os eventos da API que não estão na planilha
df_eventos_api['Evento ID'] = pd.to_numeric(df_eventos_api['Evento ID'], errors='coerce').dropna().astype(int)
novos_eventos = df_eventos_api[~df_eventos_api['Evento ID'].isin(ids_existentes)]

# Se houver novos eventos, inseri-los na planilha
if not novos_eventos.empty:
    worksheet.append_rows(novos_eventos.values.tolist(), value_input_option="RAW")
    print(f"{len(novos_eventos)} novos eventos adicionados.")
else:
    print("Nenhum novo evento para adicionar.")
