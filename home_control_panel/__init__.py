import os
import sys
from home_control_panel.app.app import app


def main():
    sys.exit(app.exec_())


def setup():
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/temp'):
        os.mkdir('data/temp')
    if not os.path.exists('data/temp/video'):
        os.mkdir('data/temp/video')
    if not os.path.exists('data/temp/image'):
        os.mkdir('data/temp/image')


setup()


if __name__ == "__main__":
    print("Running Home Control Panel")
    main()
