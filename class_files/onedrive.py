url = "https://fiapcom-my.sharepoint.com/:b:/g/personal/pf1997_fiap_com_br/Ee1CwbD_88NAu5smva50F38BbmBvQHztQkhyQGm0uN7Ybw?e=pDsOGi"

import requests

def downloadOneDriveFile(file_to_download, file_name = "downloaded_file"):

    with requests.get(url, stream=True) as response:
        if response.status_code == 200:
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  # 
                    file.write(chunk)
            print(f"Arquivo baixado com sucesso: {file_name}")
        else:
            print(f"Erro ao baixar o arquivo. Código de status: {response.status_code}")



def download_one_drive_file_full(url, file_name="downloaded_file"):
    """
    Faz o download de um arquivo do OneDrive sem usar chunks.

    :param url: URL pública do arquivo no OneDrive.
    :param file_name: Nome do arquivo de destino (opcional).
    """
   
    response = requests.get(url)

   
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)  # Escreve o conteúdo inteiro de uma vez
        print(f"Arquivo baixado com sucesso: {file_name}")
    else:
        print(f"Erro ao baixar o arquivo. Código de status: {response.status_code}")


download_one_drive_file_full(url)