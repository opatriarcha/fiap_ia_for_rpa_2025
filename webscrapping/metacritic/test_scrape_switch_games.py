import unittest
import os
import pandas as pd

# Importa sua função
from ten_best_games_2025 import scrape_switch_games_completo

class TestIntegracaoScrapeSwitchGamesCompleto(unittest.TestCase):

    def test_gera_csv_com_10_linhas(self):
        # Executa a função de scraping real
        scrape_switch_games_completo()

        # Define o caminho do CSV
        csv_path = os.path.join(os.getcwd(), 'melhores_jogos_switch_completo.csv')

        # Verifica se o arquivo foi criado
        self.assertTrue(os.path.exists(csv_path), "O arquivo CSV não foi criado.")

        # Carrega o CSV
        df = pd.read_csv(csv_path)

        # Verifica se existem exatamente 10 linhas
        self.assertEqual(len(df), 10, "O CSV não contém exatamente 10 jogos.")

        # Limpa o ambiente: apaga o arquivo gerado após o teste
        if os.path.exists(csv_path):
            os.remove(csv_path)

if __name__ == "__main__":
    unittest.main()
