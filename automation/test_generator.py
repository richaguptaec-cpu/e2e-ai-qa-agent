import ast
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATED_TESTS_DIR = PROJECT_ROOT / "generated_tests"

ALLOWED_IMPORTS = {
    "os",
    "pytest",
    "playwright",
}

FORBIDDEN_NAMES = {
    "eval",
    "exec",
    "compile",
    "__import__",
    "breakpoint",
}

FORBIDDEN_ATTRIBUTES = {
    "system",
    "popen",
    "remove",
    "unlink",
    "rmdir",
    "rmtree",
}


def validate_generated_code(code):
    """
    Perform basic static checks on generated Python code.

    These checks reduce obvious risks but do not make
    arbitrary Python code safe to execute.
    """

    if not isinstance(code, str) or not code.strip():
        raise ValueError("Generated Python code is empty.")

    try:
        syntax_tree = ast.parse(code)
    except SyntaxError as exc:
        raise ValueError(
            f"Generated Python has a syntax error: {exc}"
        ) from exc

    test_functions = [
        node
        for node in ast.walk(syntax_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
    ]

    if not test_functions:
        raise ValueError(
            "The generated file must contain at least "
            "one function whose name starts with 'test_'."
        )

    for node in ast.walk(syntax_tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_module = alias.name.split(".")[0]

                if root_module not in ALLOWED_IMPORTS:
                    raise ValueError(
                        f"Disallowed import: {alias.name}"
                    )

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            root_module = module.split(".")[0]

            if root_module not in ALLOWED_IMPORTS:
                raise ValueError(
                    f"Disallowed import: {module}"
                )

        elif isinstance(node, ast.Name):
            if node.id in FORBIDDEN_NAMES:
                raise ValueError(
                    f"Disallowed Python operation: {node.id}"
                )

        elif isinstance(node, ast.Attribute):
            if node.attr in FORBIDDEN_ATTRIBUTES:
                raise ValueError(
                    "Disallowed operation detected: "
                    + node.attr
                )

    return True


def save_generated_test(code, filename="test_generated.py"):
    """
    Validate and save one generated test under generated_tests.

    Returns the saved file's absolute path.
    """

    if not re.fullmatch(
        r"test_[A-Za-z0-9_]+\.py",
        filename
    ):
        raise ValueError(
            "Filename must use the pattern "
            "'test_<name>.py'."
        )

    validate_generated_code(code)

    GENERATED_TESTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = (
        GENERATED_TESTS_DIR / filename
    ).resolve()

    if file_path.parent != GENERATED_TESTS_DIR.resolve():
        raise ValueError(
            "The generated file must remain inside "
            "the generated_tests directory."
        )

    file_path.write_text(
        code,
        encoding="utf-8"
    )

    return file_path