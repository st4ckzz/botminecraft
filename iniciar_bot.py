#!/usr/bin/env python3
"""
Bot para Minecraft
Desenvolvido por Stackzzx

Este é o arquivo principal para iniciar o bot.
Execute este arquivo para iniciar o painel de controle.
"""

import os
import sys

# Adiciona o diretório atual ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from painel.painel_controle import BotControlPanel

if __name__ == "__main__":
    print("\nIniciando Painel de Controle do Bot Minecraft...")
    painel = BotControlPanel()
    painel.start()