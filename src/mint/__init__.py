"""mint - Lab Project Scaffolding Tool

A Python package that automates the creation of standardized project repositories
(data_, prj__, infra_) with pre-configured Git and DVC initialization.
"""

__version__ = "0.1.0"

from .api import create_project

__all__ = ["create_project"]