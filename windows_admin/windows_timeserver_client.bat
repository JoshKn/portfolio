:: Configures this machine as a Windows Time Service (w32tm) client pointing at a specific time server IP.
:: Must be run as Administrator. Sets the peer, starts the service, forces a resync, and confirms the source.

:: run as admin

:: configure Time Server IP (e.g. 10.1.0.9)
w32tm /config /manualpeerlist:"TimeServer-IP" /syncfromflags:manual /reliable:yes /update

:: net stop w32time ::not necessary if service not started
net start w32time

w32tm /resync

w32tm /query /source