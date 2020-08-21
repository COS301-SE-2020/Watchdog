from service import config

conf = config.configure()

class Settings:
    def __init__(self):
        self.settings = conf['settings']

    def change_setting(self, *config_trail, value):
        for index in range(len(config_trail)):
            if index == len(config_trail) - 1:
                self.settings[config_trail[index]] = value
        config.update_config('settings', self.settings)
