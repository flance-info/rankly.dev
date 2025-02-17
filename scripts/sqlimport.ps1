# Full path to the compressed SQL file
$SQL_FILE = "D:\domains\rankly\scripts\laravel_db_20250214.sql.gz"

Write-Host "Starting database import process..."
Write-Host "Input file: $SQL_FILE"
Write-Host "----------------------------------------"

# ==============================
# Step 1: Validate Prerequisites
# ==============================
Write-Host "Step 1: Validating prerequisites..."

if (-Not (Test-Path $SQL_FILE)) {
    Write-Host "❌ Error: File '$SQL_FILE' not found." -ForegroundColor Red
    exit 1
}

try {
    docker ps | Out-Null
}
catch {
    Write-Host "❌ Error: Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

$containerStatus = docker ps --format "{{.Names}}" | Select-String -Pattern "^laravel-db$"
if ($containerStatus -eq $null) {
    Write-Host "❌ Error: The 'laravel-db' container is not running." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Prerequisites validated."
Write-Host "----------------------------------------"

# ====================================================
# Step 2: Start Docker Process & Establish DB Connection
# ====================================================
Write-Host "Step 2: Starting Docker process and establishing database connection..."

# The Docker command runs a shell that decompresses the SQL file (via gunzip)
# and pipes it to psql to restore the database.
$dockerCmd   = "docker"
$dockerArgs  = 'exec -i laravel-db sh -c "gunzip -c | psql -U laravel -d rankly-db1"'

# Configure the process start info
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $dockerCmd
$psi.Arguments = $dockerArgs
$psi.RedirectStandardInput = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $psi

try {
    if (-not $process.Start()) {
        Write-Host "❌ Error: Failed to start the Docker process." -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Docker process started and database connection established."
    Write-Host "----------------------------------------"

    # ============================================================
    # Step 3: Stream File Data to Container (Trigger Unzipping & Import)
    # ============================================================
    Write-Host "Step 3: Streaming file data to container (this will trigger unzipping and DB import)..."

    # Open the compressed file for reading
    $fileStream = [System.IO.File]::OpenRead($SQL_FILE)
    $BufferSize = 8192  # 8 KB buffer
    $buffer = New-Object byte[] $BufferSize
    $FileSize = (Get-Item $SQL_FILE).Length
    $BytesRead = 0

    # Get the binary stream for Docker process STDIN
    $stdIn = $process.StandardInput.BaseStream

    while (($chunkSize = $fileStream.Read($buffer, 0, $buffer.Length)) -gt 0) {
        # Write the chunk to the Docker process’s STDIN
        $stdIn.Write($buffer, 0, $chunkSize)
        $stdIn.Flush()

        # Update the count of bytes streamed
        $BytesRead += $chunkSize
        $percentComplete = [math]::Round(($BytesRead / $FileSize) * 100, 2)
        $streamedMB = [math]::Round($BytesRead / 1MB, 2)
        $totalMB    = [math]::Round($FileSize / 1MB, 2)

        Write-Progress -Activity "Importing Database..." `
                       -Status "Streaming: $streamedMB MB of $totalMB MB ($percentComplete% complete)" `
                       -PercentComplete $percentComplete
    }

    # Signal end-of-file to the Docker process
    $stdIn.Close()
    $fileStream.Close()
    Write-Host "✅ File streaming completed. Unzipping and database import have been triggered."
    Write-Host "----------------------------------------"

    # ============================================================
    # Step 4: Wait for the Database Import Process to Complete
    # ============================================================
    Write-Host "Step 4: Waiting for the database import process to finish..."
    $process.WaitForExit()

    if ($process.ExitCode -eq 0) {
        Write-Host "----------------------------------------"
        Write-Host "✅ Database import completed successfully!" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Error: Database import failed!" -ForegroundColor Red
        Write-Host "Error Output:" -ForegroundColor Red
        Write-Host $process.StandardError.ReadToEnd()
        exit 1
    }
}
catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    exit 1
}
finally {
    if ($fileStream) { $fileStream.Dispose() }
    if ($process) { $process.Dispose() }
}
