"""Command Line Interface for mint."""

import click
from rich.console import Console

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """mint - Lab Project Scaffolding Tool"""
    pass


@main.group()
def create():
    """Create a new project."""
    pass


@create.command()
@click.option("--name", "-n", required=True, help="Project name")
@click.option("--path", "-p", default=".", help="Output directory")
@click.option("--no-git", is_flag=True, help="Skip Git initialization")
@click.option("--no-dvc", is_flag=True, help="Skip DVC initialization")
@click.option("--bucket", help="Override bucket name for DVC remote")
def data(name: str, path: str, no_git: bool, no_dvc: bool, bucket: str):
    """Create a data product repository (data_{name})."""
    from .api import create_project

    with console.status("Scaffolding project..."):
        try:
            result = create_project(
                project_type="data",
                name=name,
                path=path,
                init_git=not no_git,
                init_dvc=not no_dvc,
                bucket_name=bucket,
            )
            console.print(f"✅ Created: {result.full_name}", style="green")
            console.print(f"   Location: {result.path}", style="dim")
        except Exception as e:
            console.print(f"❌ Error: {e}", style="red")
            raise click.Abort()


@create.command()
@click.option("--name", "-n", required=True, help="Project name")
@click.option("--path", "-p", default=".", help="Output directory")
@click.option("--no-git", is_flag=True, help="Skip Git initialization")
@click.option("--no-dvc", is_flag=True, help="Skip DVC initialization")
@click.option("--bucket", help="Override bucket name for DVC remote")
def project(name: str, path: str, no_git: bool, no_dvc: bool, bucket: str):
    """Create a project repository (prj__{name})."""
    from .api import create_project

    with console.status("Scaffolding project..."):
        try:
            result = create_project(
                project_type="project",
                name=name,
                path=path,
                init_git=not no_git,
                init_dvc=not no_dvc,
                bucket_name=bucket,
            )
            console.print(f"✅ Created: {result.full_name}", style="green")
            console.print(f"   Location: {result.path}", style="dim")
        except Exception as e:
            console.print(f"❌ Error: {e}", style="red")
            raise click.Abort()


@create.command()
@click.option("--name", "-n", required=True, help="Project name")
@click.option("--path", "-p", default=".", help="Output directory")
@click.option("--no-git", is_flag=True, help="Skip Git initialization")
@click.option("--no-dvc", is_flag=True, help="Skip DVC initialization")
@click.option("--bucket", help="Override bucket name for DVC remote")
def infra(name: str, path: str, no_git: bool, no_dvc: bool, bucket: str):
    """Create an infrastructure repository (infra_{name})."""
    from .api import create_project

    with console.status("Scaffolding project..."):
        try:
            result = create_project(
                project_type="infra",
                name=name,
                path=path,
                init_git=not no_git,
                init_dvc=not no_dvc,
                bucket_name=bucket,
            )
            console.print(f"✅ Created: {result.full_name}", style="green")
            console.print(f"   Location: {result.path}", style="dim")
        except Exception as e:
            console.print(f"❌ Error: {e}", style="red")
            raise click.Abort()


@main.group()
def config():
    """Configure mint settings."""


@config.command()
def show():
    """Show current configuration."""
    from .config import get_config

    config = get_config()

    console.print("[bold]Current Configuration:[/bold]")
    console.print()

    console.print("[bold blue]Storage:[/bold blue]")
    storage = config.get("storage", {})
    console.print(f"  Provider: {storage.get('provider', 'Not set')}")
    console.print(f"  Endpoint: {storage.get('endpoint', 'Not set')}")
    console.print(f"  Region: {storage.get('region', 'Not set')}")
    console.print(f"  Bucket Prefix: {storage.get('bucket_prefix', 'Not set')}")
    console.print(f"  Versioning: {storage.get('versioning', 'Not set')}")

    console.print()
    console.print("[bold blue]Defaults:[/bold blue]")
    defaults = config.get("defaults", {})
    console.print(f"  Author: {defaults.get('author', 'Not set')}")
    console.print(f"  Organization: {defaults.get('organization', 'Not set')}")


@config.command()
@click.option("--set", "set_value", nargs=2, metavar="KEY VALUE",
              help="Set a configuration value (e.g., --set storage.bucket_prefix mylab)")
@click.option("--set-credentials", is_flag=True,
              help="Set storage credentials interactively")
def setup(set_value, set_credentials):
    """Set up or modify configuration."""
    from .config import init_config, save_config, get_config, set_storage_credentials

    if set_value:
        key, value = set_value
        config = get_config()

        # Parse nested keys like "storage.bucket_prefix"
        keys = key.split(".")
        current = config
        for k in keys[:-1]:
            current = current.setdefault(k, {})
        current[keys[-1]] = value

        save_config(config)
        console.print(f"✅ Set {key} = {value}")

    elif set_credentials:
        from rich.prompt import Prompt

        access_key = Prompt.ask("AWS Access Key ID")
        secret_key = Prompt.ask("AWS Secret Access Key", password=True)

        try:
            set_storage_credentials(access_key, secret_key)
            console.print("✅ Credentials stored securely")
        except RuntimeError as e:
            console.print(f"❌ Error storing credentials: {e}")

    else:
        # Interactive setup
        init_config()


if __name__ == "__main__":
    main()