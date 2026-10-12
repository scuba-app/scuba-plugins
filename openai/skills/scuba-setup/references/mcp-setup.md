# Connect to Scuba MCP

Scuba's hosted endpoint is `https://api.scuba.app/mcp/`. Use the client's native
remote HTTP transport and OAuth support. A skill installation alone does not create
an authenticated connection. Reuse a working Scuba connector before adding a duplicate.

## Plugin installation

Prefer the Scuba plugin for Codex and Claude Code. It bundles the skills and the
MCP connection. Register `scuba-app/scuba-plugins` as a plugin marketplace, then
install `scuba@scuba` using the client's native plugin installer. For an existing
team catalog, use that catalog's name instead. Follow the
[public installation guide](https://github.com/scuba-app/scuba-plugins#quick-start)
for client commands and shared team configuration.

If the plugin is already installed, inspect its enabled state and its MCP connection
before adding a standalone server. Reload or start a new session if needed, then
complete the client's OAuth flow. Plugin server names may be namespaced; use the
actual name shown by the client rather than assuming it is exactly `scuba`.

## Manual connection alternative

Use the following for standalone skills or an existing manually managed connection.
For team configuration, commit a root `.mcp.json` for Claude Code or
`.codex/config.toml` for Codex in the adopting repository. Merge with existing
configuration. Each teammate still installs the skills, trusts or approves the
project as required, and signs in individually. Never commit credentials.

The connection definition and `.scuba/config.json` have separate purposes: the latter
selects the memory collection and does not grant access to it.

## Codex

For user-level configuration:

```bash
codex mcp add scuba --url https://api.scuba.app/mcp/
codex mcp login scuba
```

For a trusted repository's shared connection definition, merge this into its
`.codex/config.toml` instead of adding a second user-level entry:

```toml
[mcp_servers.scuba]
url = "https://api.scuba.app/mcp/"
```

Commit `.codex/config.toml`. Each teammate must trust the project for Codex to load
its configuration, then run `codex mcp login scuba` from that repository. Each person
completes OAuth separately. Use `codex mcp list` or `/mcp` to inspect the connection.
If the current session does not expose the newly connected tools, follow the
client's reload or restart instructions before verifying access.

Each skill includes `agents/openai.yaml` declaring Scuba as an MCP dependency,
following Codex's supported metadata. Other hosts may ignore that file. It declares
a connection requirement, not credentials, collection configuration, or permission
to share anything. See [Codex MCP](https://developers.openai.com/codex/mcp) and
[skill metadata](https://developers.openai.com/codex/skills).

## Claude Code

For a connection available to the user across projects:

```bash
claude mcp add --transport http --scope user scuba https://api.scuba.app/mcp/
```

Open Claude Code, run `/mcp`, and complete the browser sign-in for Scuba.

For a connection definition shared by a repository, use `--scope project` instead:

```bash
claude mcp add --transport http --scope project scuba https://api.scuba.app/mcp/
```

This stores the server definition in the repository's `.mcp.json`. The equivalent
entry, merged alongside existing servers, is:

```json
{
  "mcpServers": {
    "scuba": {
      "type": "http",
      "url": "https://api.scuba.app/mcp/"
    }
  }
}
```

Commit `.mcp.json`. Teammates approve project MCP configuration as their client
requires, then use `/mcp` to sign in individually. See
[Claude Code project scope](https://code.claude.com/docs/en/mcp#project-scope).

## Other clients

Add the same endpoint using the client's remote MCP or connector setup, then follow
its OAuth prompts. Settings locations and supported skill metadata vary by client;
neither `.mcp.json` nor Codex's TOML is a universal MCP configuration format.
See the [MCP remote-server guide](https://modelcontextprotocol.io/docs/develop/connect-remote-servers).

## Verification and recovery

Discover the connected toolset, use `get_me` when available, and read the selected
collection. A 401 from an unauthenticated HTTP probe is expected; it is not proof
that OAuth sign-in or authenticated tool calls work. Let the client handle
authorization discovery and tokens according to the
[MCP authorization specification](https://modelcontextprotocol.io/specification/latest/basic/authorization).

If one connection fails, check other enabled repo, connector, or plugin connections
for the required Scuba tools before concluding access is unavailable. Namespace
prefixes can differ, including legacy Flashback names. If tools are connected but a
collection is inaccessible, check the signed-in account and ask its owner to grant
access. Do not silently choose a different collection.

Keep tokens out of repository files, command examples, and the skill's destination
configuration. Do not implement a second OAuth flow or collect tokens manually.
