param(
    [ValidateSet("all", "beamer", "clean")]
    [string]$Target = "beamer"
)
$ErrorActionPreference = "Stop"
$ProjectDir = (Get-Item $PSScriptRoot).Parent.FullName
$BuildDir = [IO.Path]::GetFullPath((Join-Path $ProjectDir "scripts/.build/beamer"))
$OutputDir = Join-Path $ProjectDir "output"
$Destination = Join-Path $OutputDir "beamer.pdf"

if ($Target -eq "clean") {
    if (-not $BuildDir.StartsWith($ProjectDir + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Build directory is outside the project."
    }
    if (Test-Path -LiteralPath $BuildDir) { Remove-Item -LiteralPath $BuildDir -Recurse -Force }
    if (Test-Path -LiteralPath $Destination) { Remove-Item -LiteralPath $Destination -Force }
    Write-Host "Beamer build artifacts removed."
    exit 0
}
if (-not (Get-Command latexmk -ErrorAction SilentlyContinue)) {
    throw "Install TeX Live, MacTeX or MiKTeX with latexmk and XeLaTeX."
}
New-Item -ItemType Directory -Force -Path $BuildDir | Out-Null
$PreviousTexInputs = $env:TEXINPUTS
$StylePath = (Join-Path $ProjectDir "style") -replace '\\', '/'
$env:TEXINPUTS = "${StylePath}//;${PreviousTexInputs}"
Push-Location (Join-Path $ProjectDir "src/beamer")
try {
    & latexmk -xelatex -silent -interaction=nonstopmode -halt-on-error -synctex=1 "-outdir=$($BuildDir -replace '\\', '/')" main.tex
    if ($LASTEXITCODE -ne 0) { throw "Beamer compilation failed; output PDF was not replaced." }
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
    Copy-Item -LiteralPath (Join-Path $BuildDir "main.pdf") -Destination $Destination -Force
    Write-Host "Created: $Destination"
}
finally {
    Pop-Location
    $env:TEXINPUTS = $PreviousTexInputs
}
