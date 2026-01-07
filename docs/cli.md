# CLI Reference

## Main Commands

```bash
mintd --help                    # Show help
mintd --version                 # Show version (1.0.0)
```

## Project Creation

```bash
mintd create data --name <name> [OPTIONS]
mintd create project --name <name> [OPTIONS]
mintd create infra --name <name> [OPTIONS]

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
mintd config show                    # Show current config
mintd config setup                   # Interactive setup
mintd config setup --set KEY VALUE  # Set specific value
mintd config setup --set-credentials # Set storage credentials
```

## Registry Management

```bash
mintd registry register --path <path>     # Register existing project
mintd registry status <project_name>      # Check registration status
mintd registry sync                       # Process pending registrations
```

## Utility Management

```bash
mintd update utils                        # Update mintd utilities to latest version
```
