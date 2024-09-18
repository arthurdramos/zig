import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('baladapp-1fa8424aeb8f.json', scope)
client = gspread.authorize(creds)

spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1NPN2VSAyLIvAsYm-6GOC6n3YQPx4LS1-i3SwLUpRT_o/edit#gid=0'

spreadsheet = client.open_by_url(spreadsheet_url)
worksheet = spreadsheet.sheet1

api_url = 'https://www.sympla.com.br/api/v1/search'

headers = {
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'pt-BR,pt;q=0.5',
    'content-type': 'application/json',
    'origin': 'https://www.sympla.com.br',
    'referer': 'https://www.sympla.com.br/eventos/show-musica-festa/em-alta',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

def get_events(page):
    payload = {
        "service": "/v4/mapsearch",
        "params": {
            "city": "",
            "formats": "80,87,89",
            "has_banner": "1",
            "location_score": "month_trending_score",
            "only": "name,start_date,end_date,images,event_type,duration_type,location,id,global_score,start_date_formats,end_date_formats,url,company,type",
            "page": page,
            "sort": "month_trending_score",
            "themes": "99",
            "type": "normal"
        }
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Erro na requisição: {response.status_code} para a página {page}')
        return None

all_events = []
for page in range(1, 324):
    print(f'Obtendo eventos da página {page}...')
    data = get_events(page)
    if data:
        events = data.get('result', {}).get('events', {}).get('data', [])
        for event in events:
            all_events.append(event)
    time.sleep(1)

records = []
for event in all_events:
    record = {
        "ID": event.get("id"),
        "Name": event.get("name"),
        "Start Date": event.get("start_date_formats", {}).get("pt"),
        "End Date": event.get("end_date_formats", {}).get("pt"),
        "Organizer": event.get("organizer", {}).get("name"),
        "Organizer Email": event.get("organizer", {}).get("email"),
        "Location": event.get("location", {}).get("name"),
        "City": event.get("location", {}).get("city"),
        "State": event.get("location", {}).get("state"),
        "Address": f"{event.get('location', {}).get('address')} {event.get('location', {}).get('address_num')}",
        "Zip Code": event.get("location", {}).get("zip_code"),
        "Event Type": event.get("event_type"),
        "Start Date (ISO)": event.get("start_date"),
        "End Date (ISO)": event.get("end_date")
    }
    records.append(record)

df = pd.DataFrame(records)

worksheet.clear()
worksheet.update([df.columns.tolist()] + df.values.tolist())

print("Dados atualizados na planilha com sucesso!")
