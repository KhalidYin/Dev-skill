# Commented SAP docx

Produce this only after the user explicitly confirms they want it. Agreeing that the review should run is not confirmation. Offer it in one line after the Excel log is delivered.

## Preconditions

- The SAP was supplied as `.docx`. For a PDF, say that comments can only be added to a Word file, and offer the Excel log as the deliverable.
- `build_issue_log.py check --run-dir RUN` passes.

## Ask before running

Settle two choices with the user, using defaults when they do not answer:

1. Minimum severity to comment. Default: all ranked findings (`Editorial`).
2. Comment author label. Default: `SAP Review (AI-assisted)`.

## Run

```bash
python scripts/annotate_docx.py --run-dir RUN --sap SAP.docx \
  --out SAP_reviewed.docx --confirmed [--min-severity Major]
```

The script:

- anchors each comment to a unique paragraph containing `sap_excerpt`, using the numbered section in `sap_locator` to narrow the search when available. It can fall back to a uniquely matched section heading when the excerpt is absent. Ambiguous matches are reported as unanchored;
- includes ranked findings at or above `--min-severity`. Out-of-scope observations (`n/a`) are excluded unless `--min-severity n/a` is passed;
- collects findings it cannot anchor into one comment on the first paragraph, and reports them;
- writes a new file and never modifies the original.

## Report

Tell the user how many comments were anchored and list the IDs of any unanchored findings. Comments do not replace the Excel log, which remains the tracking record. Track-changes edits are out of scope because this skill does not rewrite the SAP.
