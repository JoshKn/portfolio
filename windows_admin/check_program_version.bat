:: Uses WMIC to query and print the installed version numbers of Program  and sharedStorage (plcconsole.exe).
:: Run this on a workstation to quickly verify which versions are currently installed.

wmic datafile where Name="C:\Program Files\Program\Program \Program.exe" get Version /format:table
wmic datafile where Name="C:\\Windows\\sharedStorage\\plcconsole.exe" get Name,Version /format:table

pause