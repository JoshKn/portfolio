:: Full post-production workstation update script for workstation editing suites.
:: Copies and silently installs Program , Nvidia GPU drivers, FX, Software,
:: and Blackmagic Desktop Video — all running in the background in parallel where possible.

@echo off

set /p UserName=Ist der angemeldete Nutzer user oder user1? 

IF NOT EXIST "%ProgramFiles%\7-Zip\7z.exe" (
    echo Installiere 7-Zip...
    "\\nas-server\nas-share\Installer\7z2409-x64.exe" /S
)
echo 7-Zip ist installiert :)
echo .

echo Entpacke und Installiere Program im Hintergrund...
xcopy /s \\nas-server\nas-share\Installer\25.12.0_Win.zip /d C:\Users\%UserName%\Desktop\updates\
:: creates sub-script to run the installation in the background
:: {GUID} von Program 24.6.0
echo msiexec.exe /x "{123456789}" /qb /norestart > "C:\Users\%UserName%\Desktop\updates\Program_install_bg.bat"
echo "%ProgramFiles%\7-Zip\7z.exe" x "C:\Users\%UserName%\Desktop\updates\25.12.0_Win.zip" -o"C:\Users\%UserName%\Desktop\updates" -y >> "C:\Users\%UserName%\Desktop\updates\Program_install_bg.bat"
echo "C:\Users\%UserName%\Desktop\updates\Install .exe" /s /v"/qb REMOVE=\"OpenNDI,OpenSRT\" OPEN_NDI_SELECT=\"\" OPEN_SRT_SELECT=\"\" ADDLOCAL=\"EditorTranscode,,OTSProgramHuddle\" /norestart /l*v install.log" >> "C:\Users\%UserName%\Desktop\updates\Program_install_bg.bat"
echo exit >> "C:\Users\%UserName%\Desktop\updates\Program_install_bg.bat"
start "Program Install" "C:\Users\%UserName%\Desktop\updates\Program_install_bg.bat"
echo .

echo Installiere FX im Hintergrund...
xcopy /s "\\nas-server\nas-share\Installer\FX-avx-install-2026-cuda10.exe" /d C:\Users\%UserName%\Desktop\updates\
echo "C:\Users\%UserName%\Desktop\updates\FX-avx-install-2026-cuda10.exe" /SILENT > "C:\Users\%UserName%\Desktop\updates\FX_install_bg.bat"
echo exit >> "C:\Users\%UserName%\Desktop\updates\FX_install_bg.bat"
start "FX Install" "C:\Users\%UserName%\Desktop\updates\FX_install_bg.bat"
echo .

echo Installiere Software...
xcopy /s "\\nas-server\nas-share\Installer\Software_for_Program-6.0.23899.msi" /d C:\Users\%UserName%\Desktop\updates\
"C:\Users\%UserName%\Desktop\updates\Software_for_Program-6.0.23899.msi" /qb /norestart
echo .

echo Installiere Desktop Video...
xcopy /s "\\nas-server\nas-share\Installer\Desktop_Video_Installer_v15.3.1.msi" /d C:\Users\%UserName%\Desktop\updates\
"C:\Users\%UserName%\Desktop\updates\Desktop_Video_Installer_v15.3.1.msi" /qb /norestart
echo .

echo Installation abgeschlossen!
pause