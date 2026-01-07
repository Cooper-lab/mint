# CLI Reference

## Main Commands

```bash
mint --help                    # Show help
mint --version                 # Show version (1.0.0)
```

## Project Creation

```bash
mint create data --name <name> [OPTIONS]
mint create project --name <name> [OPTIONS]
mint create infra --name <name> [OPTIONS]

Options:
  -n, --name TEXT       Project name (required)
  -p, --path PATH       Output directory (default: current)
  --lang TEXT          Primary programming language (python|r|stata, REQUIRED)
  --no-git             Skip Git initialization
  --no-dvc             Skip DVC initialization
  --bucket TEXT        Custom DVC bucket name
  --register           Register project with Data Commons Registry
  --use-current-repo   Use current directory as project root (when in existing git repo)
```

## Configuration

```bash
mint config show                    # Show current config
mint config setup                   # Interactive setup
mint config setup --set KEY VALUE  # Set specific value
mint config setup --set-credentials # Set storage credentials
```

## Registry Management

```bash
mint registry register --path <path>     # Register existing project
mint registry status <project_name>      # Check registration status
mint registry sync                       # Process pending registrations
```

## Utility Management

```bash
mint update utils                        # Update mint utilities to latest version
```
