# Registry Integration

mint integrates with a Data Commons Registry for automatic project cataloging and access control enforcement.

## Prerequisites

Registry integration requires:
- SSH key configured for GitHub
- GitHub CLI (`gh`) installed and authenticated: `gh auth login`
- Push access to the registry repository

## Registry Configuration

```bash
# Set registry URL (required for registration)
mint config setup --set registry.url https://github.com/your-org/data-commons-registry

# Or set via environment variable
export MINT_REGISTRY_URL=https://github.com/your-org/data-commons-registry
```

## Registration Workflow

```bash
# Create project with automatic registration
mint create data --name medicare_data --lang python --register

# Behind the scenes:
# 1. Project scaffolding (Git/DVC setup)
# 2. Clone registry repository via SSH
# 3. Generate catalog entry YAML
# 4. Create feature branch: register-medicare_data
# 5. Commit catalog entry + push branch
# 6. Open PR via GitHub CLI
# 7. Return PR URL to user

# Output:
# ✅ Created: data_medicare_data
# 📋 Registration PR: https://github.com/org/registry/pull/123
```

## Registry Management Commands

```bash
# Register existing projects
mint registry register --path /path/to/project

# Check registration status
mint registry status medicare_data

# Process pending registrations (when offline)
mint registry sync
```

## Registry Features

- **✅ Tokenless Operation**: Uses SSH keys + GitHub CLI instead of personal tokens
- **✅ Offline Mode**: Queues registrations when network unavailable
- **✅ Automatic Retry**: Processes pending registrations on next run
- **✅ PR Tracking**: Provides links to registration pull requests
- **✅ Access Control**: Automatic permission synchronization via GitHub Actions

## GitHub CLI & Git Commands Used

mint uses a **GitOps architecture** where all GitHub operations happen via standard Git and the GitHub CLI (`gh`), eliminating the need for personal access tokens.

### GitHub CLI Commands

| Command | Purpose |
|---------|---------|
| `gh auth login` | One-time authentication setup (required prerequisite) |
| `gh pr create --title "..." --body "..." --head <branch> --base main` | Creates pull requests for project registration |
| `gh pr list --state open --json title,url,headRefName` | Checks registration status by listing open PRs |

### Git Commands (via subprocess)

| Command | Purpose |
|---------|---------|
| `git clone git@github.com:<org>/<repo>.git` | Clones registry repository via SSH |
| `git checkout -b register-<project_name>` | Creates feature branch for registration |
| `git add .` | Stages catalog entry changes |
| `git commit -m "Register new project: <name>"` | Commits the catalog entry |
| `git push -u origin <branch>` | Pushes branch to trigger PR workflow |

### GitOps Registration Flow

```text
┌─────────────────────────────────────────────────────────────────┐
│                     User's Machine                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  mint create data --name medicare --lang python --register│  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│      1. Scaffold project   │                                    │
│      2. git clone (SSH)    ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Clone registry repo → Create branch → Write YAML →      │  │
│  │  git commit → git push → gh pr create                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Actions Runner                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  validate-catalog.yml  (on PR)                            │  │
│  │  - Validate YAML schema                                   │  │
│  │  - Check naming conventions                               │  │
│  │  - Verify access control requirements                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  sync-permissions.yml  (on merge to main)                 │  │
│  │  - Read access_control from catalog YAML                  │  │
│  │  - Sync GitHub team permissions to repository             │  │
│  │  - Apply collaborator settings                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Why Tokenless?

Traditional approaches require personal access tokens (PATs) that:

- Need manual rotation and secure storage
- Are tied to individual user accounts  
- Can become security vulnerabilities if leaked

The GitOps approach instead uses:

- **SSH Keys**: Already configured for git operations, managed by user
- **GitHub CLI**: Handles OAuth flow securely via `gh auth login`
- **GitHub Actions**: Workflows run with `GITHUB_TOKEN` (automatic, scoped, rotated)

This separation means users never handle long-lived tokens, and all sensitive operations happen in controlled GitHub Actions environments.
