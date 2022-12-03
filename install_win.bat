pip3 install pyinstaller
pip3 install pillow
pip3 install pipreqs
pipreqs .
pip3 install -r requirements.txt
pyinstaller --paths "./millionaire" --distpath "./bin" --noconfirm --onefile --console --icon "./loim.png" --name=millionaire "./runner.py"
set TARGET=Convert-Path .\bin\millionaire.exe
set SHORTCUT='.\Millionaire.lnk'
set WORKINGFOLDER=Convert-Path .\millionaire
set PWS=powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile
%PWS% -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(%SHORTCUT%); $S.WorkingDirectory = %WORKINGFOLDER%; $S.TargetPath = %TARGET%; $S.Save()"
echo set TARGET=Convert-Path .\millionaire.exe > .\bin\create_windows_desktop_launcher.bat
echo set SHORTCUT=[Environment]::GetFolderPath('Desktop') + '\Millionaire.lnk'>> .\bin\create_windows_desktop_launcher.bat
echo set WORKINGFOLDER=Convert-Path ..\millionaire >> .\bin\create_windows_desktop_launcher.bat
echo set PWS=powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile >> .\bin\create_windows_desktop_launcher.bat
echo %%PWS%% -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(%%SHORTCUT%%); $S.WorkingDirectory = %%WORKINGFOLDER%%; $S.TargetPath = %%TARGET%%; $S.Save()" >> .\bin\create_windows_desktop_launcher.bat