# Mint - Lab Project Scaffolding Tool

A comprehensive Python CLI tool that automates the creation of standardized research project repositories with pre-configured version control, data versioning, **mandatory language selection (Python/R/Stata)**, and **Data Commons Registry integration**. Version 1.0.0 includes full GitOps-based project registration without requiring personal access tokens, plus auto-generated utilities for logging, project validation, and schema generation.

## Features

### Core Functionality
- 🚀 **Rapid Project Setup**: Create standardized research projects in seconds
- 📊 **Multi-Language Support**: Python, R, and Stata with mandatory language selection
- 🔄 **Version Control**: Automatic Git and DVC initialization with cloud storage
- ☁️ **Cloud Storage**: S3-compatible storage support (AWS, Wasabi, MinIO)
- 📁 **Standardized Structure**: Consistent directory layouts for different project types
- 🔧 **CLI & API**: Command-line interface and Python API
- 📈 **Stata Integration**: Native Stata commands for seamless workflow
- 🛠️ **Mint Utilities**: Auto-generated utilities for logging, project validation, and schema generation
- 📝 **Parameter-Aware Logging**: Automatic logging with parameter-based filenames (e.g., `ingest_2023.log`)
- 🔖 **Version Tracking**: Metadata includes mint version and commit hash for reproducibility
- 🌐 **Cross-Platform Support**: Automatic Stata detection and platform-aware command execution
- 📍 **Script Directory Execution**: Commands run from `src/` directory for consistent path handling

### 🎉 Data Commons Registry Integration (v1.0.0)
- 🏛️ **Automatic Project Registration**: Tokenless GitOps-based cataloging
- 🔐 **Secure Access Control**: Automatic permission synchronization via GitHub Actions
- 📋 **Registry Management**: CLI commands for registration status and management
- 🔄 **Offline Mode**: Graceful handling with automatic retry when registry is unreachable
- 🚫 **Zero Token Management**: Uses SSH keys and GitHub CLI instead of personal access tokens
