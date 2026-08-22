@echo off

echo Welche IP willst Du hinzufuegen?
echo Die 81 fuer ungerade Schnittplaetze
echo Die 82 fuer gerade Schnittplaetze
echo Die 83 fuer das kleine Buero + Server
echo Die 84 fuer das grosse Buero

echo.
set /p UserIP=Gib hier die IP ein die du hinzufuegen willst: & :: WICHTIG, dass zwischen "UserIP" und "=" kein Leerzeichen ist

echo.
echo Unmounte alle Drives...
plchld unmount -a

plchld set_setting disable_discovery  & :: sharedStorage Server wird nicht mehr gesucht, sondern es wird immer eine bestimmte IP angesteuert
    timeout /t 1 /nobreak >nul

echo Entferne alle Server IP-Adressen...
plchld set_setting white_list
plchld set_setting black_list

plchld remove_search 10.1.0.81
plchld remove_search 10.1.0.181
plchld remove_search 10.1.0.82
plchld remove_search 10.1.0.182
plchld remove_search 10.1.0.83
plchld remove_search 10.1.0.84
plchld remove_search 10.1.0.85
plchld remove_search 10.1.0.86
    timeout /t 1 /nobreak >nul

echo Fuege vom User angegebene IP-Adresse hinzu...
plchld add_search 10.1.0.%UserIP%

echo Fuege andere Terrablocks hinzu...
    timeout /t 1 /nobreak >nul

::for loop startet bei 1, geht in 1er Schritten und endet bei 4
for /l %%i in (1,1,4) do (
	if not 8%%i==%UserIP% (set IP%%i=10.1.0.8%%i)
) 

echo Adde nicht genutzte IP-Adressen zur Blacklist...
plchld set_setting peer_block_list %IP1% %IP2% %IP3% %IP4%
    timeout /t 1 /nobreak >nul

echo Starte den Profile Process neu...
plchld stop
    timeout /t 5 /nobreak >nul

plchld start
    timeout /t 1 /nobreak >nul

echo.
echo Starte sharedStorage...
start "" "C:\Windows\sharedStorage\plchd.exe"

echo.
echo Das Skript ist fertig. Druecke irgendeine Taste um es zu beenden. &pause>nul

:: removes installer files batch files that match the regex pattern
del sharedStorage_shell_client_*.bat

:: removes itself
(goto) 2>nul & del "%~f0"