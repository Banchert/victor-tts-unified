# VICTOR-TTS Docker Build Test (CPU Version)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VICTOR-TTS Docker Build Test (CPU Version)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Testing Docker build with CPU version..." -ForegroundColor Yellow
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

Write-Host "Building Docker image with CPU version..." -ForegroundColor Green
docker build -f Dockerfile.cpu -t victor-tts-cpu:test ..

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS: Docker build completed!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "To run the container:" -ForegroundColor White
    Write-Host "docker run -p 6969:6969 -p 7000:7000 victor-tts-cpu:test" -ForegroundColor Gray
    Write-Host ""
    Write-Host "To test with docker-compose:" -ForegroundColor White
    Write-Host "docker-compose -f docker-compose.simple.yml up" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "ERROR: Docker build failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the error messages above for details." -ForegroundColor Yellow
    Write-Host ""
}

Read-Host "Press Enter to continue" 