import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_switch_games_completo():
    url = "https://www.metacritic.com/browse/games/score/metascore/all/switch/filtered"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    games = soup.find_all(attrs={"data-testid": "filter-results"})

    rankings = []
    titles = []
    metascores = []
    release_dates = []
    descriptions = []
    links = []
    image_urls = []

    for game in games[:10]:  # só os 10 primeiros
        # Ranking (posição no ranking)
        position = None

        # Nota do Metacritic
        score_tag = game.find('div', class_="c-siteReviewScore_background c-finderProductCard_metascoreValue u-flexbox-alignCenter g-height-100 g-outer-spacing-right-xsmall c-siteReviewScore_background-critic_xsmall")
        score = score_tag.text.strip() if score_tag else 'N/A'

        # Agora pegar todos os <span> internos para posição, título e descrição
        span_tags = game.find_all('span')

        release_date = 'N/A'
        description = 'N/A'
        title = 'N/A'

        meaningful_spans = [span for span in span_tags if not span.has_attr('class')]

        if len(meaningful_spans) >= 3:
            position = meaningful_spans[0].text.strip()    # posição no ranking
            title = meaningful_spans[1].text.strip()       # título do jogo
            description = meaningful_spans[2].text.strip() # descrição/gênero

        # Data de lançamento
        meta_div = game.find('div', class_="c-finderProductCard_meta")
        if meta_div:
            date_span = meta_div.find('span', class_="u-text-uppercase")
            release_date = date_span.text.strip() if date_span else 'N/A'

        # Link para o jogo
        a_tag = game.find('a')
        game_link = "https://www.metacritic.com" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'N/A'

       
        rankings.append(position)
        titles.append(title)
        metascores.append(score)
        release_dates.append(release_date)
        descriptions.append(description)
        links.append(game_link)

    # Criar DataFrame
    df = pd.DataFrame({
        'Posição': rankings,
        'Título': titles,
        'Nota Metacritic': metascores,
        'Data de Lançamento': release_dates,
        'Descrição': descriptions,
        'Link do Jogo': links
    })

    # Salvar CSV
    output_path = os.path.join(os.getcwd(), 'melhores_jogos_switch_completo.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Arquivo CSV final gerado: {output_path}")

if __name__ == "__main__":
    scrape_switch_games_completo()
