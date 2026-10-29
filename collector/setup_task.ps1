# Registers a Windows Task Scheduler job that runs the TomTom collector every 12 hours.
# Run once in PowerShell:  powershell -ExecutionPolicy Bypass -File setup_task.ps1
$script = Join-Path $PSScriptRoot "collect_tomtom_live.py"
$py = (Get-Command py).Source
$action  = New-ScheduledTaskAction -Execute $py -Argument "-I `"$script`"" -WorkingDirectory $PSScriptRoot
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddHours(6) -RepetitionInterval (New-TimeSpan -Hours 12) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "TomTomTrafficCollector" -Action $action -Trigger $trigger -Settings $settings -Description "Collects TomTom Traffic Index live feed for 490 cities twice daily" -Force
Write-Host "Task 'TomTomTrafficCollector' registered. Runs every 12 hours starting 06:00 today. Check with: schtasks /query /tn TomTomTrafficCollector"
