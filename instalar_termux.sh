#!/data/data/com.termux/files/usr/bin/bash

# Cores para output
VERMELHO='\033[0;31m'
VERDE='\033[0;32m'
AMARELO='\033[1;33m'
RESET='\033[0m'

echo -e "${VERDE}=== Instalador do Bot Minecraft para Termux ===${RESET}\n"
echo -e "${AMARELO}Desenvolvido por Stackzzx${RESET}"
echo -e "${VERMELHO}Instagram: @pedroz.jpg${RESET}\n"

# Atualizar repositórios
echo "Atualizando repositórios..."
pkg update -y

# Instalar dependências
echo "Instalando dependências..."
pkg install -y python nodejs git

# Instalar pip
python -m pip install --upgrade pip

# Instalar dependências Python
echo "Instalando bibliotecas Python..."
pip install javascript pytz requests

# Instalar dependências Node.js
echo "Instalando bibliotecas Node.js..."
npm install mineflayer mineflayer-pathfinder minecraft-data

# Criar atalho de execução
echo "#!/data/data/com.termux/files/usr/bin/bash
python iniciar_bot.py" > executar_bot.sh

chmod +x executar_bot.sh

echo -e "\n${VERDE}Instalação concluída!${RESET}"
echo -e "Para iniciar o bot, execute: ${AMARELO}./executar_bot.sh${RESET}"
