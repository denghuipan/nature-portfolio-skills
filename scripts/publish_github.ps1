#Requires -Version 5.1
<#
Creates a private GitHub repo and pushes the current branch.
Prerequisite: gh auth login (once per machine)

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/publish_github.ps1
  powershell -ExecutionPolicy Bypass -File scripts/publish_github.ps1 -RepoName nature-portfolio-skills -Visibility private
#>
param(
    [string]$RepoName = "nature-portfolio-skills",
    [ValidateSet("private", "public")]
    [string]$Visibility = "private"
)

$ErrorActionPreference = "Stop"
$BundleRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $BundleRoot

$gh = Get-Command gh -ErrorAction SilentlyContinue
if (-not $gh) { throw "GitHub CLI (gh) not found. Install: winget install GitHub.cli" }

gh auth status | Out-Null

if (git rev-parse --verify main 2>$null) {
    git branch -M main
} else {
    git branch -M main 2>$null
}

if (git remote get-url origin 2>$null) {
    Write-Host "Remote origin already set; pushing..."
    git push -u origin main
    gh repo view --web
    exit 0
}

gh repo create $RepoName --$Visibility --source=. --remote=origin --push --description "Nature Portfolio agent skills (writing, figures, plotting) with cross-agent installer"
Write-Host "Done. Repository:"
gh repo view --json url -q .url
