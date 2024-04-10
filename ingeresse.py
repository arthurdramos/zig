import pandas
import requests
import json
import time
from tabulate import tabulate
from bs4 import BeautifulSoup

def clean_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def lnd_tck_ingresse_api():
    events_data = []
    for state in ['mg']:
        print("=" * 40)
        print("Consultando estado:", state)
        print("=" * 40)
        
        # Consulta p/ shows e festivais
        print("Consultando shows e festivais...")
        BASE_URL = (
            'https://event-search.ingresse.com/1'
            f'?state={state}'
            '&from=now-6h'
            '&orderBy=sessions.dateTime'
            '&size=200'
            '&category=shows-e-festivais'
        )
        req = requests.get(BASE_URL)
        print('Status da requisição para', state, ':', req.status_code)
        ret = json.loads(req.content)
        
        if ret['data']['total'] > 0:
            for hit in ret['data']['hits']:
                events_data.append(extract_event_data(hit['_source'], state))

        # Consulta p/ festas e baladas
        print("Consultando festas e baladas...")
        BASE_URL = (
            'https://event-search.ingresse.com/1'
            f'?state={state}'
            '&from=now-6h'
            '&orderBy=sessions.dateTime'
            '&size=200'
            '&category=festas-e-baladas'
        )
        
        req = requests.get(BASE_URL)
        print('Status da requisição para', state, ':', req.status_code)
        ret = json.loads(req.content)
        
        if 'hits' in ret['data']:  
            if ret['data']['total'] > 0:
                for hit in ret['data']['hits']:
                    events_data.append(extract_event_data(hit['_source'], state))
        else:
            print("Nenhum dado retornado para festas e baladas.")

        print('Esperando 10 segundos...')
        time.sleep(10)
    
    return events_data

def extract_event_data(event_data, state):
    clean_event = {}
    clean_event['state'] = state
    clean_event['title'] = event_data.get('title', 'Não especificado')
    clean_event['date'] = event_data['sessions'][0]['dateTime']
    clean_event['location'] = event_data['place']['name']
    clean_event['address'] = event_data['place'].get('address', 'Não especificado')
    clean_event['description'] = clean_html_tags(event_data.get('description', 'Não especificado'))
    clean_event['contact'] = event_data.get('contact', {}).get('phones', 'Não especificado')
    clean_event['email'] = event_data.get('contact', {}).get('email', 'Não especificado')
    clean_event['price'] = event_data.get('price', 'Não especificado')
    clean_event['age_rating'] = event_data.get('ageRating', 'Não especificado')
    clean_event['category'] = event_data.get('category', 'Não especificado')
    clean_event['tickets_available'] = event_data.get('ticketsAvailable', 'Não especificado')
    clean_event['ticket_link'] = event_data.get('ticketsUrl', 'Não especificado')
    clean_event['organizer'] = event_data.get('organizer', {}).get('name', 'Não especificado')
    clean_event['website'] = event_data.get('organizer', {}).get('website', 'Não especificado')
    clean_event['tags'] = event_data.get('tags', [])
    clean_event['image'] = event_data.get('image', 'Não especificado')
    clean_event['duration'] = event_data.get('duration', 'Não especificado')
    clean_event['attendance_mode'] = event_data.get('attendanceMode', 'Não especificado')
    return clean_event

events_data = lnd_tck_ingresse_api()
for event in events_data:
    print("=" * 40)
    print("Estado:", event['state'])
    print("Título:", event['title'])
    print("Data:", event['date'])
    print("Localização:", event['location'])
    print("Endereço:", event['address'])
    print("Descrição:", event['description'])
    print("Contato:", event['contact'])
    print("E-mail de contato:", event['email'])
    print("Preço:", event['price'])
    print("Classificação etária:", event['age_rating'])
    print("Categoria:", event['category'])
    print("Ingressos disponíveis:", event['tickets_available'])
    print("Link para comprar ingressos:", event['ticket_link'])
    print("Organizador:", event['organizer'])
    print("Website do organizador:", event['website'])
    print("Tags:", event['tags'])
    print("Imagem:", event['image'])
    print("Duração:", event['duration'])
    print("Modo de participação:", event['attendance_mode'])
