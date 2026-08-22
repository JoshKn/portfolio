:: Updates the saved Windows Credential Manager entry for a network share (e.g. NAS).
:: Deletes the old credential and registers the new username/password for the target server.

@echo off

set target=nas-server
set user=username
set newPass=password

cmdkey /delete:%target%

cmdkey /add:%target% /user:%user% /pass:%newPass%
echo User %user% wurde fuer %target% hinzugefuegt

pause