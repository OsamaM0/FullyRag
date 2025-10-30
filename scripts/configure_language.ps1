# FullyRAG Language Configuration Script (PowerShell)
# This script helps configure the default language for the FullyRAG application

# Function to print colored messages
function Print-Info {
    param($message)
    Write-Host "ℹ️  $message" -ForegroundColor Blue
}

function Print-Success {
    param($message)
    Write-Host "✅ $message" -ForegroundColor Green
}

function Print-Warning {
    param($message)
    Write-Host "⚠️  $message" -ForegroundColor Yellow
}

function Print-Error {
    param($message)
    Write-Host "❌ $message" -ForegroundColor Red
}

# Check if .env file exists
$envFile = ".env"
if (-not (Test-Path $envFile)) {
    Print-Error ".env file not found!"
    Print-Info "Creating .env file from template..."
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Print-Success ".env file created"
    } else {
        Print-Error "No .env.example file found. Please create a .env file manually."
        exit 1
    }
}

Write-Host ""
Write-Host "======================================"
Write-Host "  FullyRAG Language Configuration"
Write-Host "======================================"
Write-Host ""

# Display current language setting
$currentLang = "not set"
if (Test-Path $envFile) {
    $content = Get-Content $envFile
    $langLine = $content | Where-Object { $_ -match "^LANGUAGE=" }
    if ($langLine) {
        $currentLang = $langLine -replace "^LANGUAGE=", ""
    }
}

Print-Info "Current language setting: $currentLang"
Write-Host ""

# Display available languages
Write-Host "Available languages:"
Write-Host "  1) English (en/english)"
Write-Host "  2) Arabic (ar/arabic) - RTL support"
Write-Host "  q) Quit without changes"
Write-Host ""

# Get user choice
$choice = Read-Host "Select language (1-2, or q to quit)"

$newLang = ""
$displayName = ""

switch ($choice) {
    "1" {
        $newLang = "english"
        $displayName = "English"
    }
    "2" {
        $newLang = "arabic"
        $displayName = "Arabic (العربية)"
    }
    { $_ -in "q", "Q" } {
        Print-Info "No changes made. Exiting..."
        exit 0
    }
    default {
        Print-Error "Invalid choice. Exiting..."
        exit 1
    }
}

Write-Host ""
Print-Info "Setting language to: $displayName"

# Read .env file
$envContent = Get-Content $envFile

# Check if LANGUAGE exists and update or add it
$languageExists = $false
$newContent = @()

foreach ($line in $envContent) {
    if ($line -match "^LANGUAGE=") {
        $newContent += "LANGUAGE=$newLang"
        $languageExists = $true
    } else {
        $newContent += $line
    }
}

if (-not $languageExists) {
    $newContent += "LANGUAGE=$newLang"
}

# Write back to .env file
$newContent | Set-Content $envFile

if ($languageExists) {
    Print-Success "Updated LANGUAGE setting in .env"
} else {
    Print-Success "Added LANGUAGE setting to .env"
}

Write-Host ""
Print-Success "Language configuration complete!"
Write-Host ""
Print-Info "Next steps:"
Write-Host "  1. Restart your FullyRAG application"
Write-Host "  2. The UI will now display in $displayName"
Write-Host "  3. Users can still change language using the sidebar selector"
Write-Host ""

# Check if language file exists
$langFile = ".variables/demo_fully_rag/display_texts"
if ($newLang -eq "arabic") {
    $langFile = "$langFile.ar.json"
} elseif ($newLang -eq "english") {
    $langFile = "$langFile.json"
}

if (Test-Path $langFile) {
    Print-Success "Language file found: $langFile"
} else {
    Print-Warning "Language file not found: $langFile"
    Print-Info "Make sure the language file exists before starting the application"
}

Write-Host ""
Print-Info "To restart the application:"
Write-Host "  • Docker: docker-compose restart"
Write-Host "  • Local: Stop and restart your Streamlit server"
Write-Host ""
