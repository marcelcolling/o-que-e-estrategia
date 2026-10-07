# Publica o portal no GitHub e ativa o GitHub Pages.
# Uso (PowerShell, na pasta do repositório):  .\publicar.ps1
# Pré-requisito: ter feito login uma vez com:  gh auth login
param([string]$Nome = "o-que-e-estrategia")

$ErrorActionPreference = "Stop"
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
Set-Location $PSScriptRoot

gh auth status | Out-Null
$usuario = gh api user --jq .login

if (-not (git remote 2>$null | Select-String -Quiet "origin")) {
    gh repo create $Nome --public --source . --remote origin --description "Portal da disciplina Entendendo Porter: O que é estratégia?"
}
# via cmd: no PowerShell 5.1, o progresso que o git escreve no stderr viraria erro e pararia o script
cmd /c "git push -u origin main 2>&1"
if ($LASTEXITCODE -ne 0) { throw "git push falhou" }

# Ativa o GitHub Pages (branch main, pasta raiz). Se já estiver ativo, apenas segue.
try {
    gh api -X POST "repos/$usuario/$Nome/pages" -f "source[branch]=main" -f "source[path]=/" | Out-Null
} catch { }
Write-Host ""
Write-Host "Pronto. Em 1-2 minutos o site estará em: https://$usuario.github.io/$Nome/"
