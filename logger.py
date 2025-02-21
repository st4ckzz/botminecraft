import logging
from config.config import BotConfig
from collections import defaultdict
from time import time

class DuplicateFilter(logging.Filter):
    def __init__(self, logger):
        super().__init__()
        self.message_counts = defaultdict(int)
        self.last_log_time = defaultdict(float)
        self.logger = logger
        self.RESET_INTERVAL = 60  # Reset contador a cada 60 segundos

    def filter(self, record):
        msg = record.getMessage()
        current_time = time()

        # Reset contador se passou o intervalo
        if current_time - self.last_log_time[msg] > self.RESET_INTERVAL:
            if self.message_counts[msg] > 1:
                self.logger.info(f"[{self.message_counts[msg]}x] {msg}")
            self.message_counts[msg] = 0

        self.message_counts[msg] += 1
        self.last_log_time[msg] = current_time

        # Só mostra a mensagem na primeira vez
        return self.message_counts[msg] == 1

def setup_logger():
    logger = logging.getLogger('minecraft_bot')
    logger.setLevel(getattr(logging, BotConfig.LOG_LEVEL))

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Filtro para mensagens duplicadas
    duplicate_filter = DuplicateFilter(logger)
    logger.addFilter(duplicate_filter)

    # Handler para arquivo
    file_handler = logging.FileHandler(BotConfig.LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger