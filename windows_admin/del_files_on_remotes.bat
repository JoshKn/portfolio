:: Deletes all files and subdirectories inside the .ffastrans_work_root folder on remote machines 10.1.0.4 through 10.1.0.9.
:: Used to clean up FFAStrans working directories across the render farm nodes after a job run.

@echo off
setlocal enableDelayedExpansion

for /l %%i in (4,1,9) do (
	set dest=\\10.1.0.%%i\.ffastrans_work_root
	echo !dest!
	del /f /s /q !dest!\*
	for /d %%x in (!dest!\*) do @rd /s /q "%%x"
)
pause