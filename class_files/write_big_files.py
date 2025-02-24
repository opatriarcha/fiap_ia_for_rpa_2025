import os

def create_large_file(filename, size_gb=1, chunk_size=1024 * 1024):
    """
    Creates a large file of approximately the specified size in GB.

    :param filename: Name of the file to create.
    :param size_gb: Size of the file in GB (default is 1GB).
    :param chunk_size: Size of each chunk in bytes (default is 1MB).
    """
    total_size = size_gb * 1024 * 1024 * 1024

    with open(filename, 'wb') as file:
        written_size = 0  # Track the number of bytes written

        while written_size < total_size:
            current_chunk_size = min(chunk_size, total_size - written_size)
            
            chunk = os.urandom(current_chunk_size)
            
            file.write(chunk)
            
            written_size += current_chunk_size

            progress = (written_size / total_size) * 100
            print(f"Progress: {progress:.2f}%", end="\r")  # Use \r to overwrite the line

    print(f"\nFile '{filename}' created with size {size_gb}GB.")

if __name__ == "__main__":
    create_large_file("large_file.bin", size_gb=10)