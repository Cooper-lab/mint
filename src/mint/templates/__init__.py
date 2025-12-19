"""Project templates for different project types."""

from .base import BaseTemplate
from .data import DataTemplate
from .project import ProjectTemplate
from .infra import InfraTemplate

__all__ = ["BaseTemplate", "DataTemplate", "ProjectTemplate", "InfraTemplate"]