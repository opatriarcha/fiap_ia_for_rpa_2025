
import os
import sys
import tarfile
from fabric import Connection
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

REMOTE = os.getenv("FABRIC_REMOTE")
PASSWORD = os.getenv("FABRIC_PASSWORD")
APP_DIR = "app_flask"
TAR_FILE = "app_flask.tar.gz"
REMOTE_PATH = f"/tmp/{APP_DIR}"

FLASK_CODE = '''
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Olá do Flask com PostgreSQL via Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
'''

DOCKERFILE = '''
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 5000
CMD ["python", "app.py"]
'''

def criar_app_local():
    os.makedirs(APP_DIR, exist_ok=True)
    with open(f"{APP_DIR}/app.py", "w") as f:
        f.write(FLASK_CODE.strip())
    with open(f"{APP_DIR}/Dockerfile", "w") as f:
        f.write(DOCKERFILE.strip())

def compactar_app_local():
    with tarfile.open(TAR_FILE, "w:gz") as tar:
        tar.add(APP_DIR, arcname=APP_DIR)

def conectar():
    if not REMOTE or not PASSWORD:
        print("[ERRO] Variáveis de ambiente não definidas corretamente.")
        sys.exit(1)
    return Connection(
        REMOTE,
        connect_kwargs={
            "password": PASSWORD,
            "look_for_keys": False,
            "allow_agent": False
        }
    )

def run_sudo(conn, comando):
    return conn.run(f'echo "{PASSWORD}" | sudo -S {comando}', hide=False)

def preparar_remoto(conn):
    print("[*] Verificando Docker no servidor...")
    run_sudo(conn, "docker --version")

    print("[*] Criando rede Docker (se necessário)...")
    redes = run_sudo(conn, "docker network ls --format '{{.Name}}'").stdout
    if "rede_app" not in redes:
        run_sudo(conn, "docker network create rede_app")

def subir_postgres(conn):
    print("[*] Subindo container PostgreSQL...")
    run_sudo(conn, "docker rm -f db_postgres || true")
    run_sudo(conn,
        "docker run -d --name db_postgres "
        "--network rede_app "
        "-e POSTGRES_USER=admin "
        "-e POSTGRES_PASSWORD=123456 "
        "-e POSTGRES_DB=appdb "
        "-p 5432:5432 "
        "postgres:14"
    )

def subir_flask(conn):
    print("[*] Compactando app Flask localmente...")
    compactar_app_local()

    print("[*] Enviando app Flask compactado para o servidor...")
    conn.put(TAR_FILE, remote=f"/tmp/{TAR_FILE}")

    print("[*] Extraindo app no servidor remoto...")
    run_sudo(conn, f"rm -rf {REMOTE_PATH}")
    run_sudo(conn, f"mkdir -p {REMOTE_PATH}")
    run_sudo(conn, f"tar -xzf /tmp/{TAR_FILE} -C /tmp")

    print("[*] Buildando imagem Docker da aplicação Flask...")
    with conn.cd(REMOTE_PATH):
        run_sudo(conn, "docker build -t app_flask .")

    print("[*] Subindo container Flask...")
    run_sudo(conn, "docker rm -f flask_app || true")
    run_sudo(conn,
        "docker run -d --name flask_app "
        "--network rede_app "
        "-p 5000:5000 "
        "app_flask"
    )

def listar_containers(conn):
    print("[*] Containers ativos:")
    run_sudo(conn, "docker ps")

def limpar_local():
    print("[*] Limpando arquivos temporários locais...")
    for file in Path(APP_DIR).glob("*"):
        file.unlink()
    os.rmdir(APP_DIR)
    if Path(TAR_FILE).exists():
        os.remove(TAR_FILE)

def main():
    try:
        criar_app_local()
        conn = conectar()
        preparar_remoto(conn)
        subir_postgres(conn)
        subir_flask(conn)
        listar_containers(conn)
        limpar_local()
        print("\n[OK] Robô executado com sucesso. Acesse: http://<IP_DO_SERVIDOR>:5000")
    except Exception as e:
        print(f"[ERRO] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
