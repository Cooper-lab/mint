# Mintd Utilities

mintd automatically generates utility files (`_mintd_utils.{py|R|do}`) that provide common functionality for all project scripts:

## Features

### Project Directory Validation
- Ensures scripts run from the correct project root directory
- Provides clear error messages if executed from wrong location
- Automatically detects project root via `metadata.json` or `.git`

### Parameter-Aware Logging
- Creates timestamped log files with parameter-based names
- Examples: `ingest_2023.log`, `clean_v2.log`, `validate_20241222_143052.log`
- Logs include: command executed, parameters, start/end times, working directory
- Complements DVC versioning with execution audit trails

### Schema Generation
- Extracts variable metadata from data files (CSV, DTA, RDS, etc.)
- Captures: variable names, types, labels, observation counts
- Outputs JSON schema for Data Commons Registry integration
- Useful for data dictionary creation and validation

## Usage in Scripts

**Python:**
```python
from _mintd_utils import setup_project_directory, ParameterAwareLogger

# Validate project directory and set up logging
logger = ParameterAwareLogger("ingest")
logger.log("Starting data ingestion...")

# Your script code here
logger.log("Processing completed successfully.")
logger.close()
```

**R:**
```r
source("_mintd_utils.R")

# Set up logging
logger <- ParameterAwareLogger("clean")
logger$log("Starting data cleaning...")

# Your script code here
logger$log("Cleaning completed successfully.")
logger$close()
```

**Stata:**
```stata
do _mintd_utils.do

* Initialize logging
ParameterAwareLogger clean
log_message "Starting data validation..."

* Your script code here
log_message "Validation completed successfully."
close_logger
```

## Updating Utilities

When mintd is updated, you can refresh the utility files without touching your scripts:

```bash
mintd update utils
```

This command:
- Regenerates `_mintd_utils.*` files with latest features
- Updates mintd version information in `metadata.json`
- Preserves all your custom scripts and data
