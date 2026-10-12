# Scuba plugins and skills

Connect your agent to your saved context in [Scuba](https://scuba.app). Search
Captures and Collections, save useful findings, and bring your team's engineering
memory into coding and reviews.

You'll need a Scuba account. Each person signs in separately; no local server is required.

## Quick start

Choose a plugin to install the skills and MCP connection together, or install just
the skills if you already have a Scuba connection.

### Codex

```bash
codex plugin marketplace add scuba-app/scuba-plugins
codex plugin add scuba@scuba
```

You can also install from this marketplace in the Codex desktop plugin directory.

### Claude Code

```bash
claude plugin marketplace add scuba-app/scuba-plugins
claude plugin install scuba@scuba --scope project
```

Use `--scope user` to install across projects.

After installing a plugin, open a new session and sign in to Scuba when prompted.
Use `/mcp` to check the connection.

### Skills only

```bash
npx skills add scuba-app/scuba-plugins
```

Choose your agent and the skills you want. This installs skills only; reuse your
Scuba connection or follow the [MCP setup guide](skills/scuba-setup/references/mcp-setup.md).

### MCP only

Connect your client's remote HTTP MCP integration to `https://api.scuba.app/mcp/`
and sign in. See the [MCP setup guide](skills/scuba-setup/references/mcp-setup.md)
for client configuration.

## Use it

For general Scuba context, ask:

> Find the Captures about our onboarding decisions and summarize them.

For engineering memory, start in your project with:

> Use scuba-setup to configure this repository's engineering memory collection.

Then ask:

> Before we change the sync architecture, look for previous decisions and failed approaches in Scuba.

> Review this PR and use scuba-review-memory to check relevant engineering lessons.

> Save why we chose this approach to our engineering memory, with the PR link.

| Skill | What it does |
| --- | --- |
| `scuba-setup` | Connect Scuba and choose a repository's memory collection. |
| `scuba-codebase-memory` | Recall decisions and preserve useful findings. |
| `scuba-review-memory` | Add relevant engineering memory to your existing review. |

## More

- [Team setup](docs/team-setup.md)
- [Repository configuration](docs/configuration.md)
- [Maintaining and building packages](docs/maintaining.md)
- [Support](https://scuba.app/support) · [Privacy](https://scuba.app/privacy) · [Terms](https://scuba.app/terms)

[MIT license](LICENSE).
