$filePath = "$PSScriptRoot\config.py"
if ($args[0] -eq 'd') {
    Remove-Item $filePath
    Write-Host "Config Deleted"
}
if ($args[0] -eq 'o') {
    if (Test-Path -Path "$PSScriptRoot\complete.html") {
        Invoke-Item "$PSScriptRoot\complete.html"
    } elseif (Test-Path -Path "$PSScriptRoot\partial.html") {
        Invoke-Item "$PSScriptRoot\partial.html"
    } else {
        Write-Host "No output file"
    }
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
