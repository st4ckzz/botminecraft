import time
from javascript import require
import logging
from config.config import BotConfig
from src.movimentacao import MovementController
from src.seguranca import SafetySystem
from src.comandos import CommandHandler
from src.logger import setup_logger
import random
from datetime import datetime
import pytz

class MinecraftBot:
    def __init__(self):
        self.mineflayer = None
        self.bot = None
        self.logger = setup_logger()
        self.initialize_mineflayer()
        self.last_particle_time = time.time()

        # Configuração da versão específica
        self.server_version = BotConfig.VERSAO_MINECRAFT

        # Respostas do chat
        self.chat_responses = {
            'oi': ['Olá!', 'Oi, tudo bem?', 'Hey!'],
            'bot': ['Sim, eu sou um bot!', 'Em que posso ajudar?'],
            'ajuda': ['Use !ajuda para ver os comandos disponíveis'],
            'servidor': ['Este é um ótimo servidor!', 'Estou gostando daqui!']
        }

    def initialize_mineflayer(self):
        try:
            self.logger.info("Iniciando Mineflayer...")
            self.mineflayer = require('mineflayer')
            self.logger.info("Mineflayer inicializado com sucesso")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao inicializar Mineflayer: {str(e)}")
            if self.install_dependencies():
                return self.initialize_mineflayer()
            return False

    def install_dependencies(self):
        try:
            self.logger.info("Instalando dependências...")
            import os
            os.system('npm install mineflayer mineflayer-pathfinder minecraft-data')
            self.logger.info("Dependências instaladas com sucesso")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao instalar dependências: {str(e)}")
            return False

    def setup_bot(self):
        try:
            if not self.mineflayer:
                if not self.initialize_mineflayer():
                    return False

            bot_options = {
                'host': BotConfig.HOST,
                'port': BotConfig.PORT,
                'username': BotConfig.USERNAME,
                'auth': BotConfig.AUTH_TYPE,
                'version': self.server_version,  # Usando versão específica
                'hideErrors': False,
                'checkTimeoutInterval': 60000,
                'reconnect': True,
                'chatLengthLimit': 256,
                'logErrors': True
            }

            self.bot = self.mineflayer.createBot(bot_options)
            self.setup_event_handlers()
            return True

        except Exception as e:
            self.logger.error(f"Erro ao criar bot: {str(e)}")
            time.sleep(5)
            return False

    def setup_event_handlers(self):
        try:
            self.bot.on('spawn', self.handle_spawn)
            self.bot.on('error', self.handle_error)
            self.bot.on('end', self.handle_end)
            self.bot.on('chat', self.handle_chat)
            self.bot.on('physicsTick', self.handle_physics)
            self.bot.on('login', self.handle_login)
            self.bot.on('playerJoined', self.handle_player_joined)
            self.logger.info("Event handlers configurados")
        except Exception as e:
            self.logger.error(f"Erro ao configurar handlers: {str(e)}")
            raise

    def handle_login(self, *args):
        try:
            self.logger.info("Login realizado com sucesso!")
            # Enviar comandos silenciosamente
            self.bot._client.write('chat', {'text': "/gamemode creative"})

            # Mensagem de boas-vindas
            greeting = self.get_brazil_time_greeting()
            self.bot._client.write('chat', {'text': f"Olá pessoal, {greeting}! Bot iniciado com sucesso!"})
        except Exception as e:
            self.logger.error(f"Erro no handle_login: {str(e)}")

    def get_brazil_time_greeting(self):
        brazil_tz = pytz.timezone('America/Sao_Paulo')
        current_time = datetime.now(brazil_tz)
        hour = current_time.hour

        if 5 <= hour < 12:
            return "bom dia"
        elif 12 <= hour < 18:
            return "boa tarde"
        else:
            return "boa noite"


    def handle_spawn(self):
        try:
            self.logger.info("Bot spawnou no mundo")
            self.movement = MovementController(self.bot)
            self.safety = SafetySystem(self.bot)
            self.command_handler = CommandHandler(self.bot)
            self.start_particle_effect()
            self.start_entity_tracking()
        except Exception as e:
            self.logger.error(f"Erro ao inicializar sistemas: {str(e)}")

    def handle_error(self, err, *args):
        try:
            error_message = str(err)
            if "ECONNRESET" in error_message or "connection" in error_message.lower():
                self.logger.info("Tentando reconectar ao servidor...")
            elif "version" in error_message.lower():
                self.logger.info("Detectando versão do servidor...")
                self.server_version = None
            else:
                self.logger.error(f"Erro: {error_message}")

            time.sleep(5)
            self.setup_bot()
        except Exception as e:
            self.logger.error(f"Erro crítico no tratamento de erro: {str(e)}")
            self.setup_bot()

    def handle_end(self):
        self.logger.info("Conexão encerrada, reconectando...")
        time.sleep(5)
        self.setup_bot()

    def handle_chat(self, username, message, *args):
        if username == self.bot.username:
            return

        if message.startswith(BotConfig.COMMAND_PREFIX):
            self.command_handler.handle_command(username, message[1:])
        else:
            message = message.lower()
            for key in self.chat_responses:
                if key in message:
                    response = random.choice(self.chat_responses[key])
                    self.bot.chat(response)
                    break

    def handle_player_joined(self, player):
        try:
            if player.username != self.bot.username:
                greeting = self.get_brazil_time_greeting()
                self.bot.chat(f"{player.username}, {greeting}! Bem-vindo(a) ao servidor!")
        except Exception as e:
            self.logger.error(f"Erro ao dar boas-vindas: {str(e)}")

    def handle_physics(self):
        try:
            current_time = time.time()

            if hasattr(self, 'safety'):
                self.safety.check_surroundings()

            if hasattr(self, 'command_handler'):
                self.command_handler.check_auto_teleport()

            if current_time - self.last_particle_time >= 1:
                self.last_particle_time = current_time
                self.update_particles()

        except Exception as e:
            self.logger.error(f"Erro no ciclo de física: {str(e)}")

    def start_particle_effect(self):
        try:
            self.bot.chat("/particle minecraft:lava ~ ~ ~ 0.5 0.5 0.5 0.1 1 normal")
        except Exception as e:
            self.logger.error(f"Erro ao criar partículas: {str(e)}")

    def update_particles(self):
        try:
            if hasattr(self.bot, 'entity') and hasattr(self.bot.entity, 'position'):
                self.bot.chat(f"/particle minecraft:lava {self.bot.entity.position.x} {self.bot.entity.position.y} {self.bot.entity.position.z} 0.2 0.2 0.2 0.1 1 normal")
        except Exception as e:
            self.logger.debug(f"Erro ao atualizar partículas: {str(e)}")

    def start_entity_tracking(self):
        try:
            def look_at_nearest_entity():
                try:
                    entities = self.bot.entities
                    nearest = None
                    nearest_distance = float('inf')

                    for entity_id in entities:
                        entity = entities[entity_id]
                        if hasattr(entity, 'type') and entity.type in ['player', 'mob']:
                            distance = self.bot.entity.position.distanceTo(entity.position)
                            if distance < nearest_distance and distance < 10:
                                nearest = entity
                                nearest_distance = distance

                    if nearest:
                        self.bot.lookAt(nearest.position)
                except Exception as e:
                    self.logger.debug(f"Erro ao rastrear entidades: {str(e)}")

            self.bot.on('physicsTick', look_at_nearest_entity)
            self.logger.info("Sistema de rastreamento iniciado")
        except Exception as e:
            self.logger.error(f"Erro ao iniciar rastreamento: {str(e)}")

    def start(self):
        self.logger.info("Iniciando bot do Minecraft...")
        while True:
            if self.setup_bot():
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    self.logger.info("Encerrando bot...")
                    if self.bot:
                        self.bot.quit()
                    break
            time.sleep(5)

if __name__ == "__main__":
    try:
        minecraft_bot = MinecraftBot()
        minecraft_bot.start()
    except Exception as e:
        logger = setup_logger()
        logger.error(f"Erro fatal ao iniciar: {str(e)}")