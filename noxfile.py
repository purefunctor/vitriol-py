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
