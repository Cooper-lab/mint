# Project Types

## Data Projects (`data_*`)

For data products and processing pipelines. Supports Python, R, and Stata:

**Python-focused:**
```
data_healthcare/
├── README.md                 # Project documentation
├── metadata.json            # Project metadata (with mint version)
├── requirements.txt         # Python dependencies
├── logs/                    # Script execution logs
├── data/
│   ├── raw/                 # Raw data (DVC tracked)
│   ├── intermediate/        # Processed data (DVC tracked)
│   └── final/               # Analysis-ready data (DVC tracked)
├── src/
│   ├── _mint_utils.py       # Mint utilities (auto-generated)
│   ├── ingest.py           # Data acquisition
│   ├── clean.py            # Data cleaning
│   └── validate.py         # Data validation
├── .gitignore
├── .dvcignore
└── dvc.yaml                # Pipeline configuration (python commands)
```

**R-focused:**
```
data_healthcare/
├── README.md                 # Project documentation
├── metadata.json            # Project metadata (with mint version)
├── DESCRIPTION              # R package description
├── renv.lock               # R environment snapshot
├── logs/                    # Script execution logs
├── data/
│   ├── raw/                 # Raw data (DVC tracked)
│   ├── intermediate/        # Processed data (DVC tracked)
│   └── final/               # Analysis-ready data (DVC tracked)
├── src/
│   ├── _mint_utils.R        # Mint utilities (auto-generated)
│   ├── ingest.R            # Data acquisition
│   ├── clean.R             # Data cleaning
│   └── validate.R          # Data validation
├── .gitignore
├── .dvcignore
└── dvc.yaml                # Pipeline configuration (Rscript commands)
```

**Stata-focused:**
```
data_healthcare/
├── README.md                 # Project documentation
├── metadata.json            # Project metadata (with mint version)
├── logs/                    # Script execution logs
├── data/
│   ├── raw/                 # Raw data (DVC tracked)
│   ├── intermediate/        # Processed data (DVC tracked)
│   └── final/               # Analysis-ready data (DVC tracked)
├── src/
│   ├── _mint_utils.do       # Mint utilities (auto-generated)
│   ├── ingest.do           # Data acquisition (runs from src/)
│   ├── clean.do            # Data cleaning (runs from src/)
│   └── validate.do         # Data validation (runs from src/)
├── .gitignore
├── .dvcignore
└── dvc.yaml                # Pipeline configuration (cd src && stata -b do commands)
```

## Research Projects (`prj__*`)

For analysis and research projects:

```
prj__cost_study/
├── README.md
├── metadata.json
├── requirements.txt
├── renv.lock               # R environment (if used)
├── data/                   # Project data
├── src/
│   ├── analysis/          # Python analysis scripts
│   ├── stata/             # Stata do-files
│   └── r/                 # R analysis scripts
├── output/
│   ├── figures/           # Generated plots
│   └── tables/            # Generated tables
├── docs/                  # Documentation
├── .Rprofile              # R configuration
├── .gitignore
└── .dvcignore
```

## Infrastructure Projects (`infra_*`)

For reusable packages and tools:

```
infra_stat_tools/
├── README.md
├── metadata.json
├── pyproject.toml          # Package configuration
├── src/
│   └── stat_tools/        # Main package
├── tests/
│   └── __init__.py
└── docs/
```

## Secure Enclave Projects (`enclave_*`)

For air-gapped environments requiring secure data transfer:

```
enclave_secure_workspace/
├── README.md                 # Enclave documentation
├── metadata.json            # Project metadata
├── enclave_manifest.yaml    # Data transfer tracking
├── requirements.txt         # Dependencies
├── data/                    # Data storage
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── registry.py         # Registry integration
│   ├── download.py         # Data pulling logic
│   ├── package.py          # Transfer packaging
│   └── verify.py           # Integrity verification
├── scripts/
│   ├── pull_data.sh        # Pull latest data
│   ├── package_transfer.sh # Create transfer archive
│   ├── unpack_transfer.sh  # Unpack in enclave
│   └── verify_transfer.sh  # Verify checksums
├── transfers/              # Transfer archives
├── .gitignore
└── .dvcignore
```
