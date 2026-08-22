:: Full workstation/laptop setup script.
:: Clears the Program cache, then copies installers for Program, sharedStorage, Software, FX, and Remote
:: from the NAS to the current user's Desktop, and then triggers a Windows Update scan/download/install.

@echo off

set /p UserName=Ist der angemeldete Nutzer admin, user oder user1? 

echo Lösche Program Cache...
:: remove all content from ama -> folders + files
set folder="C:\\Users\\Public\\Documents\\Program \\AMA Management\\AMA Metadata Folders\\"
IF EXIST %folder% (
    cd /d %folder%
    for /F "delims=" %%i in ('dir /b') do ( rmdir "%%i" /s/q || del "%%i" /s/q)
    echo Inhalte aus %folder% wurden geloescht.
) else ( echo Ordner %folder% existiert nicht.)

set folder="C:\\Users\\Public\\Documents\\Program \\ProgramImageCache\\"
IF EXIST %folder% (
    cd /d %folder%
    for /F "delims=" %%i in ('dir /b') do ( rmdir "%%i" /s/q || del "%%i" /s/q)
    echo Inhalte aus %folder% wurden geloescht.
) else ( echo Ordner %folder% existiert nicht.)

echo Kopiere den Program Installer...
xcopy /s \\10.1.0.1\nas-share\03_Program_\Program_Patch_22.12.4_Win.msp /d C:\Users\%UserName%\Desktop\
xcopy /s \\10.1.0.1\nas-share\03_Program_\22.12.0_Win.zip /d C:\Users\%UserName%\Desktop\

echo Kopiere sharedStorage Skripte...
xcopy /s \\10.1.0.1\nas-share\02_sharedStorage\sharedStorage_Batch_Installer\sharedStorage_8_2_5\sharedStorage_shell_client_installer_8_2_5.bat /d C:\Users\%UserName%\Desktop\
xcopy /s \\10.1.0.1\nas-share\02_sharedStorage\sharedStorage_Batch_Server_Config\sharedStorage_CMD_Server_Config.bat /d C:\Users\%UserName%\Desktop\ 

echo Kopiere Software...
xcopy /s \\10.1.0.1\nas-share\05_Software_for_Program\Software_for_Program-5.3.17538.msi /d C:\Users\%UserName%\Desktop\

echo Kopiere FX...
xcopy /s \\10.1.0.1\nas-share\04_FX\FX-avx-install-2023.51.exe /d C:\Users\%UserName%\Desktop\

echo Kopiere Remote Streamer...
xcopy /s \\10.1.0.1\nas-share\07_Remote\Remote_Streamer_v3.5.0.5.exe /d C:\Users\%UserName%\Desktop\
echo|set /p=12345678|clip

echo Kopiere wallpaper...
xcopy /s \\10.1.0.1\nas-share\Hintergrund_32zu9_2022_01_05.png /d C:\Users\Public\Pictures\
%SystemRoot%\explorer.exe "C:\Users\Public\Pictures\"

echo Scanne nach Windows Updates...
UsoClient StartScan
echo Downloade Windows Updates...
UsoClient StartDownload
echo Installiere Windows Updates...
UsoClient StartInstall

echo Der Remote Code (12345678) ist in deiner Zwischenablage :)
del 00_installer_copy.bat