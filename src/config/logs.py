import logging


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[38;5;32m',  # Light Blue
        'INFO': '\033[38;5;117m',  # Cyan
        'WARNING': '\033[38;5;178m',  # Yellow-Orange
        'ERROR': '\033[38;5;208m',  # Orange
        'CRITICAL': '\033[38;5;214m'  # Light Orange
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.msg = f"{log_color}{record.msg}{self.RESET}"
        return super().format(record)


# Configure logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = ColoredFormatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Suppress all Speckle-related logs
for logger_name in logging.root.manager.loggerDict:
    if logger_name.startswith('specklepy'):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.CRITICAL)
        logger.propagate = False
