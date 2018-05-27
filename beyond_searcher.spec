block_cipher = None

a = Analysis(['beyond_search.py'],
             pathex=['ENTER PATH HERE'],
             binaries=[],
             datas=[],
             hiddenimports=["wx.adv", "wx.html", "wx.xml"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='beyond_search',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
