$filePath = "$PSScriptRoot\config.py"
if ($args[0] -eq 'd') {
    Remove-Item $filePath
    Write-Host "Config Deleted"
}
if ($args[0] -eq 'o') {
    Invoke-Item "index.html"
    exit 0
}
if(-Not(Test-Path -Path $filePath)) {
    Write-Host "Creating new config"
    New-Item -Name "config.py" -Path $PSScriptRoot -ItemType File | Out-Null
    $client_id = Read-Host -Prompt "Client ID"
    $client_secret = Read-Host -Prompt "Client secret"
    $skips = Read-Host -Prompt "Skips"
    Add-Content -Path $filePath -Value "client_id = '$client_id'"
    Add-Content -Path $filePath -Value "client_secret = '$client_secret'"
    Add-Content -Path $filePath -Value "skips = [$skips]"
}
py "$PSScriptRoot\run.py"
