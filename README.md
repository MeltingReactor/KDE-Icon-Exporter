# KDE Icon Exporter
A simple program to extract system icons as **.svg** files.

***This script is intended for use on **Fedora 44 & KDE v6.6.4**.***

## Installation

This command will download **install.sh** and run the **start.sh** script:
```bash
bash <(curl -s https://raw.githubusercontent.com/MeltingReactor/KDE-Icon-Exporter/main/install.sh) && bash start.sh
```

If you wish to run the app standalone with python, download the [main.py](https://github.com/MeltingReactor/KDE-Icon-Exporter/blob/main/main.py) file and run it with
```bash
python3 main.py
```

## Usage
Once installation has finished, the app will open. If you wish to reopen the app, navigate to the folder where you ran `install.sh` and from that folder run this command:
```bash
bash start.sh
```
> [!IMPORTANT]
> Currently, the .svg file conversion has some issues.
> I recommend just using the raster image.
