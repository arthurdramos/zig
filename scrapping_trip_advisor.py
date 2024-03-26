from bs4 import BeautifulSoup
import requests

url = 'https://www.tripadvisor.com.br/Restaurants-g294280-oa20-Brazil.html'
headers = {'User-Agent': 'Mozilla/5.0'}

page = requests.get(url,headers=headers)
print(page)
print(page.content.decode())
bs = BeautifulSoup(page.text, 'html.parser')

from bs4 import BeautifulSoup
import requests

def extract_links_from_page(html_content):
    bs = BeautifulSoup(html_content, 'html.parser')
    ul_tag = bs.find('ul', class_='geoList')
    if ul_tag:
        links = [a_tag['href'] for a_tag in ul_tag.find_all('a', href=True)]
        return links
    else:
        print("Nenhum elemento 'ul' com a classe 'geoList' encontrado.")
        return []

base_url = 'https://www.tripadvisor.com.br/Restaurants-g294280-oa{page}-Brazil.html'

current_page_number = 20
all_links = []

while current_page_number <= 100:
    current_page_url = base_url.format(page=current_page_number)
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(current_page_url, headers=headers)
    links_on_page = extract_links_from_page(page.content)
    all_links.extend(links_on_page)
    current_page_number += 20

for link in all_links:
    print(link)

