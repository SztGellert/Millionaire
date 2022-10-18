pip install -r requirements.txt
pyinstaller --distpath "./bin" --noconfirm --onefile --console --icon "./loim.png" --name=millionaire "./millionaire/runner.py"
COPY ".\bin\millionaire.exe" ".\millionaire.exe"
millionaire.exe
pause