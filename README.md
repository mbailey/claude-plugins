# Mike Bailey's Skills Marketplace

A Claude Code plugin marketplace with skills to somewhat improve things.

## Installation

### Add Claude Code Marketplace

```
claude plugin marketplace add mbailey/skills
```

### Install a Plugin

```
claude plugin install --scope user show-me@mbailey
```

### Browse and Install Plugins

```
claude /plugin
```

## Available Plugins

| Plugin                                            | Description                                            |
| ------------------------------------------------- | ------------------------------------------------------ |
| [show-me](https://github.com/mbailey/show-me)     | Let Claude show you files and web pages (tmux, neovim) |
| [VoiceMode](https://github.com/mbailey/voicemode) | Natrual conversations with Claude Code                 |

## Security scanning

`scripts/scan_plugin.py` is a deterministic, dependency-free security scanner
for plugin directories. It flags unicode tricks (bidi/zero-width/homoglyphs),
network access, destructive commands, pipe-to-shell, credential-path access,
encoded payloads, privilege escalation, and compiled bytecode.

Run it against a plugin directory (or a `plugins/` parent) with
[`uv`](https://docs.astral.sh/uv/):

```
uv run scripts/scan_plugin.py <plugin-dir>
uv run scripts/scan_plugin.py plugins/            # scan every plugin
uv run scripts/scan_plugin.py <dir> --format=markdown
```

Exit codes: `0` clean, `1` usage error, `2` BLOCK findings, `3` WARN only.

CI runs this as a **non-blocking, informational** job (it never gates merges).
The marketplace currently lists external `url`-source plugins with no bundled
plugin directories, so the job self-skips until skills are vendored under
`plugins/`.

The scanner is vendored from
[trailofbits/skills-curated](https://github.com/trailofbits/skills-curated)
(`scripts/scan_plugin.py`) and is licensed under
[CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/); see the
attribution header in the file.
