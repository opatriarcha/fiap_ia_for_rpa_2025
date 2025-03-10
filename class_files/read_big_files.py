import concurrent.futures
import os
import time

def read_large_file_with_threads(filename, num_threads=4, chunk_size=1024 * 1024):
    """
    Reads a large file in a performant manner using threads.

    :param filename: Name of the file to read.
    :param num_threads: Number of threads to use (default is 4).
    :param chunk_size: Size of each chunk in bytes (default is 1MB).
    """
    file_size = os.path.getsize(filename)

    start_time = time.time()

    def read_chunk(thread_id, start, size):
        with open(filename, 'rb') as file:
            file.seek(start)
            chunk = file.read(size)
            lines_in_chunk = chunk.decode('utf-8', errors='ignore').count('\n')
            
            progress = (start + size) / file_size * 100
            elapsed_time = time.time() - start_time
            print(f"Thread {thread_id}: Read chunk of size {size} bytes | Progress: {progress:.2f}% | Time Elapsed: {elapsed_time:.2f}s")
            
            return lines_in_chunk

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        start = 0
        chunk_id = 0

        # Divide the file into chunks and submit tasks to the thread pool
        while start < file_size:
            end = min(start + chunk_size, file_size)
            futures.append(executor.submit(read_chunk, chunk_id % num_threads, start, end - start))
            start = end
            chunk_id += 1

        total_lines = 0
        for future in concurrent.futures.as_completed(futures):
            lines_in_chunk = future.result()
            total_lines += lines_in_chunk

    
    total_time = time.time() - start_time
    print(f"\nTotal lines in file: {total_lines}")
    print(f"Total time elapsed: {total_time:.2f}s")

if __name__ == "__main__":
    read_large_file_with_threads("large_file.bin", num_threads=4)