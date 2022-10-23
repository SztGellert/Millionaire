#!/bin/bash
path_to_millionaire=$(readlink -f ../millionaire/runner.py)
path_to_icon=$(readlink -f ../loim.png)
cd ~/Desktop || exit
cat <<EOF >millionaire.desktop
[Desktop Entry]
Type=Application
Terminal=true
Name=Millionaire
Icon=$path_to_icon
Exec=$path_to_millionaire
EOF
chmod +x "$path_to_millionaire"
chmod +x millionaire.desktop
gio set millionaire.desktop metadata::trusted true
