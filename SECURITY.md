# Security Policy

## Supported Versions

The latest minor release on the `main` branch receives security updates.

## Reporting a Vulnerability

If you discover a security vulnerability in this plugin (hooks, scripts, commands, agents), please report it responsibly:

1. **Do not** open a public GitHub Issue for security reports
2. Create a private security advisory via the GitHub Security tab:
   `https://github.com/FutureRootsDE/legal-audit-de/security/advisories/new`
3. Include:
   - Affected file(s) and version
   - Reproduction steps
   - Impact assessment
   - Proposed fix (if any)

We aim to acknowledge reports within 72 hours and provide a first assessment within 7 days.

## Scope

This policy covers:
- Python hook scripts (`.claude/hooks/*.py`) — arbitrary code execution, path traversal, injection
- Utility scripts (`scripts/*.py`) — same as above
- Shell scripts (`templates/git-hooks/*.sh`) — command injection, privilege escalation
- Plugin manifest (`plugin.json`) — malformed input handling

Out of scope:
- Correctness of legal content in `knowledge/` — use a regular Issue or PR for those
- Claude Code itself (report to [Anthropic](https://www.anthropic.com/security))
- Third-party MCP servers (report upstream)

## Disclosure Policy

After a fix is merged and a new release is tagged, we publish a Security Advisory with:
- CVE identifier (if applicable)
- Affected versions
- Fix version
- Credit to the reporter (optional, with consent)
