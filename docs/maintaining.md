# Maintaining Scuba plugins

## Package and maintain

This repository is the canonical source for Scuba skills, platform plugin packages, and MCP metadata:

- `plugin.json`, `mcp.json`, and `skills/`: portable plugin package.
- `.agents/plugins/marketplace.json`: Codex catalog.
- `.claude-plugin/plugin.json` and `.mcp.json`: Claude-compatible package metadata and MCP configuration.
- `.claude-plugin/marketplace.json`: Claude catalog.
- `.cursor-plugin/plugin.json`: Cursor metadata for the root plugin.

The catalogs distribute the same skills and endpoint. They are GitHub-hosted
catalogs, not listings in the vendors' official directories. Official directory
submission is separate. This follows [OpenAI's plugin packaging guide](https://developers.openai.com/plugins/build/plugins)
and [Claude's marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces).

Validate the package, skills, references, and destination schema:

```bash
uv run scripts/validate.py
claude plugin validate . --strict
claude plugin validate .claude-plugin/plugin.json --strict
```

Python is used only for validation, not by the installed workflows. Bump the version
in all plugin manifests when shipping plugin changes; installed clients can cache
by version. Git release tags are not required.
See [behavior checks](behavior-checks.md) for acceptance scenarios.

## Platform packages and compatibility

`openai/`, `claude/`, and `cursor/` are complete platform packages. Their `skills/`
directories are generated copies; edit only the canonical root `skills/`, then run
`python3 scripts/sync-platform-skills.py`. Validation rejects stale copies. Build complete,
self-contained ZIPs with `python3 scripts/package.py --output /tmp/scuba-packages`.
Skills and their supporting files are included from the canonical root `skills/`.
The Claude package remains at `claude/`, so marketplace applications pointing to
that directory keep the same source path. Replace previously uploaded ZIPs to
include the bundled skills.
For local Claude development, use `claude --plugin-dir .` from this repository.
Cursor packages can be submitted to its marketplace; vendor directory publication
is separate from this GitHub repository. The remote MCP registry record stays in
`registry/server.json` and the hosted endpoint remains `https://api.scuba.app/mcp/`.

All new installs use `scuba-app/scuba-plugins`. The former `scuba-skills`
repository is archived; its original commit history remains available. See [installation checks](installation-checks.md).

