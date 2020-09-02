import os
import sys
from home_control_panel import main

if __name__ == "__main__":
    print("Running Home Control Panel")
    main()


# Translate asset paths to useable format for PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)