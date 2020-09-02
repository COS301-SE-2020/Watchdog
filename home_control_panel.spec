# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['hcp.py'],
             pathex=[r'D:\\Users\\Jordan\\Shared_Folder\\Home_Control_Panel'],
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
            ('./assets/icons/plus.png', './assets/icons/plus.png', 'DATA'),
            ('./assets/icons/settings.png', './assets/icons/settings.png', 'DATA'),
            ('./assets/icons/signal_off.png', './assets/icons/signal_off.png', 'DATA'),
            ('./assets/icons/signal_on.png', './assets/icons/signal_on.png', 'DATA'),
            ('./assets/icons/user.png', './assets/icons/user.png', 'DATA'),
            ('./assets/icons/watchdog.png', './assets/icons/watchdog.png', 'DATA'),
            ('./assets/icons/watchdog_white.png', './assets/icons/watchdog_white.png', 'DATA'),
            ('./data/.conf', './data/.conf', 'DATA'),
            ('./data/.hash', './data/.hash', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
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
