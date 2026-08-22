# Cleans up the FFAStrans cache on a given drive by deleting files and folders older than 7 days.
# Accepts a -TargetDrive parameter (default: "E:"). Logs success or failure with a timestamp to the NAS.
# Replaces the separate clear_ffastrans_cache.ps1 and clear_ffastrans_cache_DriveF.ps1 scripts.
# Usage: .\clear_ffastrans_cache.ps1 -TargetDrive "F:"

param(
    [string]$TargetDrive = "E:"
)

# set logging paths
$LogFile = "\\nas-server\nas-share\Personen\user\logging\clear_ffastrans_cache.log"
$LogFileError = "C:\Users\$env:username\Desktop\ErrorLog.log"

# write current time & log message to file
function WriteLog {
    Param ([string]$file, [string]$LogString)
    $Stamp = (Get-Date).toString("yyyy-MM-dd HH:mm:ss")
    $LogMessage = "$Stamp $env:computername - $LogString"
    Add-content $file -value $LogMessage
}

# cleanup directory
$targetDir = "$TargetDrive\"

# calculate the date from a week ago
$oneWeekAgo = (Get-Date).AddDays(-7)

$ErrorActionPreference = "Stop"
try {
    # recursively delete files older than $oneWeekAgo
    Get-ChildItem -Path $targetDir -Recurse | Where-Object { $_.LastWriteTime -lt $oneWeekAgo } | Remove-Item -Force -Recurse

    # recursively delete empty folders
    Get-ChildItem -Path $targetDir -Recurse | Where-Object { $_.PSIsContainer -and @(Get-ChildItem -Path $_.FullName -Force).Count -eq 0 } | Remove-Item -Force

    WriteLog $LogFile "FFAStrans Cache on volume $targetDir was cleared successfully."
}
catch {
    WriteLog $LogFileError "Cleaning FFAStrans Cache on volume $targetDir ran into an error."
}
