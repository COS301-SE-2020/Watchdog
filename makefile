run:
	python hcp.py

compile:
	pyinstaller hcp.py -n Watchdog --windowed --noconfirm --clean --icon=icon.ico
