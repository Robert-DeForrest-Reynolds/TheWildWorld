from time import strftime
import logging
import logging.handlers

class GD: # Global Data
    def __init__(self):
        self.Logger = logging.getLogger('discord')
        self.Logger.setLevel(logging.DEBUG)
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
        self.Logger.addHandler(Handler)
        
        self.Guild = None
        self.Members = {}
        self.Channels = {}
        self.Database = None
        self.Players = {}
        self.Key = None
        self.KeyType = None
        self.Debug = False
        self.Unstable = False
        self.PlayerPanels = {}