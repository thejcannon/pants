# Copyright 2017 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_sources(dependencies=[":plugins"])

# NOTE: When adding a new backend, add it to `generate_docs.py` too! (If stable enough for docs)
target(
    name="plugins",
    dependencies=[
        "src/python/pants/backend/experimental/python",
        "src/python/pants/backend/experimental/python/lint/autoflake",
        "src/python/pants/backend/plugin_development",
        "src/python/pants/backend/project_info",
        "src/python/pants/backend/python",
        "src/python/pants/backend/python/lint/black",
        "src/python/pants/backend/python/lint/docformatter",
        "src/python/pants/backend/python/lint/flake8",
        "src/python/pants/backend/python/lint/isort",
        "src/python/pants/backend/python/mixed_interpreter_constraints",
        "src/python/pants/backend/python/typecheck/mypy",
        "src/python/pants/backend/shell",
        "src/python/pants/core",
    ],
)

python_tests(name="tests", timeout=240)
