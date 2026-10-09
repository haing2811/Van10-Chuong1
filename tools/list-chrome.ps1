Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | ForEach-Object {
  $cmd = $_.CommandLine
  $prof = ''
  if ($cmd -match '--user-data-dir=([^ "]+)') { $prof = $Matches[1] }
  $port = ''
  if ($cmd -match '--remote-debugging-port=(\d+)') { $port = $Matches[1] }
  Write-Output ("PID={0} PROF={1} PORT={2}" -f $_.ProcessId, $prof, $port)
}
