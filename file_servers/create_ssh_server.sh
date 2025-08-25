#!/bin/bash

# ==============================================================================
# Script para Instalar e Configurar um Servidor SSH Local no Ubuntu
# ==============================================================================
#
# Descrição:
# Este script automatiza a instalação do OpenSSH Server, inicia o serviço
# e o configura para iniciar automaticamente com o sistema. Ele também
# abre a porta necessária no firewall UFW (Uncomplicated Firewall).
#
# Execução:
# 1. Salve este script em um arquivo, por exemplo, 'setup_ssh.sh'.
# 2. Dê permissão de execução ao arquivo: chmod +x setup_ssh.sh
# 3. Execute o script com privilégios de superusuário: sudo ./setup_ssh.sh
#
# ==============================================================================

# Exit immediately if a command exits with a non-zero status.
set -e

# --- 1. ATUALIZAR A LISTA DE PACOTES ---
echo "=> Atualizando a lista de pacotes..."
sudo apt-get update

# --- 2. INSTALAR O OPENSSH-SERVER ---
echo "=> Instalando o OpenSSH Server..."
sudo apt-get install -y openssh-server

# --- 3. INICIAR E HABILITAR O SERVIÇO SSH ---
# O serviço geralmente inicia automaticamente após a instalação em sistemas modernos.
# Estes comandos garantem que ele esteja em execução e habilitado para iniciar no boot.
echo "=> Iniciando e habilitando o serviço SSH..."
sudo systemctl start ssh
sudo systemctl enable ssh

# --- 4. CONFIGURAR O FIREWALL (UFW) ---
# Verifica se o UFW está ativo e, em caso afirmativo, permite o tráfego SSH.
if sudo ufw status | grep -q "Status: active"; then
  echo "=> O UFW está ativo. Configurando a regra para permitir SSH..."
  sudo ufw allow ssh
  echo "=> Regra de firewall para SSH adicionada."
else
  echo "=> O UFW não está ativo. Habilitando o UFW e permitindo SSH..."
  sudo ufw allow ssh
  sudo ufw --force enable
  echo "=> UFW habilitado e regra para SSH adicionada."
fi

# --- 5. VERIFICAR O STATUS DO SERVIÇO SSH ---
echo "=> Verificando o status do servidor SSH..."
sudo systemctl status ssh --no-pager

# --- CONCLUSÃO ---
echo ""
echo "=================================================="
echo "  Instalação do Servidor SSH concluída!         "
echo "=================================================="
echo ""
echo "O seu servidor SSH está ativo e em execução."
echo "Para se conectar a partir de outra máquina na mesma rede, use:"
echo "ssh seu_usuario@$(hostname -I | awk '{print $1}')"
echo ""
