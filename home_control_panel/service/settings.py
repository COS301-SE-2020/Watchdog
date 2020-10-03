from ..service import config

conf = config.configure()

class Settings:
    def __init__(self):
        self.settings = conf['settings']
        self.video = conf['video']

    def change_setting(self, *config_trail, value):
        for index in range(len(config_trail)):
            if index == len(config_trail) - 1:
                self.settings[config_trail[index]] = value
        config.update_config('settings', self.settings)

    def update_settings(self, settings: dict):
        """
        Updates settings object
        :param settings: (dict) {
            "site": (str),
            "address": (str),
            "live": (bool),
            "recording_ratio": (str(float))
        },
        :return:
        """
        for key in self.settings:
            if settings[key]:
                self.settings[key] = settings[key]

        config.update_config('settings', self.settings)

    def update_video_settings(self, video: dict):
        """
        Updates all 'video' settings in the config
        :param video: (dict) {
            'video': {
                'resolution': (dict) {
                    'width': (int),
                    'height': (int)
                },
                'clip_length': (float),
                'frames_per_second': (int)
            }
        }
        :return:
        """
        for key in self.video:
            if video[key]:
                self.video[key] = video[key]

        config.update_config('video', self.video)
