# Python API

Use mintd programmatically in Python:

```python
from mintd import create_project

# Create a project (language is now required)
result = create_project(
    project_type="data",
    name="my_analysis",
    language="python",            # Required: "python", "r", or "stata"
    path="/projects",
    init_git=True,
    init_dvc=True,
    bucket_name="custom-bucket",  # Optional
    register_project=True         # Register with Data Commons Registry
)

print(f"Created: {result.full_name}")
print(f"Location: {result.path}")
if result.registration_url:
    print(f"Registration PR: {result.registration_url}")
```
