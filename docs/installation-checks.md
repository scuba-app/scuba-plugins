# Installation checks

Run these from the canonical repository before release. Use a scratch project
for installs so you do not replace your own skill configuration.

```bash
python3 scripts/sync-platform-skills.py --check
uv run scripts/validate.py
python3 scripts/package.py --output /tmp/scuba-packages
npx skills add . --list
npx skills add . --skill scuba-setup scuba-codebase-memory scuba-review-memory --agent codex claude-code cursor --copy --yes
claude plugin validate . --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

After merging, verify the public GitHub source:

```bash
npx skills add scuba-app/scuba-plugins --list
npx skills add https://github.com/scuba-app/scuba-plugins/tree/main/skills/scuba-setup --list
claude plugin marketplace add scuba-app/scuba-plugins
claude plugin install scuba@scuba --scope project
codex plugin marketplace add scuba-app/scuba-plugins
codex plugin add scuba@scuba
```

For standalone skills, test project and global installation (`--global`), selected
agents (`--agent`), and copies (`--copy`). Plain Git clone plus copying each skill
folder and its supporting files remains supported. Skill installation alone does
not configure MCP; follow the setup skill's manual MCP guide.

For each platform ZIP, extract into a clean directory and verify all three skills,
references and assets are inside the package. Claude supports a local development
load with `claude --plugin-dir <extracted-directory>`. Vendor marketplace approval
and account sign-in require separate host acceptance checks.

MCP-only clients continue using `https://api.scuba.app/mcp/` with their own account
sign-in. The endpoint and registry identity are unchanged by this repository move.
Use the manual MCP guide for Claude and Codex; Cursor can use the bundled
`mcp.json` server entry in project `.cursor/mcp.json` or its global configuration.
Never overwrite unrelated servers. For other remote HTTP MCP clients, supply the
same URL using that client's supported OAuth connection flow.
