# DAWN jcode rollback boundary

## Current repository-only state

The branch adds contracts, fixtures and an offline validator only. It creates no process, service, port, credential, session, repository checkout or memory store.

Rollback is to close the draft PR and delete the branch.

## Future Mac canary rollback

A later executor canary must:

1. stop the bounded foreground subprocess;
2. kill and verify removal of its complete process tree;
3. remove only the isolated canary home and evidence directory;
4. confirm the allowlisted repository has no file, index or Git changes;
5. confirm no network connection, provider call or credential read occurred;
6. confirm Hindsight, Qdrant, Obsidian and DAWN mission counts are unchanged;
7. preserve command, exit-code and resource evidence.

No automatic recovery may expand authority, switch to a cloud provider or retry with write access.