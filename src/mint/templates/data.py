"""Data project template (data_*)."""

from typing import Dict, List, Tuple, Any

from .base import BaseTemplate


class DataTemplate(BaseTemplate):
    """Template for data projects (data_*)."""

    prefix = "data_"

    def get_directory_structure(self) -> Dict[str, Any]:
        """Return directory structure for data projects."""
        return {
            "README.md": None,
            "metadata.json": None,
            "requirements.txt": None,
            "data": {
                "raw": {
                    ".gitkeep": None,
                },
                "intermediate": {
                    ".gitkeep": None,
                },
                "final": {
                    ".gitkeep": None,
                },
            },
            "src": {
                "__init__.py": None,
                "ingest.py": None,
                "clean.py": None,
                "validate.py": None,
                "r": {
                    ".gitkeep": None,
                },
            },
            ".gitignore": None,
            ".dvcignore": None,
            "dvc.yaml": None,
        }

    def get_template_files(self) -> List[Tuple[str, str]]:
        """Return template files for data projects."""
        return [
            ("README.md", "README_data.md.j2"),
            ("metadata.json", "metadata.json.j2"),
            ("requirements.txt", "requirements_data.txt.j2"),
            ("src/__init__.py", "__init__.py.j2"),
            ("src/ingest.py", "ingest.py.j2"),
            ("src/clean.py", "clean.py.j2"),
            ("src/validate.py", "validate.py.j2"),
            (".gitignore", "gitignore.txt"),
            (".dvcignore", "dvcignore.txt"),
            ("dvc.yaml", "dvc_data.yaml.j2"),
        ]