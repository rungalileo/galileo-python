from platform import system

from invoke.context import Context
from invoke.tasks import task

# Disable `pty` on Windows to avoid issues with subprocesses.
# https://github.com/pyinvoke/invoke/issues/561
COMMON_PARAMS = dict(echo=True, pty=not system().lower().startswith("win"))


@task
def install(ctx: Context) -> None:
    ctx.run("poetry install --all-extras --no-root", **COMMON_PARAMS)


@task
def setup(ctx: Context) -> None:
    install(ctx)
    ctx.run("poetry run pre-commit install --hook-type pre-commit", **COMMON_PARAMS)


@task
def test_report_xml(ctx: Context) -> None:
    ctx.run("poetry run pytest -vvv --cov=galileo --cov-report=xml", **COMMON_PARAMS)


@task
def test(ctx: Context) -> None:
    ctx.run("poetry run pytest --cov=galileo --cov-report=term-missing", **COMMON_PARAMS)


@task
def type_check(ctx: Context) -> None:
    ctx.run(
        "poetry run mypy --package galileo "
        # TODO: remove as soon as mypy errors fixed
        "--exclude galileo.resources "
        "--exclude galileo.openai "
        "--exclude galileo.decorator "
        "--exclude galileo.handlers.langchain "
        "--exclude galileo.log_streams "
        "--exclude galileo.logger "
        "--exclude galileo.api_client "
        "--namespace-packages",
        **COMMON_PARAMS,
    )


@task
def poetry_lock(ctx: Context) -> None:
    """
    Update poetry.lock file.

    Parameters
    ----------
    ctx : Context
        Invoke context.
    """
    ctx.run("poetry lock", **COMMON_PARAMS)
