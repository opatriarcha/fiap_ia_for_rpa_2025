import csv
import json

def write_text_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def append_text_file(filename, content):
    with open(filename, 'a') as file:
        file.write(content)

def write_lines_to_file(filename, lines):
    with open(filename, 'w') as file:
        for line in lines:
            file.write(line + '\n')

def append_lines_to_file(filename, lines):
    with open(filename, 'a') as file:
        for line in lines:
            file.write(line + '\n')

def write_csv_file(filename, headers, rows):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

def append_csv_file(filename, rows):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def write_json_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def append_json_file(filename, new_data):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    data.append(new_data)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def write_binary_file(filename, data):
    with open(filename, 'wb') as file:
        file.write(data)

def append_binary_file(filename, data):
    with open(filename, 'ab') as file:
        file.write(data)
