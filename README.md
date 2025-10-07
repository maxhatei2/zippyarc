# zippyarc
Small and lightweight archiver

Fast archive Python-made archiver that looks good. Based on zipfile and py7zr.

Can support:
- ZIP archive making with compression type choosing
- 7z/7zip archive making with compression type choosing and volume

Will support:

- Checking files for malware before making archive or when extracting
- Reading/extracting ZIP/7z
- Reading RAR
- Passwords for ZIP/7z archives

## Why is it not loading?

It may take 5-10 seconds to start up, because it's made in PyInstaller, and being a onefile, it may start bad.

**For now, only macOS DMGs are available. A Windows EXE will be provided in the next release.**

If you want to run it and have already a Python interpreter, then you will need to install those libraries:

`pip install customtkinter`

`pip install screeninfo`

`pip install CTkListbox`

`pip install py7zr`

Thanks!
