# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_all, copy_metadata

datas = []
binaries = []
hiddenimports = ['moviepy', 'imageio', 'imageio_ffmpeg', 'moviepy.audio.fx.all', 'decorator', 'tqdm', 'proglog', 'customtkinter', 'plyer', 'plyer.platforms.win.notification']

# Collect metadata (crucial for moviepy/imageio)
try:
    datas += collect_all('customtkinter')[0]  # Add customtkinter data
    datas += collect_all('plyer')[0]          # Add plyer data
    datas += copy_metadata('imageio')
    datas += copy_metadata('imageio_ffmpeg')
    datas += copy_metadata('moviepy')
    datas += copy_metadata('decorator')
    datas += copy_metadata('tqdm')
    datas += copy_metadata('proglog')
except Exception as e:
    print(f"Warning: Could not copy metadata: {e}")

# Collect all moviepy dependencies just to be safe
try:
    tmp_ret = collect_all('moviepy')
    datas += tmp_ret[0]
    binaries += tmp_ret[1]
    hiddenimports += tmp_ret[2]
except Exception as e:
    print(f"Warning: Could not collect moviepy: {e}")

try:
    tmp_ret = collect_all('imageio_ffmpeg')
    datas += tmp_ret[0]
    binaries += tmp_ret[1]
    hiddenimports += tmp_ret[2]
except Exception as e:
    print(f"Warning: Could not collect imageio_ffmpeg: {e}")

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pyconverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
