:: Resets a local Windows user account password using the Net user command.

@echo off

set user=user
set newPass=password

echo Das Passwort von %user% wird neu vergeben.
Net user %user% %newPass%