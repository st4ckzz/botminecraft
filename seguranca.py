from config.config import BotConfig
import logging
import time
import math

class SafetySystem:
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('minecraft_bot')
        self.last_check_time = 0
        self.check_interval = 2.0  # Aumentado para 2 segundos entre verificações

    def check_surroundings(self):
        current_time = time.time()
        if current_time - self.last_check_time < self.check_interval:
            return

        self.last_check_time = current_time

        try:
            if self.check_fall_danger():
                self.logger.warning("Perigo de queda detectado!")
                self.emergency_stop()

            if self.check_dangerous_blocks():
                self.logger.warning("Blocos perigosos detectados!")
                self.emergency_stop()
        except Exception as e:
            self.logger.error(f"Erro ao verificar segurança: {str(e)}")

    def check_fall_danger(self):
        try:
            position = self.bot.entity.position
            x = math.floor(position.x)
            y = math.floor(position.y)
            z = math.floor(position.z)

            # Verificar se o bot está no ar (pulando ou caindo)
            if self.bot.entity.isInAir:
                return False

            # Verificar blocos abaixo
            air_blocks = 0
            for offset_y in range(1, BotConfig.MAX_FALL_HEIGHT + 1):
                block = self.bot.blockAt(x, y - offset_y, z)
                if block:
                    if block.name in BotConfig.SAFE_BLOCKS:
                        return False
                    if block.name == "air":
                        air_blocks += 1
                    else:
                        return False  # Encontrou um bloco sólido

            return air_blocks >= BotConfig.MAX_FALL_HEIGHT

        except Exception as e:
            self.logger.error(f"Erro ao verificar queda: {str(e)}")
            return False

    def check_dangerous_blocks(self):
        try:
            position = self.bot.entity.position
            x = math.floor(position.x)
            y = math.floor(position.y)
            z = math.floor(position.z)

            for offset_x in range(-1, 2):
                for offset_y in range(0, 2):  # Checando apenas no nível do bot e acima
                    for offset_z in range(-1, 2):
                        block = self.bot.blockAt(
                            x + offset_x,
                            y + offset_y,
                            z + offset_z
                        )
                        if block and block.name in BotConfig.DANGER_BLOCKS:
                            return True
            return False
        except Exception as e:
            self.logger.error(f"Erro ao verificar blocos perigosos: {str(e)}")
            return False

    def emergency_stop(self):
        try:
            self.bot.pathfinder.setGoal(None)
            self.logger.warning("Parada de emergência ativada - movimento interrompido por segurança")
        except Exception as e:
            self.logger.error(f"Erro ao executar parada de emergência: {str(e)}")