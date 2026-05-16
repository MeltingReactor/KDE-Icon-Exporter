# KDE Icon Exporter
A simple program to extract system icons as **.svg** files.

***This script is intended for use on **Fedora 44 & KDE v6.6.4**.***

<details>
  <summary><strong>Installation</strong></summary>

1. Download **install.sh** by running this command:
```bash
curl -s https://api.github.com/repos/MeltingReactor/KDE-Icon-Exporter/releases/latest \
| grep '"browser_download_url":' \
| grep 'install.sh' \
| head -n1 \
| sed -E 's/.*"([^"]+)".*/\1/' \
| xargs curl -L -o install.sh
```
3. Run `bash ./install.sh` in the folder containing the script.
4. Run `./start.sh`.
</details>
