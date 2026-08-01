# DAWN jcode Executor — Capability Foundry Wave 2

## Status

`CAPABILITY_PREPARATION_READY`

This package evaluates jcode only as a bounded optional coding executor beneath DAWN. It does not install jcode, call a model, execute shell commands, modify a repository, create a branch, commit, push, merge or replace Hermes/DAWN.

## First proving slice

A later canary may inspect one allowlisted read-only repository fixture and return:

- a repository map;
- an explanation of selected code;
- a proposed patch as text;
- evidence references and limitations.

The first canary must use no provider credentials, network access, shell execution or Git writes.

## Authority boundary

DAWN remains the sole mission authority, evidence gate and source of truth. jcode must never become a parallel control plane or persist canonical memory independently.

## Offline acceptance

`acceptance.py` validates synthetic executor requests and proves that broad shell, provider, network and Git authority are refused. It does not invoke the jcode binary or inspect a real repository.

## Connection gate

A Mac-local canary requires a separate adapter with subprocess timeout, output-size limit, exact repository allowlist, environment sanitisation, process-tree cleanup and evidence capture. Any write-capable mode requires a later, separate approval.