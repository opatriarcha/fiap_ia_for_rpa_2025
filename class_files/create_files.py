def create_large_file(num_lines = 1000, file_name='large_text_file'):


    text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """


    with open(file_name, mode="w", encoding="utf-8") as file:
        for _ in range(num_lines):
            file.write(text)  # Write the text repeatedly

    print(f"File '{file_name}' created with {num_lines} lines.")


def create_large_file_csv(num_rows=10, num_columns=5 ):
    
    file_name = "lorem_ipsum.csv"


    headers = [f"Column_{i+1}" for i in range(num_columns)]


    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        writer.writerow(headers)
        
        for _ in range(num_rows):
            row = [lorem.sentence() for _ in range(num_columns)]  # Generate Lorem Ipsum sentences
            writer.writerow(row)

    print(f"File '{file_name}' created with {num_rows} rows and {num_columns} columns.")