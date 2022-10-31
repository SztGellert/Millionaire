#!/bin/bash
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10
sudo apt install python3-pip
sudo apt install pythonpy
pip install pipreqs
pipreqs .
pip install -r requirements.txt
cd ./bin || exit
cat <<EOF1 >create_linux_desktop_launcher.sh
#!/bin/bash
path_to_millionaire=\$(readlink -f ../millionaire/runner.py)
path_to_icon=\$(readlink -f ../loim.png)
chmod +x ../millionaire/runner.py
cd ~/Desktop || exit
cat <<EOF >millionaire.desktop
[Desktop Entry]
Type=Application
Terminal=true
Name=Millionaire
Icon=\$path_to_icon
Exec=\$path_to_millionaire
EOF
chmod +x millionaire.desktop
gio set millionaire.desktop metadata::trusted true
EOF1
path_to_millionaire=$(echo readlink -f ../millionaire/runner.py)
cat <<EOF > millionaire.sh
#!/bin/bash
python3 $($path_to_millionaire)
EOF