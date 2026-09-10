$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
$envFile = Join-Path $projectRoot '.env'

if (-not (Test-Path $python)) {
    Write-Error 'Virtual environment not found. Run: py -m venv .venv'
}

if (-not (Test-Path $envFile)) {
    Write-Error 'Missing .env file. Run: Copy-Item .env.example .env, then configure it.'
}

Set-Location $projectRoot
$frontendServer = Start-Process -FilePath $python -ArgumentList '-m', 'http.server', '5500', '--directory', 'frontend' -PassThru

try {
    Write-Host 'Frontend: http://localhost:5500'
    Write-Host 'Backend:  http://localhost:5000'
    Write-Host 'Press Ctrl+C to stop both servers.'
    & $python -m backend.app
}
finally {
    if ($frontendServer -and -not $frontendServer.HasExited) {
        Stop-Process -Id $frontendServer.Id -Force
    }
}
