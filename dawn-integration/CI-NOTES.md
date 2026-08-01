# Inherited fork CI constraints

The focused `DAWN integration acceptance` workflow passes without credentials and validates the executor-only boundary.

Two broader repository checks remain red for reasons unrelated to the DAWN boundary files:

## Linked-issue policy

The inherited `Require Linked Issue` workflow requires every pull request to reference an existing issue. GitHub Issues are disabled in this fork, so no qualifying issue can be created or linked.

Resolution options for a later repository-governance decision:

1. enable Issues and create a real integration issue; or
2. amend the inherited workflow so it skips only when the repository has Issues disabled.

The check must not be bypassed with a fabricated issue number.

## Private deploy key

The inherited full CI workflow unconditionally starts `webfactory/ssh-agent` with `secrets.DEPLOY_KEY`. The fork does not contain that private secret, so Ubuntu, macOS, Windows, quality and cross-target jobs stop before compiling.

No deploy key was created, copied or exposed by this preparation. Before changing the workflow, verify whether any current dependency genuinely requires private SSH access. If all dependencies are public, a separately reviewed fork-CI patch may make the SSH setup conditional and retain HTTPS checkout as the default.

## Current verdict

`DAWN_BOUNDARY_PASS_FULL_FORK_CI_BLOCKED_BY_REPOSITORY_CONFIGURATION`

This is not installation or execution approval.