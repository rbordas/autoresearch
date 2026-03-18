# Contributing to Autoresearch

Thanks for wanting to make autoresearch better. Whether you're fixing a typo, adding examples, creating a new sub-command, or improving the loop protocol — this guide will get you up and running fast.

## Quick Start

Autoresearch is Markdown files that Claude Code discovers from `skills/` and `commands/` directories. No build step, no compilation — edit a `.md` file, invoke the skill, see your changes.

```bash
# 1. Clone the repo
git clone https://github.com/uditgoenka/autoresearch.git
cd autoresearch

# 2. Copy to your local Claude Code (for testing)
cp -r skills/autoresearch ~/.claude/skills/autoresearch
cp -r commands/autoresearch ~/.claude/commands/autoresearch

# 3. Or symlink for live editing (recommended for development)
ln -s $(pwd)/skills/autoresearch ~/.claude/skills/autoresearch
ln -s $(pwd)/commands/autoresearch ~/.claude/commands/autoresearch
```

When done developing, replace symlinks with stable copies:
```bash
rm ~/.claude/skills/autoresearch ~/.claude/commands/autoresearch
cp -r skills/autoresearch ~/.claude/skills/autoresearch
cp -r commands/autoresearch ~/.claude/commands/autoresearch
```

## Repository Structure

```
autoresearch/
├── README.md                                      ← Project overview + quick start
├── GUIDE.md                                       ← Complete guide — installation to advanced chains
├── EXAMPLES.md                                    ← Real-world examples by domain
├── CONTRIBUTING.md                                ← You are here
├── LICENSE                                        ← MIT License
├── .claude-plugin/
│   ├── marketplace.json                           ← Plugin marketplace manifest
│   └── plugin.json                                ← Plugin metadata + version
├── commands/
│   └── autoresearch/
│       ├── plan.md                                ← /autoresearch:plan registration
│       ├── security.md                            ← /autoresearch:security registration
│       ├── ship.md                                ← /autoresearch:ship registration
│       ├── debug.md                               ← /autoresearch:debug registration
│       ├── fix.md                                 ← /autoresearch:fix registration
│       ├── scenario.md                            ← /autoresearch:scenario registration
│       └── predict.md                             ← /autoresearch:predict registration
├── skills/
│   └── autoresearch/
│       ├── SKILL.md                               ← Main skill (loaded by Claude Code)
│       └── references/
│           ├── autonomous-loop-protocol.md        ← 8-phase loop protocol
│           ├── core-principles.md                 ← 7 universal principles
│           ├── plan-workflow.md                   ← Plan wizard protocol
│           ├── security-workflow.md               ← Security audit protocol
│           ├── ship-workflow.md                   ← Ship workflow protocol
│           ├── debug-workflow.md                  ← Debug loop protocol
│           ├── fix-workflow.md                    ← Fix loop protocol
│           ├── scenario-workflow.md               ← Scenario exploration protocol
│           ├── predict-workflow.md                ← Multi-persona swarm prediction workflow
│           └── results-logging.md                 ← TSV tracking format
└── scripts/
    ├── release.sh                                 ← Release script (version bump + PR + tag)
    └── release.md                                 ← Release process documentation
```

### What Each File Does

| File | Purpose | Edit when... |
|------|---------|-------------|
| `SKILL.md` | Main entry point. Sub-command routing, setup phase, loop pseudocode, domain table. | Adding sub-commands, changing activation triggers, updating loop behavior |
| `references/autonomous-loop-protocol.md` | 8-phase loop protocol with rules for each phase. | Changing how the loop works (review, ideate, modify, commit, verify, guard, decide, log) |
| `references/core-principles.md` | 7 universal principles from Karpathy's autoresearch. | Refining principles or adding new ones |
| `references/plan-workflow.md` | `/autoresearch:plan` wizard protocol. | Changing planning flow, question types, metric suggestions |
| `references/security-workflow.md` | `/autoresearch:security` audit protocol. | Adding OWASP checks, red-team personas, report structure |
| `references/ship-workflow.md` | `/autoresearch:ship` shipping workflow. | Adding ship types, checklists, rollback actions |
| `references/debug-workflow.md` | `/autoresearch:debug` bug-hunting protocol. | Adding investigation techniques, bug patterns, domain checklists |
| `references/fix-workflow.md` | `/autoresearch:fix` error repair protocol. | Adding fix strategies, anti-patterns, language-specific patterns |
| `references/scenario-workflow.md` | `/autoresearch:scenario` scenario exploration. | Adding domains, dimensions, output formats |
| `references/predict-workflow.md` | `/autoresearch:predict` multi-persona swarm prediction workflow (751 lines). | Adding prediction personas, confidence models, output formats |
| `references/results-logging.md` | TSV log format and reporting rules. | Changing log columns, summary format, reporting intervals |
| `commands/autoresearch/*.md` | Sub-command registration files. | Adding new sub-commands (creates the `/autoresearch:name` slash command) |
| `.claude-plugin/plugin.json` | Plugin metadata + version. | Version bumps (use `scripts/release.sh`) |
| `README.md` | Public overview, commands table, quick start. | Adding features, updating commands, documenting changes |
| `GUIDE.md` | Comprehensive user guide with all domains and chains. | Adding scenarios, command combinations, advanced patterns |
| `EXAMPLES.md` | Copy-paste examples organized by domain. | Adding real-world examples, new domain sections |

## What to Contribute

### High-Value Contributions

| Type | Examples | Difficulty |
|------|----------|-----------|
| **New domain examples** | Add to EXAMPLES.md or GUIDE.md | Easy |
| **Verification script templates** | Reusable scripts for common metrics | Easy |
| **Bug fixes** | Loop edge cases, incorrect behavior | Medium |
| **New sub-commands** | `/autoresearch:refactor`, `/autoresearch:test` | Medium |
| **New ship types** | Additional checklist types for `/autoresearch:ship` | Medium |
| **OWASP/STRIDE additions** | New security checks for `/autoresearch:security` | Medium |
| **New scenario domains** | Additional domain templates for `/autoresearch:scenario` | Medium |
| **Protocol improvements** | Better stuck-detection, smarter ideation | Hard |
| **MCP integration patterns** | Database, API, analytics verification examples | Hard |

### Low-Value (Please Don't)

- Reformatting or restructuring existing files without functional changes
- Adding comments to explain obvious things
- Changing naming conventions or style
- Whitespace-only changes

## Day-to-Day Workflow

```bash
# 1. Fork and clone
gh repo fork uditgoenka/autoresearch --clone
cd autoresearch

# 2. Create a feature branch
git checkout -b feat/your-feature-name

# 3. Symlink for live testing
ln -s $(pwd)/skills/autoresearch ~/.claude/skills/autoresearch
ln -s $(pwd)/commands/autoresearch ~/.claude/commands/autoresearch

# 4. Make your changes
# Edit skill files, reference files, commands, docs, etc.

# 5. Test in Claude Code (changes are live via symlink)
# Open Claude Code in any project and invoke the relevant command

# 6. Commit with conventional format
git add -A
git commit -m "feat: add guard rework timeout after 60 seconds"

# 7. Push and create PR
git push -u origin feat/your-feature-name
gh pr create --title "feat: your feature" --body "## Summary\n- What changed\n- Why"
```

## Commit Messages

We use [conventional commits](https://www.conventionalcommits.org/):

| Prefix | When |
|--------|------|
| `feat:` | New feature or sub-command |
| `fix:` | Bug fix in existing behavior |
| `docs:` | Documentation-only changes |
| `refactor:` | Restructuring without behavior change |
| `chore:` | Maintenance (CI, config, tooling, version bumps) |

## Pull Request Guidelines

1. **One PR = one feature.** Don't bundle unrelated changes.
2. **Branch from `master`.** Target `master` as base.
3. **Descriptive title.** Use conventional commit format.
4. **Write a good body.** Explain what changed, why, and how to test it.
5. **Update docs.** If you add a feature, update the relevant docs:
   - `SKILL.md` — register sub-commands, update activation triggers
   - `README.md` — commands table, quick decision guide, repo structure, FAQ
   - `GUIDE.md` — command reference, domain scenarios, chain patterns
   - `EXAMPLES.md` — add copy-paste examples for new features
6. **Don't bump the version.** Maintainers handle version bumps via `scripts/release.sh`.
7. **Keep files focused.** Don't modify files unrelated to your change.

### PR Template

```markdown
## Summary
- What changed and why

## Files Changed
| File | Change |
|------|--------|
| `references/fix-workflow.md` | Added Rust-specific fix strategies |
| `EXAMPLES.md` | Added Rust examples section |

## How to Test
1. Symlink skill to ~/.claude/skills/autoresearch
2. Run /autoresearch:fix in a Rust project
3. Verify Rust-specific strategies are applied
```

## Adding a New Sub-Command

Follow this pattern when adding a command like `/autoresearch:yourcommand`:

### 1. Create the reference file

```
skills/autoresearch/references/your-workflow.md
```

Contains: full protocol, phases, rules, examples, flags, error recovery, composite metric, output directory structure.

### 2. Create the command registration file

```
commands/autoresearch/yourcommand.md
```

This thin wrapper tells Claude Code to load SKILL.md + your reference file and execute the workflow.

### 3. Register in SKILL.md

Add to the subcommands table:
```markdown
| `/autoresearch:yourcommand` | Description of what it does |
```

Add a full sub-command section with:
- `Load: references/your-workflow.md` directive
- Numbered phase summary
- Usage examples with flags
- Key behaviors and composite metric

Add to the "When to Activate" section:
```markdown
- User invokes `/autoresearch:yourcommand` → run your workflow
- User says "relevant trigger phrases" → run your workflow
```

Add to the interactive setup gate table.

### 4. Update all docs

| Doc | What to Update |
|-----|---------------|
| `README.md` | Commands table, Quick Decision Guide, dedicated section, repo structure, FAQ |
| `GUIDE.md` | Command Reference section, relevant domain scenarios, chain patterns |
| `EXAMPLES.md` | Add examples section for the new command |

## Testing Your Changes

No automated test suite — autoresearch is Markdown instructions, not code. Testing means using it:

1. **Symlink your working tree** (see Quick Start)
2. **Open Claude Code in a real project**
3. **Invoke the skill** (`/autoresearch`, `/autoresearch:plan`, etc.)
4. **Verify behavior matches your changes**
5. **Try edge cases** — wrong metric? Scope matches 0 files? Guard always fails?

### What to Check

- Does Claude follow your updated instructions?
- Does the output format match your specification?
- Are error cases handled gracefully?
- Does backward compatibility hold? (Existing commands still work)
- Does the interactive setup ask the right questions?

## Release Process

Maintainers use `scripts/release.sh` to handle releases. See `scripts/release.md` for full documentation.

```bash
# Patch release (bugfixes, docs updates)
./scripts/release.sh 1.7.1 --title "Fix scenario timeout"

# Minor release (new features, new commands)
./scripts/release.sh 1.7.0 --title "New Sub-Command Name"
```

The script: creates release branch → bumps plugin.json + README badge → pauses for doc review → commits → creates PR → waits for merge confirmation → tags → creates GitHub release.

**Contributors don't need to bump versions** — maintainers handle this during release.

## Things to Know

- **No build step.** Everything is Markdown. Edit → test → commit.
- **SKILL.md is the entry point.** Claude Code reads this first. References are loaded on demand.
- **References are lazy-loaded.** Only loaded when the relevant sub-command is invoked. Keeps context usage low.
- **commands/ directory is required.** Without it, sub-commands (`/autoresearch:plan`, etc.) won't register as slash commands.
- **Plugin system.** Users can install via `/plugin install` — the `.claude-plugin/` directory makes this work.
- **The repo is MIT licensed.** Your contributions will be under the same license.

## Getting Help

- **Questions?** Open an [issue](https://github.com/uditgoenka/autoresearch/issues)
- **Ideas?** Open an issue with `[Idea]` prefix
- **Bug reports?** Open an issue with reproduction steps
- **Discussion?** Tag [@uditgoenka](https://github.com/uditgoenka) in your PR

Thanks for contributing!
