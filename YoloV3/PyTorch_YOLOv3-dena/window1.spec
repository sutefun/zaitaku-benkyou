# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['my_demo\\window1.py'],
             pathex=['C:\\Users\\user\\Google ドライブ\\machine_learning\\PyTorch_YOLOv3-master'],
             binaries=[],
             datas=[],
             hiddenimports=[
                'pkg_resources.py2_warn'
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='window1',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               Tree( 'my_demo/image_asset' , 'image_asset' ),
               Tree( 'config' , 'config' ),
               Tree( 'weights' , 'weights' ),
               strip=False,
               upx=True,
               upx_exclude=[],
               name='window1')
