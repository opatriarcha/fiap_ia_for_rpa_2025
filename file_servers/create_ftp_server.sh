#!/bin/bash

# ==============================================================================
# Script para Instalar e Configurar um Servidor FTP (vsftpd) no Ubuntu
# ==============================================================================
#
# Descrição:
# Este script automatiza a instalação do vsftpd, cria uma configuração segura
# básica, reinicia o serviço, e abre as portas necessárias no firewall UFW.
# A configuração permite que usuários locais do sistema façam login e fiquem
# restritos ao seu diretório home.
#
# Execução:
# 1. Salve este script em um arquivo, por exemplo, 'setup_ftp.sh'.
# 2. Dê permissão de execução ao arquivo: chmod +x setup_ftp.sh
# 3. Execute o script com privilégios de superusuário: sudo ./setup_ftp.sh
#
# ==============================================================================

# Sai imediatamente se um comando falhar.
set -e

# --- 1. ATUALIZAR A LISTA DE PACOTES ---
echo "=> Atualizando a lista de pacotes..."
sudo apt-get update

# --- 2. INSTALAR O VSFTPD ---
echo "=> Instalando o vsftpd (Very Secure FTP Daemon)..."
sudo apt-get install -y vsftpd

# --- 3. CONFIGURAR O VSFTPD ---
# Primeiro, faz um backup do arquivo de configuração original.
CONFIG_FILE="/etc/vsftpd.conf"
echo "=> Fazendo backup do arquivo de configuração original para ${CONFIG_FILE}.orig..."
sudo cp $CONFIG_FILE ${CONFIG_FILE}.orig

echo "=> Aplicando configurações de segurança e funcionalidade..."
# Desabilita login anônimo (mais seguro).
sudo sed -i 's/anonymous_enable=YES/anonymous_enable=NO/' $CONFIG_FILE
# Habilita login de usuários locais (usuários do sistema).
sudo sed -i 's/#local_enable=YES/local_enable=YES/' $CONFIG_FILE
# Habilita o comando de escrita (upload, criar diretório, etc.).
sudo sed -i 's/#write_enable=YES/write_enable=YES/' $CONFIG_FILE
# Restringe os usuários locais ao seu diretório home (chroot jail).
sudo sed -i 's/#chroot_local_user=YES/chroot_local_user=YES/' $CONFIG_FILE

# Adiciona configurações para o modo passivo, que é mais amigável a firewalls.
echo "=> Configurando portas para o modo passivo..."
echo 'pasv_min_port=40000' | sudo tee -a $CONFIG_FILE
echo 'pasv_max_port=41000' | sudo tee -a $CONFIG_FILE
echo 'pasv_enable=YES' | sudo tee -a $CONFIG_FILE

# Permite que o usuário chroot tenha permissão de escrita.
echo 'allow_writeable_chroot=YES' | sudo tee -a $CONFIG_FILE


# --- 4. CONFIGURAR O FIREWALL (UFW) ---
echo "=> Configurando o firewall UFW..."
# Abre a porta 21 (comando FTP) e 20 (dados FTP em modo ativo).
sudo ufw allow 20/tcp
sudo ufw allow 21/tcp
# Abre o range de portas para o modo passivo.
sudo ufw allow 40000:41000/tcp

# Garante que o UFW esteja ativo.
if ! sudo ufw status | grep -q "Status: active"; then
  echo "=> UFW não estava ativo. Habilitando agora..."
  sudo ufw --force enable
fi

# --- 5. REINICIAR E HABILITAR O SERVIÇO FTP ---
echo "=> Reiniciando e habilitando o serviço vsftpd..."
sudo systemctl restart vsftpd
sudo systemctl enable vsftpd

# --- 6. VERIFICAR O STATUS DO SERVIÇO ---
echo "=> Verificando o status do servidor vsftpd..."
sudo systemctl status vsftpd --no-pager

# --- CONCLUSÃO ---
echo ""
echo "=================================================="
echo "  Instalação do Servidor FTP concluída!         "
echo "=================================================="
echo ""
echo "O seu servidor FTP (vsftpd) está ativo e em execução."
echo "Para se conectar, você precisa de um usuário local."
echo "Use o comando 'sudo adduser nome_do_usuario' para criar um."
echo ""
echo "Use um cliente FTP (como FileZilla ou o terminal) para conectar-se com:"
echo "Servidor: $(hostname -I | awk '{print $1}')"
echo "Porta: 21"
echo "Usuário e senha: as credenciais do usuário que você criou."
echo ""
