# Install script: link project skill directories to ~/.claude/skills/ and ~/.codex/skills/
# Three-tier strategy: SymbolicLink > Junction > Copy

param(
    [string]$SkillName = $null
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$TargetDirs = @(
    (Join-Path $HOME ".claude\skills"),
    (Join-Path $HOME ".codex\skills")
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
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
        Write-Host "Created $TargetDir"
    }

    foreach ($skill in $Skills) {
        $source = $skill.FullName
        $target = Join-Path $TargetDir $skill.Name

        if (Test-Path $target) {
            $item = Get-Item $target
            if ($item.LinkType -eq "SymbolicLink" -and (Get-Item $item.Target).FullName -eq $source) {
                Write-Host "  [$($skill.Name)] Already linked (SymbolicLink) - skipping"
                continue
            }
            if ($item.LinkType -eq "Junction" -and (Get-Item $item.Target).FullName -eq $source) {
                Write-Host "  [$($skill.Name)] Already linked (Junction) - skipping"
                continue
            }

            Write-Warning "  [$($skill.Name)] Target exists at $target but is not a link to this project."
            Write-Warning "  Remove it manually first if you want to replace it, or run:"
            Write-Warning "    Remove-Item -Recurse -Force '$target'"
            continue
        }

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
            Write-Error "  [$($skill.Name)] Copy also failed: $_"
        }
    }
}

foreach ($targetDir in $TargetDirs) {
    Write-Host "Linking skill(s) to $targetDir..."
    Write-Host ""
    Install-SkillsToTarget -TargetDir $targetDir -Skills $skills
    Write-Host ""
}

Write-Host "Done. Linked skills are available to Claude Code and Codex."
Write-Host "Verify with: Get-ChildItem '$($TargetDirs[0])'"
