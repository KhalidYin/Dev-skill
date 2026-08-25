# Install script: link project skill directories to Claude, Codex, Agents, and Workbuddy skill roots.
# Three-tier strategy: SymbolicLink > Junction > Copy

param(
    [string]$SkillName = $null
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$TargetDirs = @(
    (Join-Path $HOME ".claude\skills"),
    (Join-Path $HOME ".codex\skills"),
    (Join-Path $HOME ".agents\skills"),
    (Join-Path $HOME ".workbuddy\skills")
)

# Discover skill directories (those with SKILL.md at project root)
$skills = Get-ChildItem -Path $ProjectRoot -Directory | Where-Object {
    $_.Name -notin @("scripts", "templates", "dist", ".git") -and
    (Test-Path (Join-Path $_.FullName "SKILL.md"))
}

if ($SkillName) {
    $skills = $skills | Where-Object { $_.Name -eq $SkillName }
}

if (-not $skills) {
    Write-Host "No skill directories found in project root."
    exit 0
}

function Install-SkillsToTarget {
    param(
        [string]$TargetDir,
        [array]$Skills
    )

    if (-not (Test-Path $TargetDir)) {
        Write-Host "Skipping $TargetDir (not found)"
        return
    }

    # Phase 1: Remove all existing skill links/copies
    Write-Host "Removing existing skills..."
    foreach ($skill in $Skills) {
        $target = Join-Path $TargetDir $skill.Name
        if (Test-Path $target) {
            # Skip if target is the source directory (prevent deleting project files)
            if ((Get-Item $target).FullName -eq $skill.FullName) {
                Write-Host "  [$($skill.Name)] Skipped (source directory)"
                continue
            }
            Remove-Item -Recurse -Force -Path $target
            Write-Host "  [$($skill.Name)] Removed"
        }
    }

    # Phase 2: Install new skill links/copies
    Write-Host "Installing new skills..."
    foreach ($skill in $Skills) {
        $source = $skill.FullName
        $target = Join-Path $TargetDir $skill.Name

        # Attempt 1: SymbolicLink (needs Developer Mode or admin)
        try {
            New-Item -ItemType SymbolicLink -Path $target -Target $source -ErrorAction Stop | Out-Null
            Write-Host "  [$($skill.Name)] Linked (SymbolicLink)"
            continue
        } catch {
            Write-Host "  [$($skill.Name)] SymbolicLink failed: $_"
        }

        # Attempt 2: Junction (NTFS feature, no admin needed)
        try {
            New-Item -ItemType Junction -Path $target -Target $source -ErrorAction Stop | Out-Null
            Write-Host "  [$($skill.Name)] Linked (Junction)"
            continue
        } catch {
            Write-Host "  [$($skill.Name)] Junction failed: $_"
        }

        # Attempt 3: Copy fallback
        try {
            Copy-Item -Recurse -Path $source -Destination $target -ErrorAction Stop
            Write-Warning "  [$($skill.Name)] Copied (fallback). Re-run this script after editing."
        } catch {
            Write-Host "  [$($skill.Name)] Copy also failed: $_" -ForegroundColor Red
        }
    }
}

foreach ($targetDir in $TargetDirs) {
    Write-Host "Linking skill(s) to $targetDir..."
    Write-Host ""
    Install-SkillsToTarget -TargetDir $targetDir -Skills $skills
    Write-Host ""
}

Write-Host "Done. Linked skills are available to Claude Code, Codex, Agents, and Workbuddy."
