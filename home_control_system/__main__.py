import random
from app.home import HomeControlPanel
from server.server import Server


def main():
    port = random.randint(49152, 65535)
    # public_ip = requests.get('http://checkip.amazonaws.com').text.strip()
    home = HomeControlPanel(Server('127.0.0.1', 'Home', port))
    home.start()


if __name__ == "__main__":
    print("Running Home Control Panel")
    main()
