import concurrent.futures

def read_file_chunk(filename, start, end):
    """Lê um pedaço do arquivo e retorna o conteúdo."""
    with open(filename, 'r') as file:
        file.seek(start)
        chunk = file.read(end - start)
    return chunk

def read_large_file_with_threadpool(filename, num_threads):
    """Lê um arquivo grande usando um pool de threads."""
    file_size = 0
    with open(filename, 'r') as file:
        file.seek(0, 2)  # Vai para o final do arquivo
        file_size = file.tell()

    chunk_size = file_size // num_threads
    futures = []
    results = []
    progress = 0  # Variável para rastrear o progresso

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            start = i * chunk_size
            end = start + chunk_size if i < num_threads - 1 else file_size
            # Submete a tarefa ao pool de threads
            future = executor.submit(read_file_chunk, filename, start, end)
            futures.append(future)

        # Coleta os resultados das threads e atualiza o progresso
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            progress += 1
            percent_complete = (progress / num_threads) * 100
            print(f"Progresso: {percent_complete:.2f}% concluído")

    # Combina os resultados de todas as threads
    # full_content = ''.join(results)
    print(results)
    return full_content

if __name__ == "__main__":
    filename = "large_file.bin"
    num_threads = 4  # Número de threads no pool
    content = read_large_file_with_threadpool(filename, num_threads)
    print(f"Arquivo '{filename}' lido com sucesso usando {num_threads} threads.")