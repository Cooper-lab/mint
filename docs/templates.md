# Custom Templates

Mint supports custom templates that allow you to define your own project structures and files. This is useful for:
- Creating lab-specific project layouts
- Standardizing repetitive project setups
- Experimenting with new project structures

## Using Custom Templates

### Discovery

Mint looks for custom templates in the following locations (in order of priority):
1. The directory specified by the `MINT_TEMPLATES_DIR` environment variable.
2. `~/.mint/templates/` directory.

### Listing Available Templates

To see all available templates, including custom ones:

```bash
mint templates list
```

### Creating a Project from a Custom Template

To create a project using a custom template:

```bash
mint create custom <template_prefix> --name <project_name>
```

For example, if you have a template with prefix `paper_`, you can run:

```bash
mint create custom paper --name my_paper
```

## Creating a Custom Template

A custom template is a Python class that inherits from `mint.templates.base.BaseTemplate`.

### Step 1: Create the Template File

Create a python file (e.g., `my_templates.py`) in `~/.mint/templates/`.

### Step 2: Define the Template Class

```python
from typing import Dict, List, Tuple, Any
from mint.templates.base import BaseTemplate

class MyTemplate(BaseTemplate):
    """My Custom Template Description."""
    
    # Prefix for projects created with this template (e.g. my_myproject)
    prefix = "my_"
    
    # Identifier for the template type (used in CLI)
    template_type = "my_template"
    
    def define_structure(self, use_current_repo: bool = False) -> Dict[str, Any]:
        """Define the directory structure."""
        return {
            "README.md": None,
            self.source_dir: {  # Uses configured source dir (default: code)
                ".gitkeep": None
            },
            "data": {
                ".gitkeep": None
            }
        }

    def define_files(self) -> List[Tuple[str, str]]:
        """Define template files to render."""
        return [
            # (relative_path_in_project, template_name_in_files_dir)
            ("README.md", "README_custom.md.j2"),
        ]
```

### Templates and Jinja2

If you use Jinja2 templates (files ending in `.j2`), they should be placed in a `files` subdirectory relative to your template python file, or you can override `__init__` to point to a specific template directory.

By default, `BaseTemplate` looks for templates in the `mint` package. Custom templates might need to set `self.template_dir` if they have their own Jinja2 files.

```python
    def __init__(self):
        super().__init__()
        # Point to local 'files' directory
        self.template_dir = Path(__file__).parent / "files"
        # Re-initialize Jinja environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
```
