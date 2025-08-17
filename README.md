## RMM Linux Installer
A simple wrapper to install and launch Rumble Mod Manager

## Known Issues
Rumble Mod Manager cannot launch Rumble in VR mode, as it normally launches the game through steam.exe.
To launch the game with mods, add `WINEDLLOVERRIDES="version=n,b" %command%` to the launch options in steam.
