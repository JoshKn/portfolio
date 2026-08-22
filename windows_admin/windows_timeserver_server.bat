:: Configures this machine as a Windows NTP time server by enabling the NtpServer registry key and restarting w32tm.
:: Must be run as Administrator on the machine that will serve as the authoritative time source.

:: run as admin
w32tm /config /reliable:yes /update
reg add HKLM\SYSTEM\CurrentControlSet\Services\W32Time\TimeProviders\NtpServer /v Enabled /t REG_DWORD /d 1 /f
net stop w32time
net start w32time