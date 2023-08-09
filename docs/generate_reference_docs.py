from __future__ import annotations

import logging
import subprocess
import json
import textwrap
from pathlib import Path
from typing import Any, cast

import mkdocs_gen_files
import jinja2

logger = logging.getLogger(__name__)

def run_pants_help_all() -> dict[str, Any]:
    # List all (stable enough) backends here.
    backends = [
        "pants.backend.build_files.fix.deprecations",
        "pants.backend.build_files.fmt.black",
        "pants.backend.build_files.fmt.buildifier",
        "pants.backend.build_files.fmt.yapf",
        "pants.backend.awslambda.python",
        "pants.backend.codegen.protobuf.lint.buf",
        "pants.backend.codegen.protobuf.python",
        "pants.backend.codegen.thrift.apache.python",
        "pants.backend.docker",
        "pants.backend.docker.lint.hadolint",
        "pants.backend.experimental.adhoc",
        "pants.backend.experimental.codegen.protobuf.go",
        "pants.backend.experimental.codegen.protobuf.java",
        "pants.backend.experimental.codegen.protobuf.scala",
        "pants.backend.experimental.go",
        "pants.backend.experimental.helm",
        "pants.backend.experimental.java",
        "pants.backend.experimental.java.lint.google_java_format",
        "pants.backend.experimental.kotlin",
        "pants.backend.experimental.kotlin.lint.ktlint",
        "pants.backend.experimental.openapi",
        "pants.backend.experimental.openapi.lint.spectral",
        "pants.backend.experimental.python",
        "pants.backend.experimental.python.framework.stevedore",
        "pants.backend.experimental.python.lint.add_trailing_comma",
        "pants.backend.experimental.python.lint.autoflake",
        "pants.backend.experimental.python.lint.pyupgrade",
        "pants.backend.experimental.python.packaging.pyoxidizer",
        "pants.backend.experimental.scala",
        "pants.backend.experimental.scala.lint.scalafmt",
        "pants.backend.experimental.terraform",
        "pants.backend.experimental.tools.workunit_logger",
        "pants.backend.experimental.tools.yamllint",
        "pants.backend.google_cloud_function.python",
        "pants.backend.plugin_development",
        "pants.backend.python",
        "pants.backend.python.lint.bandit",
        "pants.backend.python.lint.black",
        "pants.backend.python.lint.docformatter",
        "pants.backend.python.lint.flake8",
        "pants.backend.python.lint.isort",
        "pants.backend.python.lint.pydocstyle",
        "pants.backend.python.lint.pylint",
        "pants.backend.python.lint.yapf",
        "pants.backend.python.mixed_interpreter_constraints",
        "pants.backend.python.typecheck.mypy",
        "pants.backend.python.typecheck.pytype",
        "pants.backend.shell",
        "pants.backend.shell.lint.shellcheck",
        "pants.backend.shell.lint.shfmt",
        "pants.backend.tools.preamble",
    ]
    argv = [
        "./pants",
        "--concurrent",
        "--plugins=[]",
        f"--backend-packages={repr(backends)}",
        "--no-verify-config",
        "help-all",
    ]
    run = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    try:
        run.check_returncode()
    except subprocess.CalledProcessError:
        logger.error(
            textwrap.dedent(
                f"""
                Running {argv} failed with exit code {run.returncode}.

                stdout:
                {textwrap.indent(run.stdout, " " * 4)}

                stderr:
                {textwrap.indent(run.stderr, " " * 4)}
                """
            )
        )
        raise
    with open("foo.json", "w") as f:
        f.write(run.stdout)
    return cast("dict[str, Any]", json.loads(run.stdout))


env = jinja2.Environment(
    loader = jinja2.FileSystemLoader("docs/reference_templates"),
    autoescape=False,
)
template = env.get_template("options.md")

print("=== Getting `./pants help-all` ===")
#help_info = run_pants_help_all()
with open("help-all.json") as f:
    help_info = json.load(f)

help_infos = help_info["scope_to_help_info"].values()
for info in help_infos:
    filename = (info["scope"] or "global-options")
    if info["is_goal"]:
        with mkdocs_gen_files.open(f"reference/{filename}.md", "w") as f:
            print(template.render(**info), file=f)
        # mkdocs_gen_files.Nav["reference", ""]