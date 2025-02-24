url = "https://drive.google.com/file/d/1HPyQAByXAVjNYxIMQ6bhDt9ifBXyhM3G/view?usp=sharing"

import requests
from bs4 import BeautifulSoup

def downloadGoogleDriveFile(file_id, file_name="downloaded_file"):
    """
    Faz o download de um arquivo do Google Drive.

    :param file_id: ID do arquivo no Google Drive.
    :param file_name: Nome do arquivo de destino (opcional).
    """
    # URL de download
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    
    session = requests.Session() #TEM QUE MANTER OS COCKIES
    response = session.get(url, stream=True)

   
    if "confirm" in response.url:
        soup = BeautifulSoup(response.text, "html.parser")
        confirm_token = soup.find("input", {"name": "confirm"}).get("value")
        url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token}"
        response = session.get(url, stream=True)

    # Faz o download do arquivo
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  # Baixa em chunks de 8KB
                if chunk:  # Filtra chunks vazios
                    file.write(chunk)
        print(f"Arquivo baixado com sucesso: {file_name}")
    else:
        print(f"Erro ao baixar o arquivo. Código de status: {response.status_code}")


##inicia aqui
if __name__ == "__main__":
    
    file_id = "1HPyQAByXAVjNYxIMQ6bhDt9ifBXyhM3G"


    file_name = "spring_boot_reference.pdf"


    downloadGoogleDriveFile(file_id, file_name)