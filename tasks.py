import re
import sys
from typing import Any, Optional

from invoke import Collection, Context, task  # type: ignore[attr-defined]


@task(aliases=["c"])
def clean(c: Context) -> None:
    """Clean up build artifacts."""
    c.run("echo 'Cleaning up build artifacts ...'")

    # Remove build artifact files
    c.run("find sos tests -name '*.pyc' -type f -delete")
    c.run("find sos tests -name '.coverage' -type f -delete")
    c.run("find sos tests -name 'junit.xml' -type f -delete")
    c.run("find sos tests -name '*.log' -type f -delete")

    # Remove build artifact directories
    c.run("find sos tests -name '*.egg-info' -type d -exec rm -r {} +")
    c.run("find sos tests -name '.mypy_cache' -type d -exec rm -r {} +")
    c.run("find sos tests -name '.pytest_cache' -type d -exec rm -r {} +")
    c.run("find sos tests -name '__pycache__' -type d -exec rm -r {} +")

    c.run("rm -f *.log junit.xml .coverage coverage.xml")
    c.run("rm -rf .tox/ dist/ build/ *.egg-info")

    # Clear the npm cache
    c.run("npm cache clean --force")


@task(aliases=["i"], pre=[clean], help={"prod": "Install production dependencies."})
def install(c: Context, prod: bool = False) -> None:
    """Install dependencies."""
    if prod:
        c.run("echo 'Installing dependencies ...'")
        c.run("pip install .")
    else:
        c.run("echo 'Installing development dependencies ...'")
        c.run("pip install -e .[dev]")



@task(aliases=["f"])
def format_code(c: Context) -> None:
    """Format code with black and isort."""
    c.run("echo 'Formatting code ...'")

    # Format code
    c.run("black sos/ tests/ tasks.py")

    # Sort imports
    c.run("isort sos/ tests/ tasks.py")


@task(aliases=["l"], pre=[format_code])
def lint(c: Context) -> None:
    """Run linters (flake8 and pylint)."""
    c.run("echo 'Analyzing Syntax ...'")
    c.run("flake8 sos/ tests/ tasks.py")
    c.run("pylint sos/ tests/ tasks.py")
    c.run("mypy sos/ tests/ tasks.py")


@task(aliases=["t"])
def test(c: Context) -> None:
    """Run tests."""
    c.run("echo 'Running tests ...'")
    c.run("pytest")


@task(aliases=["v"])
def coverage(c: Context) -> None:
    """Run tests with coverage."""
    c.run("echo 'Running tests with coverage ...'")
    c.run("pytest --cov=sos --cov-report=term-missing tests/")
    c.run("coverage report")
    c.run("coverage xml")


@task(aliases=["p"])
def package(c: Context) -> None:
    """Package the CLI tool."""
    c.run("echo 'Packaging the project ...'")
    c.run("python setup.py sdist bdist_wheel")


@task()
def run_all_tasks(c: Context) -> None:
    """Run all tasks."""
    lint(c)
    test(c)


@task(aliases=["b"])
def build(c: Context) -> None:
    """Build the package."""
    c.run("echo 'Building the package ...'")
    c.run("python -m build")


@task(aliases="r", pre=[clean, build])
def release(c: Context) -> None:
    """Release the package to PyPI."""
    c.run("echo 'Releasing the package ...'")
    c.run("twine upload dist/*")


@task(aliases=["cc"])
def check_complexity(c: Context, max_complexity: int = 10) -> None:
    """
    Check the cyclomatic complexity of the code.
    Fail if it exceeds the max_complexity.

    :param c: The context instance (automatically passed by invoke).
    :param ctx: The context instance (automatically passed by invoke).
    :param max_complexity: The maximum allowed cyclomatic complexity.
    """
    c.run("echo 'Checking cyclomatic complexity ...'")
    result = c.run("radon cc sos tests -s", hide=True)

    if result is None:
        print("No output from radon.")
        sys.exit(1)

    output = result.stdout
    results = parse_radon_output(output)
    display_radon_results(results)
    max_score = get_max_score(results)

    if max_score > max_complexity:
        print(f"\nFAILED - Maximum complexity exceeded: {max_score}\n")
        sys.exit(1)

    print(f"\nMaximum complexity not exceeded: {max_score}\n")

    sys.exit(0)


def get_max_score(results: dict[Optional[str], Any]) -> int:
    max_score = 0
    for _, functions in results.items():
        for function in functions:
            if function["score"] > max_score:
                max_score = function["score"]
    return max_score


def display_radon_results(results: dict[Optional[str], Any]) -> None:
    for file, functions in results.items():
        print(f"\nFile: {file}")
        for function in functions:
            print(
                f"\tFunction: {function['name']}, ",
                f"Complexity: {function['complexity']}, ",
                f"Score: {function['score']}",
            )


def parse_radon_output(output: str) -> dict[Optional[str], Any]:
    # Remove the escape sequence
    output = output.replace("\x1b[0m", "")

    # Regular expression to match the lines with complexity information
    pattern = re.compile(r"^\s*(\w)\s(\d+:\d+)\s([\w_]+)\s-\s([A-F])\s\((\d+)\)$")

    # Dictionary to store the results
    results: dict[Optional[str], Any] = {}

    # Split the output into lines
    output = output.strip()
    lines = output.splitlines()

    current_file = None
    for line in lines:
        try:
            # Check if the line is a file name
            if not line.startswith(" "):
                current_file = line.strip()
                results[current_file] = []
            else:
                # Match the line with the pattern
                match = pattern.match(line)
                if match:
                    function_info = {
                        "type": match.group(1),
                        "location": match.group(2),
                        "name": match.group(3),
                        "complexity": match.group(4),
                        "score": int(match.group(5)),
                    }
                    results[current_file].append(function_info)
        except ValueError as e:
            print(f"Error parsing line: '{line}'")
            print(e)

    return results


# Create a collection and set the default task
ns = Collection(
    clean,
    install,
    lint,
    test,
    build,
    coverage,
    format_code,
    package,
    run_all_tasks,
    check_complexity,
)
ns.configure({"run": {"echo": True}})
ns.default = "run_all_tasks"
