"""Shared utilities for the mint package."""


def validate_project_name(name: str) -> bool:
    """Validate that a project name is valid.

    Args:
        name: Project name to validate

    Returns:
        True if valid, False otherwise
    """
    # Basic validation - can be expanded later
    if not name:
        return False
    if any(char in name for char in [" ", "/", "\\", ":", "*", "?", '"', "<", ">", "|"]):
        return False
    return True


def format_project_name(project_type: str, name: str) -> str:
    """Format a full project name with the appropriate prefix.

    Args:
        project_type: Type of project ("data", "project", or "infra")
        name: Base project name

    Returns:
        Full project name with prefix
    """
    if project_type == "data":
        return f"data_{name}"
    elif project_type == "project":
        return f"prj__{name}"
    elif project_type == "infra":
        return f"infra_{name}"
    else:
        raise ValueError(f"Unknown project type: {project_type}")