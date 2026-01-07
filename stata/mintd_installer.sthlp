{smcl}
{* *! version 1.0.0}{...}
{vieweralsosee "[R] net" "help net"}{...}
{vieweralsosee "mintd" "help mintd"}{...}
{viewerjumpto "Syntax" "mintd_installer##syntax"}{...}
{viewerjumpto "Description" "mintd_installer##description"}{...}
{viewerjumpto "Options" "mintd_installer##options"}{...}
{viewerjumpto "Examples" "mintd_installer##examples"}{...}
{viewerjumpto "Remarks" "mintd_installer##remarks"}{...}
{title:Title}

{p2colset 5 20 22 2}{...}
{p2col :{manlink R mintd_installer} {hline 2}}Automated installation of the mintd package{p_end}
{p2colreset}{...}

{marker syntax}{...}
{title:Syntax}

{p 8 16 2}
{cmd:mintd_installer} [, {opt force} {opt replace} {opt from(url)} {opt pythonpath(path)} {opt novenv} {opt github} ]

{marker description}{...}
{title:Description}

{pstd}
{cmd:mintd_installer} provides automated installation of the complete mintd package,
including both the Stata commands and the required Python package. This installer
handles the installation process in two steps:

{p 4 4 2}
1. Installs the Stata package files ({cmd:mintd.ado}, {cmd:mintd.sthlp})
{p_end}
{p 4 4 2}
2. Installs the Python {cmd:mintd} package in Stata's Python environment
{p_end}

{pstd}
The installer will attempt to install the Python package from GitHub or local
source directory. PyPI installation is not supported.

{marker options}{...}
{title:Options}

{phang}
{opt force} forces reinstallation even if mintd appears to be already installed.

{phang}
{opt replace} passes the {opt replace} option to {cmd:net install} for the Stata package.

{phang}
{opt from(url)} specifies the URL to install the Stata package from.
Default is "{browse "https://github.com/Cooper-lab/mint/raw/main/stata/":https://github.com/Cooper-lab/mint/raw/main/stata/}".

{phang}
{opt pythonpath(path)} specifies the path to the {it:local} mintd Python package source
directory on your machine. This must be a local directory path containing {cmd:pyproject.toml}
(not a GitHub URL). If not specified, the installer will attempt to find it automatically
based on the Stata installation location. Use this option if automatic detection fails or if
you want to install from a specific local source location.

{phang}
{opt novenv} skips virtual environment creation and installs mintd directly into
Stata's Python environment. By default, the installer creates a virtual environment
for mintd to avoid conflicts with other packages. If virtual environment creation fails,
the installer will throw an error - use {opt novenv} to install directly instead.

{phang}
{opt github} automatically clones the mint repository from GitHub into a temporary
directory and installs from the development version. Use this option to install the
latest development version without manually cloning the repository.

{marker examples}{...}
{title:Examples}

{phang}
Install mintd with default settings:

{p 8 12 2}
{cmd:. mintd_installer}

{phang}
Force reinstallation:

{p 8 12 2}
{cmd:. mintd_installer, force}

{phang}
Install from a custom location with local Python path:

{p 8 12 2}
{cmd:. mintd_installer, from("https://example.com/stata/") pythonpath("/path/to/mintd")}

{phang}
Install directly without virtual environment:

{p 8 12 2}
{cmd:. mintd_installer, novenv}

{phang}
Install from specific source directory:

{p 8 12 2}
{cmd:. mintd_installer, pythonpath("C:\Users\username\projects\mintd")}

{phang}
Install latest development version from GitHub:

{p 8 12 2}
{cmd:. mintd_installer, github}

{marker remarks}{...}
{title:Remarks}

{pstd}
This installer provides a convenient way to set up the complete mintd environment
without manual intervention. By default, it creates an isolated virtual environment
for mintd to avoid conflicts with other Python packages. It is particularly useful for:

{p 4 4 2}
• First-time installations
{p_end}
{p 4 4 2}
• Automated deployment scripts
{p_end}
{p 4 4 2}
• Development environment setup
{p_end}
{p 4 4 2}
• Clean package isolation via virtual environment
{p_end}

{pstd}
If the automated installation fails, you can still install the components manually:

{p 4 4 2}
1. Install Stata files: {cmd:net install mintd, from("https://github.com/Cooper-lab/mint/raw/main/stata/")}
{p_end}
{p 4 4 2}
2. Install Python package: {cmd:python: import subprocess; subprocess.run(["pip", "install", "mintd"])}
{p_end}

{title:Also see}

{psee}
{manhelp mintd R} - Create research projects using mintd
{p_end}
{psee}
{manhelp net R} - Install and manage Stata packages
{p_end}