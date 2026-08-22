:: Copies the Rainmeter 4.5.17 installer from the NAS, runs it, copies the RS Cutter skin path to clipboard,
:: and cleans up the installer files afterwards.

xcopy /s \\10.1.0.1\nas-share\98_Rainmeter\Rainmeter-4.5.17.exe /d C:\Users\user\Desktop
echo Warte auf Rainmeter...

echo Installiere Rainmeter...
C:\Users\user\Desktop\Rainmeter-4.5.17.exe

echo|set/p=\\10.1.0.1\nas-share\98_Rainmeter\Skins|clip

del Rainmeter-4.5.17.exe
del rainmeter_install_4_5_17.bat