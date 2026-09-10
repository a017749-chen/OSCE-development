<#
  sync-skill.ps1 — 把正本 skill 推送到各部署位置

  正本：D:\osce-item-development\skill\   （本 repo）
  部署：1) C:\Users\User\.claude\skills\osce-item-development\        實際生效
        2) C:\Users\User\YiChan-Context-Repo\.agents\skills\osce-item-development\   註冊表

  用法：
    .\sync-skill.ps1            檢查差異（不寫入）
    .\sync-skill.ps1 -Apply     實際同步
#>
[CmdletBinding()]
param([switch]$Apply)

$ErrorActionPreference = 'Stop'
$src = Join-Path $PSScriptRoot 'skill'
$targets = @(
  'C:\Users\User\.claude\skills\osce-item-development',
  'C:\Users\User\YiChan-Context-Repo\.agents\skills\osce-item-development'
)

if (-not (Test-Path $src)) { throw "找不到正本目錄：$src" }

# 正本內的相對檔案清單
$files = Get-ChildItem $src -Recurse -File | ForEach-Object {
  $_.FullName.Substring($src.Length).TrimStart('\')
}

$dirty = $false
foreach ($t in $targets) {
  Write-Host ""
  Write-Host "→ $t" -ForegroundColor Cyan
  if (-not (Test-Path $t)) {
    Write-Host "   目標不存在" -ForegroundColor Yellow
    if ($Apply) { New-Item -ItemType Directory -Path $t -Force | Out-Null }
  }
  foreach ($rel in $files) {
    $s = Join-Path $src $rel
    $d = Join-Path $t $rel
    $same = $false
    if (Test-Path $d) {
      $same = (Get-FileHash $s).Hash -eq (Get-FileHash $d).Hash
    }
    if ($same) {
      Write-Host "   = $rel"
    } else {
      $dirty = $true
      Write-Host "   $(if (Test-Path $d) { '≠' } else { '+' }) $rel" -ForegroundColor Yellow
      if ($Apply) {
        $dir = Split-Path $d -Parent
        if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
        Copy-Item $s $d -Force
      }
    }
  }
  # 目標端多出來的檔案只提示，不自動刪除
  if (Test-Path $t) {
    Get-ChildItem $t -Recurse -File | ForEach-Object {
      $rel = $_.FullName.Substring($t.Length).TrimStart('\')
      if ($files -notcontains $rel) {
        Write-Host "   ! 目標多出（未處理）：$rel" -ForegroundColor DarkYellow
      }
    }
  }
}

Write-Host ""
if ($Apply) {
  Write-Host "同步完成。Context Repo 的變更請記得 commit。" -ForegroundColor Green
} elseif ($dirty) {
  Write-Host "有差異未同步 —— 執行 .\sync-skill.ps1 -Apply 套用。" -ForegroundColor Yellow
} else {
  Write-Host "全部一致，無需同步。" -ForegroundColor Green
}
