"""
Interface Class:
"""
import os


class Interface:
    def __init__(self):
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists('data/temp'):
            os.mkdir('data/temp')
        if not os.path.exists('data/temp/video'):
            os.mkdir('data/temp/video')
        if not os.path.exists('data/temp/image'):
            os.mkdir('data/temp/image')

        self.loggedIn = False

    def login(self, callback=None):
        self.loggedIn = True

    def logout(self, callback=None):
        self.loggedIn = False

    def start(self, callback=None):
        pass

    def end(self, callback=None):
        pass

    def add_camera(self, callback=None):
        pass

    def remove_camera(self, callback=None):
        pass

    def add_location(self, callback=None):
        pass

    def remove_location(self, callback=None):
        pass
