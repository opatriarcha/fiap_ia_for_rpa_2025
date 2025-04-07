import requests
from bs4 import BeautifulSoup
import os

url = "https://dados.gov.br/dados/conjuntos-dados/entidades-imunes-e-isentas-de-tributos-federais"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

os.makedirs('downloads_csv', exist_ok=True)

recursos_section = soup.find('h2', string='Recursos')
if recursos_section:
    recursos_div = recursos_section.find_next('div')
    for link in recursos_div.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.csv'):
            filename = os.path.join('downloads_csv', href.split('/')[-1])
            print(f'Baixando {filename}...')
            try:
                with requests.get(href, stream=True, headers=headers) as r:
                    r.raise_for_status()
                    with open(filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f'{filename} baixado com sucesso!')
            except Exception as e:
                print(f'Erro ao baixar {href}: {e}')
else:
    print('Seção de Recursos não encontrada')