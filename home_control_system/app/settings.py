from service import config

conf = config.configure()

class Settings:
    def __init__(self):
        self.site = conf['settings']['site']
        self.address = conf['settings']['address']
