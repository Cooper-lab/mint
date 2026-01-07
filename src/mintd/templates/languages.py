"""Language strategies for project templates."""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any


class LanguageStrategy(ABC):
    """Base class for language-specific template strategies."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Language name (e.g., 'python', 'r', 'stata')."""
        pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """File extension (e.g., 'py', 'R', 'do')."""
        pass

    def get_system_requirements(self) -> Dict[str, Any]:
        """Return system requirement files (requirements.txt, etc)."""
        return {}

    def get_project_structure(self, source_dir: str = "code") -> Dict[str, Any]:
        """Return structure for standard Project template."""
        return {}

    def get_project_files(self, source_dir: str = "code") -> List[Tuple[str, str]]:
        """Return files for standard Project template."""
        return []

    def get_data_structure(self, source_dir: str = "code") -> Dict[str, Any]:
        """Return structure for Data template."""
        return {}

    def get_data_files(self, source_dir: str = "code") -> List[Tuple[str, str]]:
        """Return files for Data template."""
        return []

    def get_infra_structure(self, package_name: str, source_dir: str = "code") -> Dict[str, Any]:
        """Return structure for Infra (Library) template."""
        return {}

    def get_infra_files(self, package_name: str, source_dir: str = "code") -> List[Tuple[str, str]]:
        """Return files for Infra (Library) template."""
        return []


class PythonStrategy(LanguageStrategy):
    """Python language strategy."""

    name = "python"
    file_extension = "py"

    def get_system_requirements(self) -> Dict[str, Any]:
        return {"requirements.txt": None}

    def get_project_structure(self, source_dir: str = "code") -> Dict[str, Any]:
        return {
            source_dir: {
                "analysis": {
                    "__init__.py": None,
                }
            }
        }

    def get_project_files(self, source_dir: str = "code") -> List[Tuple[str, str]]:
        return [
            ("requirements.txt", "requirements_project.txt.j2"),
            (f"{source_dir}/analysis/__init__.py", "__init__.py.j2"),
        ]

    def get_data_structure(self, source_dir: str = "code") -> Dict[str, Any]:
        return {
            "requirements.txt": None,
            source_dir: {
                "_mintd_utils.py": None,
                "ingest.py": None,
                "clean.py": None,
                "validate.py": None,
            }
        }

    def get_data_files(self, source_dir: str = "code") -> List[Tuple[str, str]]:
        return [
            ("requirements.txt", "requirements_data.txt.j2"),
            (f"{source_dir}/_mintd_utils.py", "_mintd_utils.py.j2"),
            (f"{source_dir}/ingest.py", "ingest.py.j2"),
            (f"{source_dir}/clean.py", "clean.py.j2"),
            (f"{source_dir}/validate.py", "validate.py.j2"),
        ]

    def get_infra_structure(self, package_name: str, source_dir: str = "code") -> Dict[str, Any]:
        return {
            "pyproject.toml": None,
            source_dir: {
                package_name: {
                    "__init__.py": None,
                },
            },
            "tests": {
                "__init__.py": None,
            },
        }

    def get_infra_files(self, package_name: str, source_dir: str = "code") -> List[Tuple[str, str]]:
        return [
            ("pyproject.toml", "pyproject_infra.toml.j2"),
            (f"{source_dir}/{package_name}/__init__.py", "__init__.py.j2"),
            ("tests/__init__.py", "__init__.py.j2"),
        ]


class RStrategy(LanguageStrategy):
    """R language strategy."""

    name = "r"
    file_extension = "R"

    def get_system_requirements(self) -> Dict[str, Any]:
        return {
            "DESCRIPTION": None,
            "renv.lock": None,
        }

    def get_project_structure(self, source_dir: str = "code") -> Dict[str, Any]:
        # Standardize R to use code/ folder logic?
        # Legacy used src/r/analysis.R. Let's modernize to code/analysis.R
        return {
            source_dir: {
                "analysis.R": None
            }
        }

    def get_project_files(self, source_dir: str = "code") -> List[Tuple[str, str]]:
        return [
            ("DESCRIPTION", "DESCRIPTION.j2"),
            ("renv.lock", "renv.lock.j2"),
            (f"{source_dir}/analysis.R", "analysis.R.j2"),
            (".Rprofile", ".Rprofile.j2"),
        ]

    def get_data_structure(self, source_dir: str = "code") -> Dict[str, Any]:
        return {
            "DESCRIPTION": None,
            "renv.lock": None,
            source_dir: {
                "_mintd_utils.R": None,
                "ingest.R": None,
                "clean.R": None,
                "validate.R": None,
            }
        }

    def get_data_files(self, source_dir: str = "code") -> List[Tuple[str, str]]:
        return [
            ("DESCRIPTION", "DESCRIPTION.j2"),
            ("renv.lock", "renv.lock.j2"),
            (f"{source_dir}/_mintd_utils.R", "_mintd_utils.R.j2"),
            (f"{source_dir}/ingest.R", "ingest.R.j2"),
            (f"{source_dir}/clean.R", "clean.R.j2"),
            (f"{source_dir}/validate.R", "validate.R.j2"),
        ]

    def get_infra_structure(self, package_name: str, source_dir: str = "code") -> Dict[str, Any]:
        # R Libraries (Packages)
        return {
            "DESCRIPTION": None,
            "NAMESPACE": None,
            source_dir: {
                # R source files usually go in R/ directory in standard packages
                # But we are using 'code' as our source root.
                # Standard R packages expect 'R/' directory.
                # We might need to map 'code' -> 'R' for R packages OR configure R to use 'code'
                # But R is strict.
                # However, for Mint consistency we want 'code'.
                # Let's assume for now we use 'code' and user might symlink or we stick to 'code' as the 'src' equivalent.
                # Wait, standard R package MUST have 'R' directory.
                # If we enforce 'code' directory, it's not a standard R package structure.
                # For Infra (Library), satisfying the Language Standard is probably more important than Mint standard?
                # But the User said: "should be similar to the prj_ where we have code, data, docs... Note that this maybe a stata, R or python library"
                # If we use 'code', we can add .Rbuildignore or config?
                # Actually, forcing 'code' instead of 'R' might break R tooling.
                # But let's follow instruction: "refactor this, it should be similar to the prj_".
                f"{package_name}.R": None, # Simple single file lib? No, package.
            }
        }

    def get_infra_files(self, package_name: str, source_dir: str = "code") -> List[Tuple[str, str]]:
        # Placeholder for R infra support
        return []


class StataStrategy(LanguageStrategy):
    """Stata language strategy."""

    name = "stata"
    file_extension = "do"
    
    def get_system_requirements(self) -> Dict[str, Any]:
        return {}

    def get_project_structure(self, source_dir: str = "code") -> Dict[str, Any]:
        return {
            source_dir: {
                ".gitkeep": None
            }
        }
        
    def get_project_files(self, source_dir: str = "code") -> List[Tuple[str, str]]:
        return []

    def get_data_structure(self, source_dir: str = "code") -> Dict[str, Any]:
        return {
            source_dir: {
                "_mintd_utils.do": None,
                "ingest.do": None,
                "clean.do": None,
                "validate.do": None,
            }
        }

    def get_data_files(self, source_dir: str = "code") -> List[Tuple[str, str]]:
        return [
            (f"{source_dir}/_mintd_utils.do", "_mintd_utils.do.j2"),
            (f"{source_dir}/ingest.do", "ingest.do.j2"),
            (f"{source_dir}/clean.do", "clean.do.j2"),
            (f"{source_dir}/validate.do", "validate.do.j2"),
        ]
        
    def get_infra_structure(self, package_name: str, source_dir: str = "code") -> Dict[str, Any]:
        return {
            source_dir: {
                f"{package_name}.ado": None
            }
        }

    def get_infra_files(self, package_name: str, source_dir: str = "code") -> List[Tuple[str, str]]:
        return []
