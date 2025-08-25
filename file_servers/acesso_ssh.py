import os
import datetime
import posixpath
import paramiko

# --- CONFIG ---
SSH_HOST = "localhost"
SSH_PORT = 22
SSH_USER = "ftp_user"
SSH_PASS = "masterkey"

NOME_LOCAL = f"arquivo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
DIR_REMOTO = "teste_upload"  # será criado se não existir

def listar_detalhado(sftp, path="."):
    from stat import S_ISDIR
    print(f"\nListando: {path}")
    try:
        for attr in sftp.listdir_attr(path):
            tipo = "d" if S_ISDIR(attr.st_mode) else "-"
            data = datetime.datetime.fromtimestamp(attr.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{tipo} {attr.st_size:>10}  {data}  {attr.filename}")
    except FileNotFoundError:
        print("(diretório não existe)")

def main():
    # 1) Cria arquivo local automaticamente
    with open(NOME_LOCAL, "w", encoding="utf-8") as f:
        f.write("Arquivo gerado automaticamente para SFTP via Paramiko.\n")
        f.write("Gerado em: " + datetime.datetime.now().isoformat())

    ssh = paramiko.SSHClient()
    # Aceita host keys desconhecidas — para produção, prefira known_hosts.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 2) Conecta via SSH
        ssh.connect(
            SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS,
            look_for_keys=False, allow_agent=False, timeout=10
        )
        print(f"Conectado em {SSH_HOST}:{SSH_PORT} como {SSH_USER}")

        # 3) Abre sessão SFTP
        sftp = ssh.open_sftp()
        print("SFTP aberto.")
        print("Diretório atual remoto:", sftp.getcwd())

        # 4) Lista diretório inicial
        listar_detalhado(sftp, ".")

        # 5) Garante diretório de trabalho remoto
        try:
            sftp.mkdir(DIR_REMOTO)
            print(f"Diretório remoto criado: {DIR_REMOTO}")
        except IOError:
            # já existe
            pass

        sftp.chdir(DIR_REMOTO)
        cwd = sftp.getcwd()
        print("Entrou em:", cwd)
        listar_detalhado(sftp, ".")

        # 6) Upload
        remoto_nome = NOME_LOCAL
        sftp.put(NOME_LOCAL, remoto_nome)
        print(f"Upload concluído: {NOME_LOCAL} -> {posixpath.join(cwd, remoto_nome)}")

        # 7) Rename no servidor
        novo_nome = "renomeado_" + remoto_nome
        sftp.rename(remoto_nome, novo_nome)
        print(f"Arquivo remoto renomeado para: {novo_nome}")
        listar_detalhado(sftp, ".")

        # 8) Download para validar conteúdo
        nome_download = "baixado_" + NOME_LOCAL
        sftp.get(novo_nome, nome_download)
        print(f"Download concluído: {novo_nome} -> {nome_download}")

        # 9) Remoção remota
        sftp.remove(novo_nome)
        print(f"Arquivo remoto removido: {novo_nome}")
        listar_detalhado(sftp, ".")

        # 10) Sobe um nível e tenta remover o diretório se estiver vazio
        sftp.chdir("..")
        try:
            sftp.rmdir(DIR_REMOTO)  # só funciona se estiver vazio
            print(f"Diretório remoto removido: {DIR_REMOTO}")
        except IOError:
            print(f"Diretório {DIR_REMOTO} não está vazio ou não pôde ser removido.")

        print("Diretório atual remoto:", sftp.getcwd())

        # 11) Fecha SFTP
        sftp.close()
        print("SFTP fechado.")

    finally:
        # 12) Encerra SSH
        ssh.close()
        print("Conexão SSH encerrada.")

        # 13) Limpa arquivos locais (opcional)
        for caminho in (NOME_LOCAL, "baixado_" + NOME_LOCAL):
            try:
                os.remove(caminho)
            except FileNotFoundError:
                pass

if __name__ == "__main__":
    main()
