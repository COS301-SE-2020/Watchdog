# -*- mode: python ; coding: utf-8 -*-
import os
import sys

spec_root = os.path.abspath(SPECPATH)

block_cipher = None


a = Analysis(['hcp.py'],
             pathex=[spec_root],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('./assets/styles/dark.css', './assets/styles/dark.css', 'DATA'),
            ('./assets/styles/light.css', './assets/styles/light.css', 'DATA'),
            ('./assets/icons/home.png', './assets/icons/home.png', 'DATA'),
            ('./assets/icons/icon.png', './assets/icons/icon.png', 'DATA'),
            ('./assets/icons/pause.png', './assets/icons/pause.png', 'DATA'),
            ('./assets/icons/play.png', './assets/icons/play.png', 'DATA'),
            ('./assets/icons/plus.png', './assets/icons/plus.png', 'DATA'),
            ('./assets/icons/quit.png', './assets/icons/quit.png', 'DATA'),
            ('./assets/icons/settings.png', './assets/icons/settings.png', 'DATA'),
            ('./assets/icons/signal_off.png', './assets/icons/signal_off.png', 'DATA'),
            ('./assets/icons/signal_on.png', './assets/icons/signal_on.png', 'DATA'),
            ('./assets/icons/user.png', './assets/icons/user.png', 'DATA'),
            ('./assets/icons/watchdog.png', './assets/icons/watchdog.png', 'DATA'),
            ('./data/.conf', './data/.conf', 'DATA'),
            ('./data/.logs', './data/.logs', 'DATA'),
            ('./data/.hash', './data/.hash', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

if sys.platform == 'darwin':
  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='HCP',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=False,
            icon='assets/icon.icns')

# Package the executable file into .app if on OS X
if sys.platform == 'darwin':
   app = BUNDLE(exe,
                name='HCP.app',
                info_plist={
                  'NSHighResolutionCapable': 'True'
                },
                icon='assets/icon.icns')

# Generate an executable file
# Notice that the icon is a .ico file, unlike macOS
# Also note that console=False
if sys.platform == 'win32' or sys.platform == 'win64' or sys.platform == 'linux':
    exe = EXE(pyz,
            a.scripts,
            [],
            exclude_binaries=True,
            name='HCP',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            console=True )

    coll = COLLECT(exe,
                a.binaries,
                a.zipfiles,
                a.datas,
                strip=False,
                debug=True,
                upx=True,
                upx_exclude=[],
                name='HCP',
                icon='assets/icon.ico')