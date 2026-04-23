$filePath = "$PSScriptRoot\config.py"
if ($args[0] -eq 'd') {
    Remove-Item $filePath
    Write-Host "Config Deleted"
}
py "$PSScriptRoot\run.py"
