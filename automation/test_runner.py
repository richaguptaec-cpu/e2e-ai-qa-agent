import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATED_TESTS_DIR = (
    PROJECT_ROOT / "generated_tests"
)


def run_pytest(
    test_file,
    reviewed=False,
    base_url="https://www.saucedemo.com/",
    username="",
    password="",
    timeout=120
):
    """
    Run a reviewed generated test file with Pytest.

    This runner is intended for local development and
    authorized practice environments. It is not a sandbox.
    """

    if not reviewed:
        raise PermissionError(
            "Review and approve the generated code "
            "before executing it."
        )

    requested_path = Path(test_file).resolve()
    allowed_directory = GENERATED_TESTS_DIR.resolve()

    if requested_path.parent != allowed_directory:
        raise ValueError(
            "Only test files directly inside generated_tests "
            "can be executed."
        )

    if not requested_path.is_file():
        raise FileNotFoundError(
            f"Generated test file not found: {requested_path}"
        )

    if not requested_path.name.startswith("test_"):
        raise ValueError(
            "The test filename must start with 'test_'."
        )

    if requested_path.suffix != ".py":
        raise ValueError(
            "Only Python test files can be executed."
        )

    env = os.environ.copy()

    env["SAUCEDEMO_BASE_URL"] = base_url.strip()
    env["SAUCEDEMO_USERNAME"] = username
    env["SAUCEDEMO_PASSWORD"] = password

    command = [
        sys.executable,
        "-m",
        "pytest",
        str(requested_path),
        "-q",
        "--disable-warnings",
        "--tb=short",
    ]

    try:
        completed = subprocess.run(
            command,
            cwd=str(PROJECT_ROOT),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
            check=False,
        )

        output = (
            completed.stdout
            + "\n"
            + completed.stderr
        ).strip()

        return {
            "status": (
                "passed"
                if completed.returncode == 0
                else "failed"
            ),
            "return_code": completed.returncode,
            "output": output,
            "timed_out": False,
        }

    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""

        if isinstance(stdout, bytes):
            stdout = stdout.decode(
                "utf-8",
                errors="replace"
            )

        if isinstance(stderr, bytes):
            stderr = stderr.decode(
                "utf-8",
                errors="replace"
            )

        return {
            "status": "timed_out",
            "return_code": None,
            "output": (
                str(stdout)
                + "\n"
                + str(stderr)
                + f"\nTest execution exceeded {timeout} seconds."
            ).strip(),
            "timed_out": True,
        }