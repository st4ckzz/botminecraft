import time
import os
import json
from datetime import datetime
import subprocess
import threading
import signal
from config.config import BotConfig

class BotControlPanel:
    def __init__(self):
        self.bot_process = None
        self.running = True
        self.log_update_thread = None
        self.commands = {
            'start': self.start_bot,
            'stop': self.stop_bot,
            'restart': self.restart_bot,
            'status': self.show_status,
            'config': self.show_config,
            'help': self.show_help,
            'exit': self.exit,
            'servidor': self.change_server
        }

        # Cores ANSI
        self.cores = {
            'vermelho': '\033[91m',
            'verde': '\033[92m',
            'amarelo': '\033[93m',
            'reset': '\033[0m',
            'negrito': '\033[1m'
        }

        self.ascii_art = """
░██████╗████████╗░█████╗░░█████╗░██╗░░██╗███████╗███████╗
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║░██╔╝╚════██║╚════██║
╚█████╗░░░░██║░░░███████║██║░░╚═╝█████═╝░░░███╔═╝░░███╔═╝
░╚═══██╗░░░██║░░░██╔══██║██║░░██╗██╔═██╗░██╔══╝░░██╔══╝░░
██████╔╝░░░██║░░░██║░░██║╚█████╔╝██║░╚██╗███████╗███████╗
╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝╚══════╝
"""

    def start(self):
        signal.signal(signal.SIGINT, self.handle_sigint)

        print(f"\n{self.cores['verde']}{self.ascii_art}{self.cores['reset']}")
        print(f"{self.cores['negrito']}=== Painel de Controle do Bot Minecraft ===")
        print(f"{self.cores['amarelo']}Direitos Reservados © Stackzzx{self.cores['reset']}")
        print(f"{self.cores['vermelho']}Instagram: @pedroz.jpg{self.cores['reset']}")
        print("\nDigite 'help' para ver os comandos disponíveis\n")

        while self.running:
            try:
                command = input(f"{self.cores['verde']}Bot > {self.cores['reset']}").strip().lower()
                if command in self.commands:
                    self.commands[command]()
                elif command:
                    print(f"{self.cores['vermelho']}Comando desconhecido. Digite 'help' para ver os comandos disponíveis.{self.cores['reset']}")
            except EOFError:
                self.exit()
            except KeyboardInterrupt:
                self.exit()
            except Exception as e:
                print(f"{self.cores['vermelho']}Erro: {str(e)}{self.cores['reset']}")

    def handle_sigint(self, signum, frame):
        self.exit()

    def start_bot(self):
        if self.bot_process:
            print("Bot já está rodando!")
            return

        try:
            self.bot_process = subprocess.Popen(
                ['python3', 'bot.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("Bot iniciado com sucesso!")
            self.start_log_update()
        except Exception as e:
            print(f"Erro ao iniciar bot: {str(e)}")

    def stop_bot(self):
        if not self.bot_process:
            print("Bot não está rodando!")
            return

        try:
            self.bot_process.terminate()
            self.bot_process.wait(timeout=5)  # Esperar até 5 segundos pelo término
            self.bot_process = None
            print("Bot parado com sucesso!")
        except subprocess.TimeoutExpired:
            self.bot_process.kill()  # Forçar término se demorar muito
            self.bot_process = None
            print("Bot forçado a parar!")
        except Exception as e:
            print(f"Erro ao parar bot: {str(e)}")

    def restart_bot(self):
        self.stop_bot()
        time.sleep(2)
        self.start_bot()

    def show_status(self):
        print("\n=== Status do Bot ===")
        if self.bot_process:
            print("Status: RODANDO")
            print("\nProcesso:", self.bot_process.pid)

            if os.path.exists('minecraft_bot.log'):
                with open('minecraft_bot.log', 'r') as f:
                    last_logs = f.readlines()[-10:]  # Mostrar últimos 10 logs
                    print("\nÚltimos logs:")
                    for log in last_logs:
                        print(f"  {log.strip()}")

            print("\nComandos disponíveis:")
            print("  stop    - Para o bot")
            print("  restart - Reinicia o bot")
            print("  help    - Lista todos os comandos")
        else:
            print("Status: PARADO")
            print("\nUse 'start' para iniciar o bot ou 'help' para ver todos os comandos")
            print(f"{self.cores['amarelo']}Direitos Reservados © Stackzzx{self.cores['reset']}")
            print(f"{self.cores['vermelho']}Instagram: @pedroz.jpg{self.cores['reset']}")

    def show_config(self):
        try:
            with open('settings.py', 'r') as f:
                print("\n=== Configurações do Bot ===")
                for line in f:
                    if any(key in line for key in ['SERVIDOR', 'PORTA', 'NOME_BOT', 'TIPO_AUTENTICACAO']):
                        print(f"  {line.strip()}")
        except Exception as e:
            print(f"Erro ao ler configurações: {str(e)}")

    def show_help(self):
        print(f"\n{self.cores['negrito']}=== Comandos do Painel de Controle ===")
        print("  start    - Inicia o bot")
        print("  stop     - Para o bot")
        print("  restart  - Reinicia o bot")
        print("  status   - Mostra o status atual do bot")
        print("  config   - Mostra as configurações atuais")
        print("  servidor - Muda o servidor de conexão")
        print("  help     - Mostra esta mensagem")
        print("  exit     - Sai do painel de controle")

        print(f"\n{self.cores['negrito']}=== Comandos do Bot In-Game ===")
        print("  !vem         - Bot vai até sua localização")
        print("  !parar       - Para todos os movimentos do bot")
        print("  !ir x y z    - Bot vai até as coordenadas especificadas")
        print("  !pular       - Faz o bot pular")
        print("  !status      - Mostra a posição atual do bot")
        print("  !olhar       - Bot olha para o jogador especificado")
        print("  !inventario  - Mostra os itens no inventário do bot")
        print("  !dima        - Dá 64 diamantes (apenas para Stackzzx)")
        print("  !criativo    - Ativa modo criativo")
        print("  !skin        - Muda a skin do bot")
        print("  !nome        - Muda o nome do bot (apenas para Stackzzx)")

        print(f"\n{self.cores['amarelo']}Direitos Reservados © Stackzzx")
        print(f"{self.cores['vermelho']}Instagram: @pedroz.jpg{self.cores['reset']}")

    def change_server(self):
        """Novo comando para mudar o servidor"""
        print("\n=== Mudar Servidor ===")
        new_server = input("Novo endereço do servidor: ")
        new_port = input("Nova porta (pressione Enter para usar 25565): ") or "25565"

        try:
            with open('settings.py', 'r') as f:
                lines = f.readlines()

            with open('settings.py', 'w') as f:
                for line in lines:
                    if line.startswith('SERVIDOR'):
                        f.write(f'SERVIDOR = "{new_server}"\n')
                    elif line.startswith('PORTA'):
                        f.write(f'PORTA = {new_port}\n')
                    else:
                        f.write(line)

            print("\nServidor alterado com sucesso!")
            print("Use 'restart' para aplicar as mudanças.")
        except Exception as e:
            print(f"Erro ao mudar servidor: {str(e)}")


    def update_logs(self):
        while self.running and self.bot_process:
            try:
                if os.path.exists('minecraft_bot.log'):
                    with open('minecraft_bot.log', 'r') as f:
                        logs = f.readlines()[-1:]
                        for log in logs:
                            print(f"Log: {log.strip()}")
            except Exception as e:
                print(f"Erro ao atualizar logs: {str(e)}")
            time.sleep(1)

    def start_log_update(self):
        if not self.log_update_thread or not self.log_update_thread.is_alive():
            self.log_update_thread = threading.Thread(target=self.update_logs)
            self.log_update_thread.daemon = True
            self.log_update_thread.start()

    def exit(self):
        print("\nEncerrando painel de controle...")
        self.running = False
        if self.bot_process:
            self.stop_bot()
        os._exit(0)  # Forçar saída para evitar problemas com threads

if __name__ == "__main__":
    panel = BotControlPanel()
    panel.start()