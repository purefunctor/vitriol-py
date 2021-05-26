import tempfile

import nox


def install_with_constraints(session, *args, **kwargs):
    """
    https://cjolowicz.github.io/posts/hypermodern-python-03-linting/
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            "--without-hashes",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session
def lint(session):
    install_with_constraints(session, "pre-commit")
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python=["3.9"])
def test(session):
    env = {"COVERAGE_FILE": f".coverage.{session.python}"}

    install_with_constraints(session, "pytest", "coverage[toml]")
    session.install(".")
    session.run("coverage", "run", "--branch", "-m", "pytest", "-vs", env=env)
    session.run("coverage", "report", "-m", env=env)
