import psutil
import time

def monitorar_sistema():
    while True:
        # CPU
        uso_cpu = psutil.cpu_percent(interval=1)
        print(f"Uso da CPU: {uso_cpu}%")
        
        # Memória
        memoria = psutil.virtual_memory()
        print(f"Uso de memória: {memoria.percent}%")
        
        # Disco
        disco = psutil.disk_usage('/')
        print(f"Uso do disco: {disco.percent}%")
        
        # Rede
        rede = psutil.net_io_counters()
        print(f"Bytes enviados: {rede.bytes_sent / (1024 ** 2):.2f} MB")
        
        time.sleep(5)  # Verifica a cada 5 segundos

monitorar_sistema()
