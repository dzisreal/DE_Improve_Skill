# Global Codex skills for Data Engineering

This bundle installs five selected skills for the current OS user. Installing on
one machine does not sync to other machines, accounts, or cloud environments.

## Install on macOS or Linux

Requires Python 3.9+. On Ubuntu/Debian, install it with `sudo apt-get install
python3` if missing. On macOS, use `brew install python` when Homebrew is already
available, or the installer from https://www.python.org/downloads/macos/.
Do not run this bundle installer with sudo.

Download and extract the bundle, open a terminal in this folder:

```sh
python3 install.py --check
python3 install.py
```

The same commands work on Linux and macOS, including Apple Silicon. Installation
uses only the Python standard library and the included files; upstream network
access is not required. This does not install the Codex application itself.

The default destination is `~/.agents/skills/`, available across projects on that
machine. Start a new Codex chat after installation. Existing skills with different
contents are never overwritten. Re-running the same bundle is safe. A different
version requires explicitly resolving the conflicting installation first.
`--check` does not install anything: it reports how many skills are still missing.
After installation it should report zero missing skills.

## Use

| Skill | Example request |
|---|---|
| `socratic-tutor` | Use $socratic-tutor to assess and teach me CDC and idempotency. |
| `data-architect` | Use $data-architect to compare lakehouse migration options for this workload. |
| `requesting-code-review` | Use $requesting-code-review to review this Python ingestion tool. |
| `data-review` | Use $data-review to check the SQL changes, grain and downstream impact. |
| `data-platform-reliability-reviewer` | Use $data-platform-reliability-reviewer to review this Kafka/Spark recovery design. |

Skills are available globally but should load only for relevant tasks. The tutor
is for explicit teaching requests. Project instructions and the user's current
request retain precedence. The installer does not edit global AGENTS.md,
configure hooks, connect MCP servers, provision cloud resources, or install
unrelated skill collections. Cloud credentials are not included.

## Sources and adaptations

`manifest.json` records source repositories, exact Git commits, adaptations and
SHA-256 hashes of every installed file. Each skill includes its upstream license
and `INSTALL-SOURCE.json`. Adapted skills retain their original entry text.

- Jane Street's socratic tutor is copied unchanged.
- Magnus's data architect includes its references and templates; optional routes
  to other skills do not block a review. Current product claims must be verified.
- Superpowers' reviewer includes its reviewer template and Codex compatibility
  guidance, including review-only scope and unavailable-subagent fallback.
- Aurora's data review works without forcing issue-tracker setup in every project
  and includes uncommitted changes when requested. Its modeling rules remain
  conditional heuristics.
- Vaquarkhan's platform reviewer is wrapped as a discoverable skill. Companion
  workflows, references, templates and example MCP configurations are bundled as
  reference material, not separately activated skills or installed connections.
  Review does not authorize executing the operational actions those docs describe.

This is an installation and compatibility package, not a claim of benchmarked
review accuracy or validated teaching effectiveness. The review skills still need
real code, requirements and evidence to produce useful findings.

## Removal

Remove only the five corresponding directories from the installation destination
after checking for personal edits. Built-in and unrelated skills are untouched.
For upgrades, first move conflicting skill directories to a backup OUTSIDE the
skills discovery tree, then run the new installer. To roll back, move the new
directories out and restore the backup. Open a new Codex chat after either change.

Full installation, usage and maintenance documentation is versioned in the
repository: https://github.com/dzisreal/DE_Improve_Skill (see the docs directory).
