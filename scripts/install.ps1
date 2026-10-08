#Requires -Version 5.1
<#
.SYNOPSIS
  Install Nature Portfolio skills from this repo into Cursor / Claude / Codex skill dirs.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/install.ps1

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 -ConfigPath "C:\path\config.yaml"
#>
param(
    [string]$ConfigPath = "",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$BundleRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$SkillsSrc = Join-Path $BundleRoot "skills"
$UserHome = $env:USERPROFILE

if (-not $ConfigPath) { $ConfigPath = Join-Path $BundleRoot "config.yaml" }
if (-not (Test-Path $ConfigPath)) {
    $example = Join-Path $BundleRoot "config.example.yaml"
    if (Test-Path $example) {
        Copy-Item $example $ConfigPath
        Write-Host "Created config.yaml from example — edit canonical_plotting_dir, then re-run."
        exit 2
    }
    throw "Missing config.yaml at $ConfigPath"
}

function Read-SimpleYaml($path) {
    $data = @{ agents = @{}; sync_nature_style = $true }
    foreach ($line in Get-Content $path) {
        $t = $line.Trim()
        if ($t -match '^canonical_plotting_dir:\s*"(.*)"\s*$') { $data.canonical_plotting_dir = $Matches[1] }
        if ($t -match '^sync_nature_style_to_plotting_dir:\s*(true|false)\s*$') {
            $data.sync_nature_style = ($Matches[1] -eq "true")
        }
        if ($t -match '^cursor:\s*(true|false)\s*$') { $data.agents.cursor = ($Matches[1] -eq "true") }
        if ($t -match '^claude:\s*(true|false)\s*$') { $data.agents.claude = ($Matches[1] -eq "true") }
        if ($t -match '^codex:\s*(true|false)\s*$') { $data.agents.codex = ($Matches[1] -eq "true") }
        if ($t -match '^agents:\s*(true|false)\s*$') { $data.agents.agents = ($Matches[1] -eq "true") }
    }
    if (-not $data.canonical_plotting_dir) { throw "config.yaml must set canonical_plotting_dir" }
    return $data
}

$cfg = Read-SimpleYaml $ConfigPath
$plotDir = $cfg.canonical_plotting_dir -replace "/", "\\"

$targets = @()
if ($cfg.agents.cursor) { $targets += @{ Name = "cursor"; Path = Join-Path $UserHome ".cursor\skills" } }
if ($cfg.agents.claude) { $targets += @{ Name = "claude"; Path = Join-Path $UserHome ".claude\skills" } }
if ($cfg.agents.codex) { $targets += @{ Name = "codex"; Path = Join-Path $UserHome ".codex\skills" } }
if ($cfg.agents.agents) { $targets += @{ Name = "agents"; Path = Join-Path $UserHome ".agents\skills" } }

if (-not (Test-Path $SkillsSrc)) { throw "Missing skills folder: $SkillsSrc" }

# Persist bundle location for the nature-portfolio install skill
$stateDir = Join-Path $UserHome ".nature-portfolio"
New-Item -ItemType Directory -Force -Path $stateDir | Out-Null
@{ bundle_root = $BundleRoot; installed_at = (Get-Date).ToString("o") } | ConvertTo-Json | Set-Content (Join-Path $stateDir "state.json") -Encoding UTF8

$skillDirs = Get-ChildItem $SkillsSrc -Directory
$installed = @()

foreach ($target in $targets) {
    New-Item -ItemType Directory -Force -Path $target.Path | Out-Null
    foreach ($skill in $skillDirs) {
        $dest = Join-Path $target.Path $skill.Name
        if ((Test-Path $dest) -and -not $Force) {
            Remove-Item $dest -Recurse -Force
        }
        robocopy $skill.FullName $dest /E /NFL /NDL /NJH /NJS /nc /ns /np | Out-Null
        if ($LASTEXITCODE -ge 8) { throw "robocopy failed for $($skill.Name) -> $dest" }
        $installed += "$($target.Name):$($skill.Name)"
    }
}

# Patch plotting path in deployed nature-plotting skills
$placeholder = "{{CANONICAL_PLOTTING_DIR}}"
$winPlot = $plotDir
$slashPlot = $cfg.canonical_plotting_dir

foreach ($target in $targets) {
    $skillMd = Join-Path $target.Path "nature-plotting\SKILL.md"
    if (Test-Path $skillMd) {
        $text = Get-Content $skillMd -Raw -Encoding UTF8
        $text = $text -replace [regex]::Escape($placeholder), $winPlot
        $text = $text -replace 'D:\\OneDrive\\UCSC\\Paper\\End-facet\\plotting', $winPlot
        $text = $text -replace 'D:/OneDrive/UCSC/Paper/End-facet/plotting', $slashPlot
        Set-Content $skillMd $text -Encoding UTF8 -NoNewline
    }
    $bundleRootFile = Join-Path $target.Path "nature-portfolio\BUNDLE_ROOT.txt"
    if (Test-Path (Join-Path $target.Path "nature-portfolio")) {
        Set-Content $bundleRootFile $BundleRoot -Encoding UTF8
    }
}

if ($cfg.sync_nature_style) {
    $srcStyle = Join-Path $SkillsSrc "nature-plotting\assets\nature_style.py"
    if (Test-Path $srcStyle) {
        New-Item -ItemType Directory -Force -Path $plotDir | Out-Null
        Copy-Item -Force $srcStyle (Join-Path $plotDir "nature_style.py")
        Write-Host "Synced nature_style.py -> $plotDir"
    }
}

Write-Host ""
Write-Host "Nature Portfolio install complete."
Write-Host "  Bundle:  $BundleRoot"
Write-Host "  Plotting: $plotDir"
Write-Host "  Targets: $($targets.Name -join ', ')"
Write-Host "  Skills:  $($skillDirs.Count) folders x $($targets.Count) agents"
Write-Host ""
Write-Host "Restart Cursor / Claude / Codex to reload skills."
