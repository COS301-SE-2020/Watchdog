from app.app import HomeControlPanel


def main():
    home = HomeControlPanel()  # change to pass in user object
    home.start()


if __name__ == "__main__":
    print("Running Home Control Panel")
    main()
