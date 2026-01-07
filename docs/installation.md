# Installation

## Using uv (Recommended)

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install mint
git clone <repository-url>
cd mint
uv sync --dev
```

## Using pip

```bash
# Install directly from git (PyPI not available)
pip install git+https://github.com/Cooper-lab/mint.git

# Install from source (development)
git clone https://github.com/Cooper-lab/mint.git
cd mint
pip install -e ".[dev]"

# Verify installation
python verify_installation.py
```

**Version 1.0.0** includes complete Data Commons Registry integration with tokenless GitOps-based project registration, plus mandatory language selection, parameter-aware logging, and auto-generated utility scripts.

## Requirements

### Core Requirements
- **Python**: 3.9+
- **Optional**: Git, DVC for version control features
- **Stata**: 16+ for Stata integration

### Registry Integration (Optional)
- **SSH Key**: Configured for GitHub (`ssh-keygen -t ed25519 -C "your_email@example.com"`)
- **GitHub CLI**: Installed and authenticated (`gh auth login`)
- **Registry Access**: Push permissions to the Data Commons Registry repository
