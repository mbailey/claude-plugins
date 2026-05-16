#!/usr/bin/env python3
"""Minimal sanity check for .claude-plugin/marketplace.json.

Adapted from trailofbits/skills .github/scripts/validate_plugin_metadata.py.
ToB's validator cross-checks plugins/<name>/.claude-plugin/plugin.json against a
root manifest. mbailey/skills currently ships *external* plugins via url-source
entries (source.source == "url"), so there are no in-repo plugin.json files to
cross-check. This script instead validates the marketplace manifest itself:
valid JSON, required top-level fields, and a well-formed plugins list with
unique names and resolvable sources.

stdlib only; no third-party deps. Exit 0 on success, 1 on any error.
"""

import json
import sys
from pathlib import Path

MANIFEST = Path(".claude-plugin/marketplace.json")


def main() -> int:
    if not MANIFEST.is_file():
        print(f"ERROR: {MANIFEST} not found", file=sys.stderr)
        return 1

    try:
        data = json.loads(MANIFEST.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: {MANIFEST} is not valid JSON: {e}", file=sys.stderr)
        return 1

    errors: list[str] = []

    def require_str(obj: object, key: str, where: str) -> None:
        if not isinstance(obj, dict) or key not in obj:
            errors.append(f"{where}: missing '{key}'")
        elif not isinstance(obj[key], str) or not obj[key].strip():
            errors.append(f"{where}: '{key}' must be a non-empty string")

    if not isinstance(data, dict):
        print("ERROR: top-level value must be a JSON object", file=sys.stderr)
        return 1

    require_str(data, "name", "marketplace")

    owner = data.get("owner")
    if not isinstance(owner, dict):
        errors.append("marketplace: 'owner' must be an object")
    else:
        require_str(owner, "name", "owner")
        require_str(owner, "email", "owner")

    plugins = data.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append("marketplace: 'plugins' must be a non-empty list")
        plugins = []

    seen: set[str] = set()
    for i, plugin in enumerate(plugins):
        where = f"plugins[{i}]"
        if not isinstance(plugin, dict):
            errors.append(f"{where}: must be an object")
            continue
        require_str(plugin, "name", where)
        require_str(plugin, "description", where)

        name = plugin.get("name")
        if isinstance(name, str):
            if name in seen:
                errors.append(f"{where}: duplicate plugin name '{name}'")
            seen.add(name)

        source = plugin.get("source")
        if not isinstance(source, dict):
            errors.append(f"{where}: 'source' must be an object")
            continue
        kind = source.get("source")
        if kind == "url":
            url = source.get("url")
            if not isinstance(url, str) or not url.startswith(("http://", "https://")):
                errors.append(f"{where}: url-source must have an http(s) 'url'")
        elif kind in (None, ""):
            errors.append(f"{where}: 'source.source' is required")
        # Non-url source kinds (e.g. local/github) are accepted as-is: this is a
        # sanity check, not a full schema validator.

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"marketplace.json OK: {len(plugins)} plugin(s), all entries well-formed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
