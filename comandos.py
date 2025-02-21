import time
from config.config import BotConfig
import os

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.commands = {
            'vem': self.cmd_come,
            'parar': self.cmd_stop,
            'ir': self.cmd_goto,
            'ajuda': self.cmd_help,
            'pular': self.cmd_jump,
            'status': self.cmd_status,
            'olhar': self.cmd_look,
            'inventario': self.cmd_inventory,
            'dima': self.cmd_diamonds,
            'criativo': self.cmd_creative,
            'skin': self.cmd_skin,
            'nome': self.cmd_change_name
        }
        self.auto_teleport = True
        self.last_teleport = time.time()
        self.target_player = "Stackzzx"

    def handle_command(self, username, command_text):
        command_parts = command_text.split()
        command = command_parts[0].lower()
        args = command_parts[1:]

        if command in self.commands:
            self.commands[command](username, args)
        else:
            self.bot._client.write('chat', {'text': "Comando desconhecido. Use !ajuda para ver todos os comandos disponíveis."})

    def cmd_change_name(self, username, args):
        """Comando para mudar o nome do bot"""
        if username != "Stackzzx":
            self.bot._client.write('chat', {'text': "Apenas o Stackzzx pode mudar meu nome!"})
            return

        if not args:
            self.bot._client.write('chat', {'text': "Use: !nome <novo_nome>"})
            return

        new_name = args[0]
        try:
            with open('config/configuracoes.py', 'r') as f:
                lines = f.readlines()

            with open('config/configuracoes.py', 'w') as f:
                for line in lines:
                    if line.startswith('NOME_BOT'):
                        f.write(f'NOME_BOT = "{new_name}"\n')
                    else:
                        f.write(line)

            self.bot._client.write('chat', {'text': f"Nome alterado para {new_name}! Reinicie o bot para aplicar a mudança."})
        except Exception as e:
            self.bot._client.write('chat', {'text': f"Erro ao mudar o nome: {str(e)}"})

    def cmd_diamonds(self, username, args):
        if username == "Stackzzx":
            try:
                self.bot._client.write('chat', {'text': "/give Stackzzx minecraft:diamond 64"})
                self.bot._client.write('chat', {'text': "✨ Aqui estão seus diamantes!"})
            except Exception as e:
                self.bot._client.write('chat', {'text': "Não foi possível dar os diamantes. Verifique se tenho permissões."})
        else:
            self.bot._client.write('chat', {'text': "Desculpe, apenas o Stackzzx pode usar este comando!"})

    def cmd_creative(self, username, args):
        try:
            self.bot._client.write('chat', {'text': "/gamemode creative"})
            self.bot._client.write('chat', {'text': "Modo criativo ativado!"})
        except Exception as e:
            self.bot._client.write('chat', {'text': "Não foi possível mudar para modo criativo."})

    def cmd_skin(self, username, args):
        if len(args) == 1:
            skin_url = args[0]
            try:
                self.bot._client.write('chat', {'text': f"Tentando mudar a skin para: {skin_url}"})
            except Exception as e:
                self.bot._client.write('chat', {'text': "Erro ao mudar a skin."})
        else:
            self.bot._client.write('chat', {'text': "Uso: !skin <url_da_skin>"})

    def cmd_come(self, username, args):
        self.bot._client.write('chat', {'text': f"Indo até você, {username}!"})
        self.bot.movement.follow_player(username)

    def cmd_stop(self, username, args):
        self.bot._client.write('chat', {'text': "Parando todos os movimentos"})
        self.bot.movement.stop_movement()

    def cmd_goto(self, username, args):
        if len(args) == 3:
            try:
                x, y, z = map(int, args)
                self.bot._client.write('chat', {'text': f"Indo para as coordenadas: x={x}, y={y}, z={z}"})
                self.bot.movement.move_to_position(x, y, z)
            except ValueError:
                self.bot._client.write('chat', {'text': "Coordenadas inválidas! Use apenas números inteiros."})
        else:
            self.bot._client.write('chat', {'text': "Uso correto: !ir <x> <y> <z>"})

    def cmd_help(self, username, args):
        help_text = """Comandos disponíveis:
        !vem - Faz o bot ir até sua localização
        !parar - Para todos os movimentos do bot
        !ir <x> <y> <z> - Bot vai até as coordenadas especificadas
        !pular - Faz o bot pular
        !status - Mostra a posição atual do bot
        !olhar <jogador> - Bot olha para o jogador especificado
        !inventario - Mostra os itens no inventário do bot
        !dima - Dá 64 diamantes (apenas para Stackzzx)
        !criativo - Ativa modo criativo
        !skin <url> - Muda a skin do bot
        !nome <novo_nome> - Muda o nome do bot (apenas para Stackzzx)
        !ajuda - Mostra esta mensagem de ajuda"""
        self.bot._client.write('chat', {'text': help_text})

    def cmd_jump(self, username, args):
        self.bot._client.write('chat', {'text': "Pulando!"})
        self.bot.movement.jump()

    def cmd_status(self, username, args):
        position = self.bot.entity.position
        self.bot._client.write('chat', {'text': f"Posição atual: x={position.x:.1f}, y={position.y:.1f}, z={position.z:.1f}"})

    def cmd_look(self, username, args):
        if len(args) == 1:
            target_player = args[0]
            if target_player in self.bot.players:
                player = self.bot.players[target_player]
                self.bot.lookAt(player.entity.position)
                self.bot._client.write('chat', {'text': f"Olhando para {target_player}"})
            else:
                self.bot._client.write('chat', {'text': f"Jogador {target_player} não encontrado"})
        else:
            self.bot._client.write('chat', {'text': "Uso correto: !olhar <jogador>"})

    def cmd_inventory(self, username, args):
        try:
            inventory = self.bot.inventory.items()
            if not inventory:
                self.bot._client.write('chat', {'text': "Inventário vazio"})
                return

            items = [f"{item.name} (x{item.count})" for item in inventory]
            inventory_text = "Itens no inventário: " + ", ".join(items)
            self.bot._client.write('chat', {'text': inventory_text})
        except Exception as e:
            self.bot._client.write('chat', {'text': "Erro ao verificar inventário"})

    def check_auto_teleport(self):
        current_time = time.time()
        if current_time - self.last_teleport >= 600:  # 10 minutos
            self.last_teleport = current_time
            target = self.bot.players.get(self.target_player)

            if target:
                self.bot._client.write('chat', {'text': f"Teleportando para {self.target_player}..."})
                try:
                    self.bot._client.write('chat', {'text': f"/tp {self.target_player}"})
                except Exception as e:
                    self.bot._client.write('chat', {'text': "Erro ao teleportar."})
            else:
                self.bot._client.write('chat', {'text': "Jogador alvo não encontrado, teleportando para o spawn..."})
                try:
                    self.bot._client.write('chat', {'text': "/spawn"})
                except Exception as e:
                    self.bot._client.write('chat', {'text': "Erro ao teleportar para o spawn."})