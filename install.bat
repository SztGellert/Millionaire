pip install -r requirements.txt
pyinstaller --distpath "./bin" --noconfirm --onefile --console --icon "./loim.png" "./millionaire.py"
COPY ".\bin\millionaire.exe" ".\millionaire.exe"
millionaire.exe