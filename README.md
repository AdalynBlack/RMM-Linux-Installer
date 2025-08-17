## RMM Linux Installer
A simple wrapper to install and launch Rumble Mod Manager

## Installation
1. Clone the repository
2. Run `pip install -r requirements.txt`, or install `vdf` and `loguru` through your package manager
3. Set `WINEDLLOVERRIDES="version=n,b"` in Rumble's launch options
4. Run RMM-Install.py

### Setting up a desktop shortcut
1. Modify `Exec` in `RMM.desktop` to be the full qualified path to `RMM-Install.py`
    - `~` will *not* expand to `/home/user`
2. Copy `RMM.png` to `~/.local/share/icons`

## Known Issues
Rumble Mod Manager cannot launch Rumble in VR mode, as it normally does so by launching game through steam.exe.
To launch the game with mods, add `WINEDLLOVERRIDES="version=n,b" %command%` to the launch options in steam.
