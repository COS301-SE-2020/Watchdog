"""
Interface Class:
- Abstract class that generalizes to Actual UI
"""
import os
from abc import ABC


class Interface:
    def __init__(self, controller_events: dict = None):
        """
        Interface Constructor
        - Creates data directories if they don't exist
        - Accepts the controller events that initiate functionality
        :param controller_events: (dict) Does all the backend logic for each event - {
            "start": func() - start controller,
            "end": func() - end controller,
            "login": func(username, password) - does the login and returns True or False,
            "logout": func() - shuts down all background processes,
            "add_camera": func(protocol, ip, path, name, location) - adds a camera object,
            "remove_camera": func(id) - removes camera with camerae.id = id,
            "repair_camera": func(id) -
            "add_location": func(name) - adds a new location,
            "remove_location": func(id) - removes a location
        }
        """
        # Directory Structure
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists('data/temp'):
            os.mkdir('data/temp')
        if not os.path.exists('data/temp/video'):
            os.mkdir('data/temp/video')
        if not os.path.exists('data/temp/image'):
            os.mkdir('data/temp/image')
        # Utility Files
        if not os.path.exists('data/.conf'):
            with open('data/.conf', 'w'):
                pass
        if not os.path.exists('data/.hash'):
            with open('data/.hash', 'w'):
                pass
        if not os.path.exists('data/.logs'):
            with open('data/.logs', 'w'):
                pass

        self.controller_events = controller_events
        self.camera_elements = {}
        self.loggedIn = False

    # ---------------------------- Event Triggers ------------------------------- #
    def get_stream_object(self, camera_id):
        """
        Gets the Stream Object
        :param camera_id:
        :return: StreamObject
        """
        pass

    # ---------------------------- Event Triggers ------------------------------- #

    def trigger_add_camera(self, callback=None):
        """
        Fetches data from UI dialog and trigger controller.add_camera
        1. Open Dialog
        2. Validate data
        3. Pass in data to controller_event.add_camera
        :param callback: (func)
        :return: None
        """
        pass

    def trigger_remove_camera(self, camera_id, callback=None):
        """
        Triggers controller.remove_camera(camera_id)
        :param camera_id
        :param callback:
        :return:
        """
        pass

    def trigger_add_location(self, callback=None):
        """
        Gets data and triggers controller.add_location(data)
        :param callback:
        :return:
        """
        pass

    def trigger_remove_location(self, location_id, callback=None):
        """
        Triggers controller.remove_location(data)
        :param location_id
        :param callback
        :return:
        """
        pass

    def trigger_view_recordings(self, callback=None):
        """
        Fetched and displays all the Recordings
        :param callback:
        :return:
        """
        pass

    # ---------------------------- UI Manipulators ------------------------------- #

    def add_camera(self, location_label, camera_id, name, address, port, path, protocol, callback=None):
        """
        Adds Camera to UI
        :param location_label:
        :param camera_id:
        :param name:
        :param address:
        :param port:
        :param path:
        :param protocol:
        :param callback:
        :return:
        """
        pass

    def remove_camera(self, camera_id, callback=None):
        """
        Remove camera from UI
        :param camera_id
        :param callback: (func)
        :return: None
        """
        pass

    def add_location(self, location_label, callback=None):
        """
        Adds location to UI
        :param location_label
        :param callback:
        :return:
        """
        pass

    def remove_location(self, location_id, callback=None):
        """
        Removes location from UI
        :param location_id
        :param callback:
        :return:
        """
        pass

    def update_stream(self, camera_id, frame):
        """
        Updates UI camera stream
        :param camera_id
        :param frame
        :return:
        """
        pass

    # =================================================== #
    def login(self, callback=None):
        """
        Initiates login process and starts controller processes:
        1. Get login details
        2. Pass into controller_events.login and get status
        3. If status == true: start controller_events.start
        :param callback:
        :return:
        """
        self.loggedIn = True

    def logout(self, callback=None):
        """
        Stops controller processes and closes UI
        1. controller_events.logout
        2. controller_events.stop
        3. Stop UI and end process
        :param callback:
        :return:
        """
        self.loggedIn = False

    def attach_stream(self, camera_id, stream_obj):
        pass
