from invoke.context import Context
from invoke.tasks import task


@task
def install(ctx: Context) -> None:
    ctx.run("poetry install --all-extras --without docs --no-root", echo=True)


@task
def setup(ctx: Context) -> None:
    install(ctx)
    ctx.run("poetry run pre-commit install --hook-type pre-commit", echo=True)


@task
def test_report_xml(ctx: Context) -> None:
    ctx.run("poetry run pytest -vvv --cov=galileo --cov-report=xml", echo=True)


@task
def test(ctx: Context) -> None:
    ctx.run("poetry run pytest --cov=galileo --cov-report=term-missing", echo=True)


@task
def type_check(ctx: Context) -> None:
    ctx.run("poetry run mypy --package galileo --exclude galileo.resources --namespace-packages", echo=True)


@task
def docs_build(ctx: Context) -> None:
    ctx.run("poetry run mkdocs build --verbose", echo=True)
