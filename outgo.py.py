import requests
import csv
import os
from requests.exceptions import RequestException

def get_state_codes():
    url = "https://app.outgo.com.br/api/get_states"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [state['state_code'] for state in data]
    except RequestException as e:
        print(f"Erro ao acessar a API de estados: {e}")
        return []

def fetch_event_details(identificador, state_code, existing_ids):
    url = f"https://app.outgo.com.br/api/event/{identificador}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        event_id = data.get('id')

        if event_id not in existing_ids:
            producer_info = data.get('producer', {})
            place_info = data.get('place', {})
            address_info = place_info.get('address', {})

            row = [
                producer_info.get('name', ''),
                producer_info.get('cnpj', ''),
                producer_info.get('email', ''),
                producer_info.get('phone', ''),
                event_id,
                data.get('clientId', ''),
                data.get('name', ''),
                data.get('startDate', ''),
                producer_info.get('id', ''),
                producer_info.get('type', ''),
                producer_info.get('avatar_url', ''),
                producer_info.get('phone_outgo', ''),
                producer_info.get('cpf', ''),
                producer_info.get('instagram', ''),
                producer_info.get('category', ''),
                producer_info.get('category_text', ''),
                producer_info.get('subcategory', ''),
                producer_info.get('subcategory_text', ''),
                identificador,
                state_code,
                address_info.get('city', '')  # Ajusta para '' se a cidade não estiver presente
            ]
            return row
    except RequestException as e:
        print(f"Erro ao acessar a API para o evento {identificador}: {e}")
    except ValueError as e:
        print(f"Erro ao processar o JSON para o evento {identificador}: {e}")
    return None

def main():
    csv_file_path = 'event_details.csv'
    state_codes = get_state_codes()
    existing_ids = []

    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Pula o cabeçalho
            for row in reader:
                existing_ids.append(row[4])  # Supondo que 'Event ID' esteja na quinta coluna

    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not existing_ids:
            writer.writerow(['Producer Name', 'CNPJ', 'Email', 'Phone', 'Event ID', 'Client ID', 'Event Name', 'Start Date', 'Producer ID', 'Type', 'Avatar URL', 'Phone Outgo', 'CPF', 'Instagram', 'Category', 'Category Text', 'Subcategory', 'Subcategory Text', 'Identifier', 'State Code', 'City'])

        for state_code in state_codes:
            identificadores = []
            page = 1
            
            while True:
                url = f"https://app.outgo.com.br/api/agenda?state={state_code}&old=true&page={page}"
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    if page == 1 and 'featuredEvents' in data[0]:
                        identificadores.extend(event['identificador'] for event in data[0]['featuredEvents'] if 'identificador' in event)
                    if 'events' in data[0] and data[0]['events']:
                        identificadores.extend(event['identificador'] for event in data[0]['events'] if 'identificador' in event)
                        page += 1
                    else:
                        break
                except RequestException as e:
                    print(f"Erro ao acessar a API na página {page} ou não há mais dados para o estado {state_code}: {e}")
                    break

            for identificador in identificadores:
                row = fetch_event_details(identificador, state_code, existing_ids)
                if row:
                    writer.writerow(row)
                    existing_ids.append(row[4])  # Adiciona o ID na lista de IDs existentes

if __name__ == "__main__":
    main()
