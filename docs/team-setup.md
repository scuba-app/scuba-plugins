# Team setup

Install the public Scuba plugin in the code repository where your team works.
The plugin supplies the skills and MCP endpoint; the repository selects the team's
collection. Sign-in and collection permissions remain individual.

## Claude Code

Merge these entries into the adopting repository's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "scuba": {
      "source": {
        "source": "github",
        "repo": "scuba-app/scuba-plugins",
        "ref": "main"
      }
    }
  },
  "enabledPlugins": {
    "scuba@scuba": true
  }
}
```

Commit the file without replacing existing settings. Claude prompts teammates to
install the configured marketplace and plugin when they trust the repository.
They can also run the commands in the [quick start](../README.md#1-install-the-plugin).
Each person signs in through `/mcp` after installation.

The marketplace follows `main`. Claude's marketplace `ref` accepts a branch or
tag, not a commit SHA; omitting it uses the repository's default branch. Commit
pinning uses `sha` on an individual plugin source inside a marketplace, which is
a different configuration object. No Git release tag is needed. See
[Claude's marketplace source reference](https://code.claude.com/docs/en/plugins/marketplace-reference#marketplace-sources)
and [plugin installation](https://code.claude.com/docs/en/discover-plugins).

## Codex

For a repository-owned catalog, merge an entry into
`.agents/plugins/marketplace.json` at the adopting repository root:

```json
{
  "name": "team-tools",
  "interface": {
    "displayName": "Team tools"
  },
  "plugins": [
    {
      "name": "scuba",
      "source": {
        "source": "url",
        "url": "https://github.com/scuba-app/scuba-plugins.git"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Preserve an existing catalog name and its other plugins. Commit the catalog. Each
teammate can select it in the desktop plugin directory, or run from the repository:

```bash
codex plugin marketplace add .
codex plugin add scuba@team-tools
```

Use your actual catalog name after `@`. If your CLI does not support `plugin add`,
install from the desktop directory. Start a new session or restart the client as
needed, then complete its Scuba authentication flow. A catalog makes the plugin
available; committing it does not sign everyone in.

To pin a reviewed revision, add `sha` to the plugin's `source` with that commit SHA.
Update that selection deliberately when upgrading; no Git release tag is needed.
Use one installation source: if you installed `scuba@scuba` personally, migrate that
installation before also installing it from a team catalog. See
[OpenAI's marketplace documentation](https://developers.openai.com/plugins/build/plugins#marketplace-metadata).

## Destination and team guidance

Run `scuba-setup` and choose an existing collection or create one, then share it in
Scuba. A private repository can commit `.scuba/config.json`; for a public repository,
keep the real configuration untracked. See the [configuration contract](configuration.md).
The plugin does not include anyone's collection ID.

Add the [agent guidance snippet](../skills/scuba-setup/assets/agent-guidance.md) to
existing repository instructions. Keep team-specific policies there as well. A
plugin upgrade should not replace team settings or those policies.

## Migrate an existing installation

1. Record the existing collection ID and any team-specific instructions.
2. Install the plugin and confirm both skills and its Scuba MCP tools are available.
3. Select the existing collection through `scuba-setup`; do not create a replacement.
4. Move repository-specific policy into repository guidance. Replace links to removed
   local skills with the installed skill's name and a link to your setup guide.
5. Remove only superseded standalone skill copies and Scuba MCP entries once the
   plugin works. Preserve other servers and integrations. Existing OAuth sessions
   may not carry over to a plugin connection; use the client's authentication flow.

## Acceptance check

First test marketplace registration and installation with an empty client plugin
cache. A new session with an already registered marketplace can hide a broken
source configuration. Then use a fresh session in the adopting repository:

1. Verify the installed Scuba version, both skills, and the MCP server inventory.
2. Complete sign-in and use `get_me`, when available, to verify the account.
3. Run setup against the existing destination, retrieve that collection by ID, and
   perform a small search. An empty search is valid; authentication failures are not.
4. Have a second teammate repeat the read check using their own account. One account's
   success cannot establish team-wide access.
5. Verify that an upgrade leaves `.scuba/config.json` unchanged.

Read checks do not require creating notes. Run a write/read/undo smoke test only
when requested, following the skill's audience-confirmation and cleanup instructions.
Report installation, authentication, reads, writes, and second-account access
separately so an installation-only check is not mistaken for a complete rollout.
