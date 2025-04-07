import requests
from bs4 import BeautifulSoup
import re

# URL da busca por "virus" no IMDb
url = "https://www.imdb.com/find/?q="
query = "virus"
final_url = url + query

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(final_url, headers=headers)
    response.raise_for_status()  # Verifica se houve erro na requisição

    soup = BeautifulSoup(response.text, 'html.parser')

   
    resultados = []

    itens = soup.find_all('li', class_="ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click find-result-item find-title-result")
    
    for idx, item in enumerate(itens):
         
            title_element = item.find('a', class_=re.compile('ipc-metadata-list-summary-item__t'))
            title = title_element.get_text(strip=True) if title_element else "Título não encontrado"
            
         
            year_element = item.find('span', class_=re.compile('ipc-metadata-list-summary-item__li'))
            year = year_element.get_text(strip=True) if year_element else "Ano não encontrado"
            
         
            link_element = item.find('a', class_=re.compile('ipc-metadata-list-summary-item__t'))
            link = "https://www.imdb.com" + link_element['href'] if link_element else "Link não encontrado"
            
   
            actors = []
            actors_section = item.find('ul', class_='ipc-metadata-list-summary-item__stl')
            if actors_section:
                actors_span = actors_section.find('span', class_='ipc-metadata-list-summary-item__li')
                if actors_span:
                    actors = [actor.strip() for actor in actors_span.get_text().split(',')]
            
           
            
            resultados.append({
                'título': title,
                'ano': year,
                'atores': actors,
                'link': link
            })

  
    print(f"Foram encontrados {len(resultados)} itens:")
    for i, item in enumerate(resultados, 1):
        print(f"\n{i}. {item['título']} ({item['ano']})")
        print(f"   Atores: {', '.join(item['atores']) if item['atores'] else 'Não disponível'}")
        print(f"   Link: {item['link']}")

except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
