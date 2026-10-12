# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = ["pyyaml>=6,<7", "jsonschema>=4,<5"]
# ///
"""Validate the plugin package, skills, and Scuba configuration contract."""

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable, str(root / "scripts/sync-platform-skills.py"), "--check"], check=True)
    validate_plugin(root)
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        raise ValueError("No skills found")

    for skill in skills:
        match = re.match(r"\A---\n(.*?)\n---\n", skill.read_text(), re.DOTALL)
        if match is None:
            raise ValueError(f"Missing frontmatter: {skill}")
        metadata = yaml.safe_load(match.group(1))
        name = metadata["name"]
        if name != skill.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Invalid skill name: {name}")
        if len(name) > 64 or not 1 <= len(metadata["description"]) <= 1024:
            raise ValueError(f"Invalid metadata length: {skill}")

        interface = yaml.safe_load((skill.parent / "agents/openai.yaml").read_text())
        dependency = interface["dependencies"]["tools"][0]
        if dependency != {
            "type": "mcp",
            "value": "scuba",
            "description": "Scuba capture library and shared collections",
            "transport": "streamable_http",
            "url": "https://api.scuba.app/mcp/",
        }:
            raise ValueError(f"Unexpected MCP dependency: {skill}")
        if f"${name}" not in interface["interface"]["default_prompt"]:
            raise ValueError(f"Default prompt must name its skill: {skill}")

        for markdown in skill.parent.rglob("*.md"):
            check_links(markdown, skill.parent)

    for markdown in [root / "README.md", *(root / "docs").glob("*.md")]:
        check_links(markdown, root)

    assets = root / "skills/scuba-setup/assets"
    schema = json.loads((assets / "scuba-config.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    example = json.loads((assets / "scuba-config.example.json").read_text())
    if validator.is_valid(example):
        raise ValueError("Example must require the user to choose a real destination")
    example["engineering_memory"]["collection_id"] = "123e4567-e89b-42d3-a456-426614174000"
    validator.validate(example)
    for invalid in [
        {},
        {**example, "version": 2},
        {**example, "token": "not-a-real-token"},
        {**example, "engineering_memory": {"collection_id": "not-a-uuid"}},
        {**example, "engineering_memory": {"collection": "123e4567-e89b-42d3-a456-426614174000"}},
    ]:
        if validator.is_valid(invalid):
            raise ValueError(f"Invalid configuration accepted: {invalid}")
    print(f"Validated plugin manifests/catalogs, {len(skills)} skills, packaged links, MCP metadata, and configuration schema.")


def validate_plugin(root: Path) -> None:
    portable = json.loads((root / "plugin.json").read_text())
    claude = json.loads((root / ".claude-plugin/plugin.json").read_text())
    for field in ("name", "version", "description", "author", "homepage", "repository", "license"):
        if portable[field] != claude[field]:
            raise ValueError(f"Plugin manifests disagree on {field}")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", portable["version"]):
        raise ValueError("Plugin version must be a release version")
    if claude["mcpServers"] != "./.mcp.json":
        raise ValueError("Claude manifest must reference its bundled MCP configuration")
    for filename, transport in (("mcp.json", "streamable-http"), (".mcp.json", "http")):
        servers = json.loads((root / filename).read_text())["mcpServers"]
        if servers != {"scuba": {"type": transport, "url": "https://api.scuba.app/mcp/"}}:
            raise ValueError(f"Unexpected endpoint, transport, or credential fields in {filename}")
    for filename in ("openai/plugin.json", "claude/.claude-plugin/plugin.json",
                     "cursor/.cursor-plugin/plugin.json", ".cursor-plugin/plugin.json"):
        manifest = json.loads((root / filename).read_text())
        for field in ("name", "version", "repository"):
            if manifest[field] != portable[field]:
                raise ValueError(f"Platform manifest disagrees on {field}: {filename}")
    for filename in ("openai/mcp.json", "claude/.mcp.json", "cursor/mcp.json"):
        servers = json.loads((root / filename).read_text())["mcpServers"]
        if set(servers) != {"scuba"} or servers["scuba"]["url"] != "https://api.scuba.app/mcp/":
            raise ValueError(f"Unexpected platform MCP endpoint: {filename}")
    for filename in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
        catalog = json.loads((root / filename).read_text())
        if catalog["name"] != "scuba" or len(catalog["plugins"]) != 1:
            raise ValueError(f"Unexpected catalog identity or plugin count: {filename}")
        entry = catalog["plugins"][0]
        if entry["name"] != portable["name"]:
            raise ValueError(f"Catalog and plugin names differ: {filename}")
        source = entry["source"]
        if isinstance(source, dict):
            if source["source"] != "local":
                raise ValueError("Distribution catalog must install its bundled plugin")
            source = source["path"]
            if entry["policy"] != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
                raise ValueError("Unexpected catalog installation/authentication policy")
        if source != "./":
            raise ValueError(f"Catalog must resolve the repository-root plugin: {filename}")


def check_links(markdown: Path, boundary: Path) -> None:
    for target in re.findall(r"\]\(([^)]+)\)", markdown.read_text()):
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue
        path = (markdown.parent / target.split("#", 1)[0]).resolve()
        if not path.is_relative_to(boundary.resolve()) or not path.exists():
            raise ValueError(f"Missing or unbundled reference in {markdown}: {target}")


if __name__ == "__main__":
    main()
