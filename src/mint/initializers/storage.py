"""DVC and storage initialization for S3-compatible buckets."""

import subprocess
import shutil
from pathlib import Path
from typing import Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from ..config import get_config, get_storage_credentials


def _is_command_available(command: str) -> bool:
    """Check if a command is available on the system.

    Args:
        command: Command name to check

    Returns:
        True if command is available
    """
    return shutil.which(command) is not None


def create_bucket(project_name: str, sensitivity: str = "restricted") -> str:
    """Create a new S3-compatible bucket with versioning enabled.

    Args:
        project_name: Name of the project (used in bucket naming)
        sensitivity: Data sensitivity level ("public", "restricted", "confidential")

    Returns:
        Name of the created bucket

    Raises:
        RuntimeError: If bucket creation fails
        ValueError: If storage configuration is invalid
    """
    config = get_config()
    storage = config["storage"]

    if not storage.get("bucket_prefix"):
        raise ValueError("Bucket prefix not configured. Run 'mint config' to set it up.")

    # Create bucket name: {bucket_prefix}-{sensitivity}-{project_name}
    # Convert to lowercase and replace underscores with hyphens for S3 compatibility
    bucket_name = f"{storage['bucket_prefix']}-{sensitivity}-{project_name}".lower().replace("_", "-")

    try:
        # Get credentials
        access_key, secret_key = get_storage_credentials()

        # Set up S3 client
        client_kwargs = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
        }

        if storage.get("endpoint"):
            client_kwargs["endpoint_url"] = storage["endpoint"]
        if storage.get("region"):
            client_kwargs["region_name"] = storage["region"]

        s3 = boto3.client("s3", **client_kwargs)

        # Create bucket
        # Note: For non-AWS S3-compatible services, bucket creation parameters may vary
        if storage.get("endpoint"):
            # For S3-compatible services (Wasabi, MinIO, etc.)
            create_bucket_kwargs = {"Bucket": bucket_name}
            # Some services require additional parameters
            s3.create_bucket(**create_bucket_kwargs)
        else:
            # AWS S3
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": storage.get("region", "us-east-1")}
            )

        # Enable versioning
        if storage.get("versioning", True):
            s3.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={"Status": "Enabled"}
            )

        return bucket_name

    except NoCredentialsError:
        raise RuntimeError("Storage credentials not found. Run 'mint config --set-credentials' to set them up.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyExists':
            raise RuntimeError(f"Bucket {bucket_name} already exists")
        elif error_code == 'BucketAlreadyOwnedByYou':
            # Bucket exists but owned by us - this is OK
            return bucket_name
        else:
            raise RuntimeError(f"Failed to create bucket: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to create bucket: {e}")


def init_dvc(project_path: Path, bucket_name: str, sensitivity: str = "restricted") -> None:
    """Initialize DVC and configure S3 remote.

    Args:
        project_path: Path to the project directory
        bucket_name: Name of the S3 bucket to use as remote
        sensitivity: Data sensitivity level ("public", "restricted", "confidential")

    Raises:
        RuntimeError: If DVC operations fail
    """
    config = get_config()
    storage = config["storage"]

    try:
        # Initialize DVC
        _run_dvc_command(project_path, ["init"])

        # Add remote with sensitivity-based path prefix
        sensitivity_path = sensitivity.lower()  # "public", "restricted", or "confidential"
        remote_url = f"s3://{bucket_name}/{sensitivity_path}/"
        _run_dvc_command(project_path, ["remote", "add", "-d", "storage", remote_url])

        # Configure remote settings
        if storage.get("endpoint"):
            _run_dvc_command(project_path, [
                "remote", "modify", "storage", "endpointurl", storage["endpoint"]
            ])

        if storage.get("region"):
            _run_dvc_command(project_path, [
                "remote", "modify", "storage", "region", storage["region"]
            ])

        # Enable cloud versioning support
        if storage.get("versioning", True):
            _run_dvc_command(project_path, [
                "remote", "modify", "storage", "version_aware", "true"
            ])

    except Exception as e:
        # For any DVC-related error, just warn and continue
        # This allows the project creation to succeed even without DVC
        print(f"Warning: Failed to initialize DVC: {e}")
        print("The project was created successfully, but DVC initialization was skipped.")


def create_dvcignore(project_path: Path, project_type: str) -> None:
    """Write .dvcignore appropriate for project type.

    Note: The .dvcignore file is already created by the template system,
    so this function is mainly for future customization if needed.

    Args:
        project_path: Path to the project directory
        project_type: Type of project ("data", "project", "infra")
    """
    # The .dvcignore is already created by the template system
    # This function can be extended later for project-type-specific additions
    dvcignore_path = project_path / ".dvcignore"

    if not dvcignore_path.exists():
        raise FileNotFoundError(f".dvcignore not found at {dvcignore_path}")

    # For now, the base .dvcignore from templates is sufficient
    # Future enhancement: Add project-type-specific ignore patterns
    pass


def is_dvc_repo(project_path: Path) -> bool:
    """Check if a directory is already a DVC repository.

    Args:
        project_path: Path to check

    Returns:
        True if it's a DVC repository
    """
    dvc_dir = project_path / ".dvc"
    return dvc_dir.is_dir()


def _run_dvc_command(project_path: Path, args: list[str]) -> str:
    """Run a DVC command in the project directory.

    Args:
        project_path: Path to the project directory
        args: DVC command arguments

    Returns:
        Command output

    Raises:
        subprocess.CalledProcessError: If the command fails
        FileNotFoundError: If dvc is not available
    """
    try:
        result = subprocess.run(
            ["dvc"] + args,
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except FileNotFoundError:
        raise FileNotFoundError("dvc command not found")
    except subprocess.CalledProcessError as e:
        # Check if it's a "command not found" type error
        if "returned non-zero exit status" in str(e) and b"dvc: command not found" in e.stderr.encode():
            raise FileNotFoundError("dvc command not found")
        raise