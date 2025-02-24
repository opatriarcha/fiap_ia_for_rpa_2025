import csv
import json
import pickle
#pip install pandas pyyaml pickle json csv


# 1. Leitura de arquivo de texto linha por linha
def read_file_line_by_line(filename):
    with open(filename, 'r') as file:
        for line in file:
            print(line.strip())

# 2. Leitura de arquivo de texto completo
def read_entire_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# 3. Leitura de arquivo grande em chunks
def read_large_file_in_chunks(filename, chunk_size=1024):
    with open(filename, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

# 4. Leitura de arquivo binário
def read_binary_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

# 5. Leitura de arquivo binário em chunks
def read_binary_file_in_chunks(filename, chunk_size=1024):
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

# 6. Leitura de arquivo CSV com `csv.reader`
def read_csv_file(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

# 7. Leitura de arquivo CSV com `csv.DictReader`
def read_csv_file_as_dict(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)

# 8. Leitura de arquivo JSON
def read_json_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# 9. Leitura de arquivo JSON linha por linha
def read_json_lines(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield json.loads(line)

# 10. Leitura de arquivo XML
import xml.etree.ElementTree as ET

def read_xml_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

# 11. Leitura de arquivo YAML
import yaml

def read_yaml_file(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

# 12. Leitura de arquivo em lotes (batch)
def read_file_in_batches(filename, batch_size=10):
    with open(filename, 'r') as file:
        batch = []
        for line in file:
            batch.append(line.strip())
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

# 13. Leitura de arquivo com `pandas` (CSV)
import pandas as pd

def read_csv_with_pandas(filename):
    return pd.read_csv(filename)

# 14. Leitura de arquivo com `pandas` (Excel)
def read_excel_with_pandas(filename):
    return pd.read_excel(filename)

# 15. Leitura de arquivo com `pandas` (JSON)
def read_json_with_pandas(filename):
    return pd.read_json(filename)

# 16. Leitura de arquivo de log linha por linha
def read_log_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            if "ERROR" in line or "WARNING" in line:
                print(line.strip())

# 17. Leitura de arquivo pickle
def read_pickle_file(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

# 18. Leitura de arquivo de configuração (INI)
import configparser

def read_ini_file(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

# 19. Leitura de arquivo de texto reverso (última linha primeiro)
def read_file_reverse(filename):
    with open(filename, 'r') as file:
        for line in reversed(list(file)):
            print(line.strip())

# 20. Leitura de arquivo com filtro de linhas
def read_file_with_filter(filename, filter_func):
    with open(filename, 'r') as file:
        for line in file:
            if filter_func(line):
                print(line.strip())

# Exemplo de uso
if __name__ == "__main__":
    filename = "example.txt"
    
    # Exemplo de uso de algumas funções
    print("Leitura linha por linha:")
    read_file_line_by_line(filename)
    
    print("\nLeitura de arquivo grande em chunks:")
    for chunk in read_large_file_in_chunks(filename, chunk_size=512):
        print(chunk)
    
    print("\nLeitura de arquivo CSV:")
    read_csv_file("example.csv")
    
    print("\nLeitura de arquivo JSON:")
    data = read_json_file("example.json")
    print(data)
    
    print("\nLeitura de arquivo binário em chunks:")
    for chunk in read_binary_file_in_chunks("example.bin", chunk_size=512):
        print(chunk)