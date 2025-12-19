*! version 1.0.0
*! mint - Lab Project Scaffolding Tool
*! Native Python integration for Stata 16+

program define prjsetup
    version 16.0
    syntax, Type(string) Name(string) [Path(string) NOGit NODvc Bucket(string)]

    * Validate type
    if !inlist("`type'", "data", "project", "prj", "infra") {
        display as error "Invalid type. Use: data, project, or infra"
        exit 198
    }

    * Normalize "prj" to "project"
    if "`type'" == "prj" {
        local type "project"
    }

    * Set default path to current directory
    if "`path'" == "" {
        local path "`c(pwd)'"
    }

    * Convert Stata options to Python values
    local py_nogit = cond("`nogit'" != "", "True", "False")
    local py_nodvc = cond("`nodvc'" != "", "True", "False")
    local py_bucket = cond("`bucket'" != "", "`bucket'", "None")

    display as text "Creating project..."

    * Call Python directly using native integration
    python: _prjsetup_create("`type'", "`name'", "`path'", `py_nogit', `py_nodvc', "`py_bucket'")

end

python:
def _prjsetup_create(project_type, name, path, no_git, no_dvc, bucket):
    """Create project using mint Python package."""
    from sfi import Macro, SFIToolkit

    try:
        from mint import create_project

        # Convert string booleans to Python booleans
        init_git = no_git != "True"
        init_dvc = no_dvc != "True"

        # Handle bucket parameter
        bucket_name = bucket if bucket != "None" else None

        result = create_project(
            project_type=project_type,
            name=name,
            path=path,
            init_git=init_git,
            init_dvc=init_dvc,
            bucket_name=bucket_name
        )

        SFIToolkit.displayln("{result}Project created: " + result.full_name + "{reset}")
        SFIToolkit.displayln("{text}Location: " + str(result.path) + "{reset}")

        # Store result path in Stata macro for programmatic use
        Macro.setLocal("project_path", str(result.path))

    except ImportError:
        SFIToolkit.errprintln("Error: mint package not installed.")
        SFIToolkit.errprintln("Install with: pip install mint")
        SFIToolkit.exit(198)

    except Exception as e:
        SFIToolkit.errprintln(f"Error creating project: {e}")
        SFIToolkit.exit(198)
end