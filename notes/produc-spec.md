# PRD: mono (Lab Project Scaffolding Tool)

## 1. Product overview

### 1.1 Document title and version
   - PRD: mono (Lab Project Scaffolding Tool)
   - Version: 0.1.0 (MVP)

### 1.2 Product summary
`mono` is a Python-based scaffolding package designed to standardize data science and economic research projects within the lab. It automates the creation of standardized GitHub repositories (`data_`, `prj__`, `infra_`) with pre-configured Git and DVC initialization.

Crucially, `mono` acts as the client-side enforcer for the lab's "Data Commons." It utilizes a GitOps workflow to automatically register new projects into a central Registry Repository and enforces access control policies via code. This ensures that while researchers focus on "getting stuff done," compliance and cataloging happen transparently in the background. The tool is accessible via both a Python CLI and a native Stata command (`prjsetup`) for the primary user base of non-technical researchers.

## 2. Goals

### 2.1 Business goals
   - **100% Catalog Coverage**: Ensure every new data product or analysis project is automatically logged in the central Data Commons Registry.
   - **Policy-as-Code Enforcement**: Replace manual repository configuration with automated, code-defined access policies managed via GitHub Actions.
   - **Standardization**: Enforce uniform directory structures across the lab to facilitate code review and reproducibility for senior staff.

### 2.2 User goals
   - **Frictionless Setup**: Allow junior researchers to spin up a fully compliant environment (Repo + S3 + Permissions) in under 2 minutes.
   - **Tooling Agnostic Entry**: Enable users to create projects from their preferred environment (Stata or Terminal) without needing DevOps knowledge.
   - **Automated "Plumbing"**: Remove the need for users to manually configure S3 buckets, DVC remotes, or API tokens.

### 2.3 Non-goals
   - Building a custom web UI for the Data Registry (MVP will rely on GitHub's native file viewing and PR interface).
   - Handling data ingestion logic or ETL pipelines (Scope is limited to scaffolding and registration).
   - Supporting cloud providers other than Wasabi S3 and GitHub for the MVP.

## 3. User personas

### 3.1 Key user types
   - Junior Researcher (Primary)
   - Senior Research Reviewer
   - Data Infrastructure Admin

### 3.2 Basic persona details
   - **Junior Researcher**: Non-technical domain experts (Economists/Analysts). They value speed and "getting stuff done" over adhering to complex guidelines. They work primarily in Stata and view technical configuration as a blocker.
   - **Senior Research Reviewer**: Does not code but reviews outputs (tables, figures). Needs consistent folder structures to locate results quickly without asking "where is the file?".
   - **Data Infrastructure Admin**: Manages security and compliance. Needs a "God-view" of all data assets and guaranteed enforcement of access policies without manual auditing.

### 3.3 Role-based access
   - **Junior Researcher**: Can run `mono create` and `prjsetup`. Has Read/Write access to their own projects. Can view the Registry but cannot approve global policy changes.
   - **Senior Research Reviewer**: Has Read-only access to `prj__` repositories to review outputs.
   - **Data Infrastructure Admin**: Has Admin access to the Registry Repository. Can merge Pull Requests that alter access policies and update infrastructure templates.

## 4. Functional requirements
   - **CLI Scaffolding** (Priority: High)
     - Generate directory trees for `data_` (products), `prj__` (analysis), and `infra_` (tooling).
     - Render templates for `README.md`, `metadata.json`, and `.gitignore`.
   - **Git & DVC Initialization** (Priority: High)
     - Initialize local Git repositories.
     - Initialize DVC and configure the remote to specific Wasabi S3 buckets (`s3://bucket/{project_name}`).
   - **Registry Integration (GitOps)** (Priority: High)
     - Automatically generate a metadata YAML file upon project creation.
     - Create a Pull Request to the central `data-commons-registry` repo to register the new asset.
   - **Stata Wrapper (`prjsetup`)** (Priority: High)
     - A native Stata command that wraps the Python CLI, allowing creation of projects directly from the Stata console.
   - **Access Policy Enforcement** (Priority: High)
     - Backend logic (GitHub Action) to sync the permissions defined in the Registry YAML with actual GitHub Repository Team permissions.

## 5. User experience

### 5.1. Entry points & first-time user flow
   - **Python CLI**: Users install via `pip install mono`. First run triggers `mono config` to set up personal access tokens.
   - **Stata**: Users install via `ssc install mono` (or local net install). The command `prjsetup` detects if the Python package is missing and prompts to install it.

### 5.2. Core experience
   - **Create Project**:
     - User types `prjsetup, type(data) name(medicare_2024)` in Stata.
     - System displays a spinner: "Scaffolding folders... Initializing DVC... Registering with Data Commons..."
     - System returns: "Success! Project created at ./data_medicare_2024. URL: github.com/org/data_medicare_2024".
     - User immediately begins work in the created folder.

### 5.3. Advanced features & edge cases
   - **Offline Mode**: If the Registry is unreachable, the tool scaffolds locally and warns the user to run `mono register` later.
   - **Naming Conflicts**: If a project name already exists in the Registry, the CLI prompts the user to choose a different name or import the existing project.

### 5.4. UI/UX highlights
   - **Minimalist Feedback**: Success messages provide direct clickable links to the Repo and the Registry entry.
   - **Stata-Native Feel**: The Stata wrapper uses standard Stata syntax and error reporting, hiding the Python complexity completely.

## 6. Narrative
Sarah is a Junior Researcher who needs to start analyzing 2024 Medicare claims. In the past, she would copy-paste an old folder, struggle with S3 credentials, and eventually lose track of which data version she used. With `mono`, she simply opens Stata and types `prjsetup, type(data) name(medicare_24)`. Within 30 seconds, her folder is created with a standard structure, DVC is ready to track her large files, and the project is automatically registered in the lab's central catalog. She doesn't need to read a wiki or ask an admin for permissions—she just gets to work. Later, her Senior Reviewer can easily find her output tables because the folder structure is exactly the same as every other project in the lab.

## 7. Success metrics

### 7.1. User-centric metrics
   - **Adoption Rate**: % of new projects created using `mono` vs. manual creation (Target: >90% within 3 months).
   - **Time-to-Start**: Average time from intent to "ready to code" (Target: < 2 minutes).

### 7.2. Business metrics
   - **Registry Completeness**: % of active repositories that have a corresponding entry in the Data Commons Registry.
   - **Support Ticket Reduction**: Decrease in "I can't access this data" or "Where is the repo?" inquiries to the Admin.

### 7.3. Technical metrics
   - **Registration Success Rate**: % of `mono create` executions that successfully merge a PR to the Registry.
   - **Policy Sync Latency**: Time between Registry update and GitHub permission application (Target: < 5 minutes).

## 8. Technical considerations

### 8.1. Integration points
   - **GitHub API**: Used via `PyGithub` for creating repos and opening Registry PRs.
   - **Wasabi S3**: Used for DVC remote storage.
   - **Local Stata Integration**: Requires Python integration (`pystata` or shell calls) within Stata.

### 8.2. Data storage & privacy
   - **Metadata**: Stored in the private `data-commons-registry` GitHub repo (YAML format).
   - **Data Files**: Stored in private Wasabi S3 buckets; never committed to Git.
   - **Credentials**: User tokens stored securely in local OS keychain or environment variables; never hardcoded in the package.

### 8.3. Scalability & performance
   - **Async Registration**: The "Registration" step opens a PR but does not block the user from working locally if the network is slow.
   - **DVC**: Handles TB-scale datasets efficiently, decoupling data size from Git repo size.

### 8.4. Potential challenges
   - **Stata Python Path**: Ensuring Stata can find the correct Python environment where `mono` is installed.
   - **Rate Limits**: Hitting GitHub API rate limits during bulk operations (mitigated by using GitHub App tokens for the backend).

## 9. Milestones & sequencing

### 9.1. Project estimate
   - **Medium**: 4-6 weeks for MVP release.

### 9.2. Team size & composition
   - **Small Team**: 1-3 people
     - 1 Lead Engineer (Python/DevOps/GitOps)
     - 1 Stata Specialist (Consultant/Internal User) to refine the `.ado` wrapper.
     - 1 Product Owner (Data Admin) for requirements and testing.

### 9.3. Suggested phases
   - **Phase 1**: Core Python CLI & Registry Logic (2 weeks)
     - Key deliverables: `mono` Python package, templates, GitOps registration flow, GitHub App setup.
   - **Phase 2**: Stata Integration & Docs (2 weeks)
     - Key deliverables: `prjsetup.ado` command, Stata help files, installation guide.
   - **Phase 3**: Beta Rollout & Training (1-2 weeks)
     - Key deliverables: Workshop for Junior Researchers, internal "Gold Standard" repo examples.

## 10. User stories

### 10.1. Initialize Data Project (Python)
   - **ID**: US-001
   - **Description**: As a Data Engineer, I want to create a new data project via the CLI so that the standard directory structure and DVC remotes are configured automatically.
   - **Acceptance criteria**:
     - Command `mono create data --name {name}` creates the folder structure.
     - `dvc status` shows the remote is configured to `s3://bucket/{name}`.
     - A `metadata.json` file is populated with the project name and creator.

### 10.2. Initialize Data Project (Stata)
   - **ID**: US-002
   - **Description**: As a Junior Researcher, I want to set up a new project directly from Stata so that I don't have to use the terminal.
   - **Acceptance criteria**:
     - Running `prjsetup, type(prj) name(analysis_1)` in Stata creates the project.
     - Stata Output window confirms success and prints the path.
     - The underlying Python command handles all errors gracefully and reports them back to Stata.

### 10.3. Automated Registry Registration
   - **ID**: US-003
   - **Description**: As a Data Admin, I want every new project to automatically open a PR to the Registry so that I can maintain a central catalog without manual data entry.
   - **Acceptance criteria**:
     - Upon `mono create`, a new branch is created in `data-commons-registry`.
     - A YAML file `{project_name}.yaml` is added to the `/catalog` folder.
     - A Pull Request is opened with the title "Register: {project_name}".

### 10.4. Secure Access Enforcement
   - **ID**: US-004
   - **Description**: As a Security Officer, I want project access to be managed by the Registry's YAML files so that permissions are auditable and strictly enforced.
   - **Acceptance criteria**:
     - When the Registry PR is merged, a GitHub Action triggers.
     - The Action reads the `access_control` section of the YAML.
     - The Action updates the actual GitHub Repository settings to match the teams defined (e.g., adding `health-econ-team` as Readers).
