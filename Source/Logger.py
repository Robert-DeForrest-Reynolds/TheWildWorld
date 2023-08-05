from time import strftime
import logging
import logging.handlers

Logger = logging.getLogger('discord')
Logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)
Handler = logging.handlers.RotatingFileHandler(
    filename=f'Source\\Logs\\{strftime("%d_%m_%Y_%H-%M")}.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
Handler.setFormatter(formatter)
Logger.addHandler(Handler)