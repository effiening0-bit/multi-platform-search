$ErrorActionPreference = 'Stop'
$target = Join-Path (Get-Location) '.env'
function Read-SecretValue([string]$name) {
  $secure = Read-Host "$name (input hidden; press Enter to skip)" -AsSecureString
  $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
  try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
  finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}
$entries = @()
foreach ($name in 'TAVILY_API_KEY','EXA_API_KEY','YOUTUBE_API_KEY') {
  $value = Read-SecretValue $name
  if ($value) { $entries += "$name=$value" }
}
if ($entries.Count -eq 0) { Write-Host 'No credentials entered; .env was not changed.' -ForegroundColor Yellow; exit 0 }
[IO.File]::WriteAllLines($target, $entries, [Text.UTF8Encoding]::new($false))
Write-Host '.env written locally. It is ignored by Git. Return to Codex and say "configured".' -ForegroundColor Green
