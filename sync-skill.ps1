<# Deploy this repo's skill/ (the canonical copy) to Claude, Codex and the Context Repo; read-only unless -Apply. #>
[CmdletBinding()]
param([string]$ContextRoot, [string[]]$Target, [string]$TemplateRoot, [switch]$Apply, [switch]$Adopt)
$ErrorActionPreference = 'Stop'
$arguments = @('-X', 'utf8', '-B', (Join-Path $PSScriptRoot 'scripts/sync_skill.py'))
if ($ContextRoot) { $arguments += @('--context-root', $ContextRoot) }
foreach ($item in $Target) { $arguments += @('--target', $item) }
if ($TemplateRoot) { $arguments += @('--template-root', $TemplateRoot) }
if ($Apply) { $arguments += '--apply' }
if ($Adopt) { $arguments += '--adopt' }
if (Get-Command py -ErrorAction SilentlyContinue) { & py @arguments }
elseif (Get-Command python -ErrorAction SilentlyContinue) { & python @arguments }
else { throw 'Python 3.10+ required' }
if ($LASTEXITCODE -ne 0) { throw "Skill sync failed (exit $LASTEXITCODE); inspect reported conflicts." }
