# Checkpoint Format

The checkpoint artefact tracks integration progress so `resume` mode can continue safely.

## File Path

- `docs/integration-runs/<YYYY-MM-DD>-<batch>-checkpoints.json`

## Requirements

1. Write one checkpoint record per mutating step.
2. Include command provenance for each step.
3. Update `status` after each validation gate.
4. Preserve append-only history for auditability.

## Record Shape

Each checkpoint entry follows `checkpoint.schema.json`.

Key fields:

- `step_id`: stable identifier for the integration step.
- `timestamp`: ISO-8601 UTC timestamp.
- `mode`: `audit`, `execute`, `resume`, or `rollback`.
- `pr_number`: pull request number for PR-specific steps.
- `command`: mutating command executed.
- `status`: `pending`, `running`, `passed`, `failed`, or `rolled_back`.
- `validation`: list of validation commands and results.
- `notes`: optional context.
