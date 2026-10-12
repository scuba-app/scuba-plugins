# Scuba plugins and skills

Give your coding agent access to your team's engineering memory in [Scuba](https://scuba.app).
Recall why a decision was made, avoid repeating failed approaches, and preserve useful
conclusions with their sources.

Install the **Scuba plugin** to get all three skills and the hosted MCP connection:

| Skill | Use it to |
| --- | --- |
| `scuba-setup` | Connect Scuba, select a team collection, and configure a repository. |
| `scuba-codebase-memory` | Recall prior decisions and record approved decisions, findings, incidents, and PR outcomes. |
| `scuba-review-memory` | Bring relevant engineering lessons and intentional tradeoffs into your existing code review. |

No local Scuba server is required. Each person signs in with their own Scuba account.

## Quick start

### 1. Install the plugin

**Codex** — register the marketplace and install Scuba:

```bash
codex plugin marketplace add scuba-app/scuba-plugins
codex plugin add scuba@scuba
```

The marketplace also appears as a source in the desktop app's plugin directory.
If your Codex version does not offer `plugin add`, install from that directory.
Restart or open a new session after installation, then complete the Scuba sign-in
when prompted. Inspect the plugin's connection in `/mcp`; use the connection name
shown by your client when authenticating.

**Claude Code** — run from the repository where you want engineering memory:

```bash
claude plugin marketplace add scuba-app/scuba-plugins
claude plugin install scuba@scuba --scope project
```

Reload plugins or start a new session, then use `/mcp` to sign in to the plugin's
Scuba connection. Project scope records the enabled plugin in `.claude/settings.json`;
teammates still install it on their own machines. Use `--scope user` for personal
installation across projects.

Already using Scuba? Check for a working connection and existing copies of these
skills before installing. When migrating, verify the plugin first, then remove only
the superseded standalone Scuba configuration and skill copies. Plugin connections
may have different names and may require their own sign-in. Do not configure both
manual setup and the plugin by default.

### 2. Configure your team's memory

In your adopting repository, ask your agent:

> Use scuba-setup to configure engineering memory for this repository. Help me
> choose an existing shared Eng Wiki collection or create one for my team.

The setup skill checks access and writes `.scuba/config.json` in that repository:

```json
{
  "version": 1,
  "engineering_memory": {
    "collection_id": "<collection-uuid>"
  }
}
```

The skill can resolve a collection link or name to its ID. Collection creation
through MCP starts private: use Scuba's sharing controls to give teammates access.
A destination file does not grant access or authorize writes.

This file is **a Scuba skills convention**, separate from MCP and plugin configuration.
Private team repositories may commit it; public repositories should ignore the real
file and commit an example instead. It stays outside the installed plugin so
upgrades preserve your team's destination. See the [configuration contract](docs/configuration.md).

### 3. Use it

#### Install on your machine or a teammate's

If you're joining a repository that already has the [team setup](docs/team-setup.md)
committed, pull the latest code and install from that repository:

**Claude Code:** accept the project's plugin installation prompt, or run:

```bash
claude plugin install scuba@scuba --scope project
```

**Codex:** register the repository's catalog and install its Scuba entry:

```bash
codex plugin marketplace add .
codex plugin add scuba@team-tools
```

Replace `team-tools` with the `name` in your repository's
`.agents/plugins/marketplace.json`. You can also install from that source in the
Codex desktop plugin directory. If the repository has no team plugin configuration,
use [the installation steps above](#1-install-the-plugin) instead.

Each person then opens a new session, signs in to Scuba through `/mcp` if prompted,
and asks:

> Use scuba-setup to verify this repository's existing collection configuration
> and my access. Reuse the configured collection.

Teammates do not need to edit configuration or create another collection. If access
is missing, ask the collection owner to share it with their Scuba account. If you
already completed setup on this machine, go straight to the workflows below.

#### Recall and save engineering memory

> Before we change the sync architecture, use scuba-codebase-memory to look for
> previous decisions and failed approaches.

> Record why we chose this approach in our engineering wiki, with the alternatives
> and the PR link.

To supplement your existing code review:

> Review this PR using our usual workflow, and use scuba-review-memory to check
> for repeated mistakes and relevant prior decisions in Scuba.

Or add this instruction to your existing review skill:

> Use scuba-review-memory to bring relevant engineering lessons into the review
> and check candidate findings against prior decisions before finalizing.

The review skill uses scuba-codebase-memory for retrieval. It preserves your
review criteria and output format, verifies findings against current code, and
does not post comments or save memories without authorization.

Claude Code also exposes `/scuba:scuba-setup`, `/scuba:scuba-codebase-memory`, and `/scuba:scuba-review-memory`.
The skills offer to save valuable conclusions; an explicit filing request authorizes
that write. Scuba's sharing confirmations still apply.

## Set it up for your team

Commit the client-specific plugin configuration and your destination in the adopting
repository. Every teammate installs the same plugin, signs in separately, and verifies
access to the same collection. The [team setup guide](docs/team-setup.md) includes:

- Claude's shared marketplace and enabled-plugin settings.
- Codex's `.agents/plugins/marketplace.json` team catalog.
- Pinning a reviewed commit and migrating existing local skills.
- An installation and read-access acceptance check.

Add the [agent guidance snippet](skills/scuba-setup/assets/agent-guidance.md) to your
existing `AGENTS.md` or `CLAUDE.md` when you want proactive memory recall.

## Alternatives: standalone skills and MCP

For hosts without plugin support, or teams that already manage Scuba connections,
install just the portable [Agent Skills](https://agentskills.io/specification):

```bash
npx skills add scuba-app/scuba-plugins --skill scuba-setup scuba-codebase-memory scuba-review-memory
```

Choose your agent and project scope. Alternatively, copy the three `skills/` directories
with their supporting files into `.agents/skills/` for Codex or `.claude/skills/` for
Claude Code. For review-only standalone installation, install both `scuba-review-memory` and
`scuba-codebase-memory`. These methods do not install or authenticate an MCP connection.

Then reuse your existing Scuba connection or follow [manual MCP setup](skills/scuba-setup/references/mcp-setup.md#manual-connection-alternative).
Claude supports a committed project `.mcp.json`; Codex supports a trusted project's
`.codex/config.toml`. Both examples and personal setup are documented there.
Collection setup is the same for plugin and standalone installations.

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
in both plugin manifests when shipping plugin changes; installed clients can cache
by version. Git release tags are not required.
See [behavior checks](docs/behavior-checks.md) for acceptance scenarios.

## Platform packages and compatibility

`openai/`, `claude/`, and `cursor/` are complete platform packages. Their `skills/`
directories are generated copies; edit only the canonical root `skills/`, then run
`python3 scripts/sync-platform-skills.py`. Validation rejects stale copies. Build complete,
self-contained ZIPs with `python3 scripts/package.py --output /tmp/scuba-packages`.
Skills and their supporting files are included from the canonical root `skills/`.
For local Claude development, use `claude --plugin-dir .` from this repository.
Cursor packages can be submitted to its marketplace; vendor directory publication
is separate from this GitHub repository. The remote MCP registry record stays in
`registry/server.json` and the hosted endpoint remains `https://api.scuba.app/mcp/`.

All new installs use `scuba-app/scuba-plugins`. The former `scuba-skills`
repository has no existing users and can be archived after this consolidation
merges. See [installation checks](docs/installation-checks.md).

## License

[MIT](LICENSE).
