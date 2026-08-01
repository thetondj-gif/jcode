#!/usr/bin/env python3
"""Secret-free offline acceptance for the DAWN jcode executor boundary.

The validator does not invoke jcode, a model, Git or a shell. It proves only
that a proposed first executor canary is read-only, allowlisted and bounded.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SAFE_OPERATIONS = {
    "inspect_repository",
    "explain_code",
    "propose_patch_text"
}


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != 1:
        errors.append("schema_version")
    if payload.get("authorised") is not True:
        errors.append("operator_authority_required")
    if payload.get("control_plane") != "DAWN":
        errors.append("dawn_control_plane_required")
    repository_path = payload.get("repository_path")
    if not isinstance(repository_path, str) or not repository_path.startswith("/"):
        errors.append("absolute_repository_path_required")
    if payload.get("repository_allowlisted") is not True:
        errors.append("repository_allowlist_required")
    if payload.get("read_only") is not True:
        errors.append("read_only_required")
    if payload.get("network_execution") is not False:
        errors.append("network_execution_prohibited")
    if payload.get("provider_credentials") is not False:
        errors.append("provider_credentials_prohibited")
    if payload.get("shell_execution") is not False:
        errors.append("shell_execution_prohibited")
    if payload.get("git_write") is not False:
        errors.append("git_write_prohibited")
    if payload.get("external_actions") is not False:
        errors.append("external_actions_prohibited")
    operations = payload.get("operations")
    if not isinstance(operations, list) or not operations:
        errors.append("operations_required")
    elif not set(operations).issubset(SAFE_OPERATIONS):
        errors.append("operation_allowlist")
    max_seconds = payload.get("max_seconds")
    if not isinstance(max_seconds, int) or not 1 <= max_seconds <= 60:
        errors.append("timeout_limit")
    max_output = payload.get("max_output_chars")
    if not isinstance(max_output, int) or not 1000 <= max_output <= 50000:
        errors.append("output_limit")
    if payload.get("persist_session") is not False:
        errors.append("session_persistence_prohibited")
    if payload.get("write_memory") is not False:
        errors.append("memory_write_prohibited")
    return errors


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    errors = validate(payload)
    return {
        "schema_version": 1,
        "capability": "dawn-jcode-executor",
        "operation": "validate-read-only-executor-canary",
        "status": "blocked" if errors else "success",
        "data": {
            "canary_eligible": not errors,
            "jcode_invoked": False,
            "model_called": False,
            "shell_executed": False,
            "repository_modified": False,
            "git_action_performed": False
        },
        "warnings": errors,
        "network_used": False,
        "credentials_used": False,
        "external_actions_performed": False
    }


def main() -> int:
    valid = json.loads((ROOT / "fixtures" / "valid-executor.json").read_text())
    invalid = json.loads((ROOT / "fixtures" / "invalid-executor.json").read_text())
    accepted = evaluate(valid)
    refused = evaluate(invalid)
    assertions = [
        accepted["status"] == "success",
        accepted["data"]["jcode_invoked"] is False,
        accepted["data"]["model_called"] is False,
        accepted["data"]["repository_modified"] is False,
        accepted["external_actions_performed"] is False,
        refused["status"] == "blocked",
        "dawn_control_plane_required" in refused["warnings"],
        "repository_allowlist_required" in refused["warnings"],
        "read_only_required" in refused["warnings"],
        "network_execution_prohibited" in refused["warnings"],
        "provider_credentials_prohibited" in refused["warnings"],
        "shell_execution_prohibited" in refused["warnings"],
        "git_write_prohibited" in refused["warnings"],
        "operation_allowlist" in refused["warnings"]
    ]
    report = {
        "capability": "dawn-jcode-executor",
        "status": "passed" if all(assertions) else "failed",
        "tests": len(assertions),
        "passed": sum(assertions),
        "network_used": False,
        "credentials_required": False,
        "jcode_invoked": False,
        "external_actions_performed": False
    }
    print(json.dumps(report, indent=2))
    return 0 if all(assertions) else 1


if __name__ == "__main__":
    sys.exit(main())
