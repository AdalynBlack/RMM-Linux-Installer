#!/bin/python3

import vdf
from loguru import logger
from pathlib import Path
from os.path import expanduser
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from typing import Final
from subprocess import run as subprocess_run

RMM_REPO_AUTHOR: Final[str] = 'xLoadingx'
RMM_REPO_NAME:   Final[str] = 'Rumble-Mod-Manager'

RUMBLE_APPID: Final[int] = 890550

STEAM_ROOT_PATH = '~/.local/share/Steam'

def drive_c_path() -> Path:
    logger.info(f'Automatically detecting install location')
    library_folders = vdf.parse(open(expanduser(f'{STEAM_ROOT_PATH}/steamapps/libraryfolders.vdf')))['libraryfolders']

    for folder in library_folders.values():
        if not f'{RUMBLE_APPID}' in folder['apps']:
            continue
        drive_c = Path(f'{folder["path"]}/steamapps/compatdata/{RUMBLE_APPID}/pfx/drive_c')
        assert drive_c.is_dir(), f'No compatdata found at {drive_c}'

        logger.info(f'Successfully located Rumble\'s wine prefix')
        return drive_c

    critical(f'Rumble({RUMBLE_APPID}) installation path not detected. Please ensure the game is installed, and that the steam root folder can be accessed at {STEAM_ROOT_PATH}')
    exit(1)

def download_and_install(install_path: Path):
    logger.info(f'Downloading Manager.zip from github.com/{RMM_REPO_AUTHOR}/{RMM_REPO_NAME}/releases');
    resp = urlopen(f'https://github.com/{RMM_REPO_AUTHOR}/{RMM_REPO_NAME}/releases/latest/download/Manager.zip')

    logger.info(f'Extracting Manager.zip to {install_path}')
    ZipFile(BytesIO(resp.read())).extractall(path=install_path)

def install_dotnet(drive_c: Path, install_path: Path):
    # Bypass winetricks's install check because it takes too long
    winetricks_log_path = drive_c / '..' / 'winetricks.log'

    if winetricks_log_path.is_file():
        with open(winetricks_log_path, 'r') as winetricks_log:
            log_contents = winetricks_log.read()
            if all(component in log_contents for component in ['dotnetdesktop8', 'dotnetdesktop6']):
                return

    # Dotnet Desktop isn't logged as being installed, so install it
    logger.info('dotnetdesktop has not been installed by protontricks yet. Installing dotnetdesktop6 and dotnetdesktop8')
    subprocess_run(['protontricks', f'{RUMBLE_APPID}', 'dotnetdesktop8'], check=True, cwd=install_path)
    subprocess_run(['protontricks', f'{RUMBLE_APPID}', 'dotnetdesktop6'], check=True, cwd=install_path)


def main():
    drive_c = drive_c_path()
    install_path = drive_c / 'Program Files' / 'Rumble-Mod-Manager'
    install_path.mkdir(exist_ok=True)

    if not (install_path / 'Rumble Mod Manager.exe').is_file():
        download_and_install(install_path)
        logger.warning('Rumble Mod Manager will not be able to launch Rumble in either modded or vanilla')
        logger.warning('As a workaround, please add the following launch options to Rumble: \'WINEDLLOVERRIDES="version=n,b" %command%\'')
        logger.warning('Press enter to continue.')
        input()
    
    install_dotnet(drive_c, install_path)

    logger.info('Starting Rumble Mod Manager via protontricks-launch')
    subprocess_run(['protontricks-launch', '--appid', f'{RUMBLE_APPID}', f'{install_path / "Rumble Mod Manager.exe"}'], cwd=install_path)

if __name__ == '__main__':
    main()
