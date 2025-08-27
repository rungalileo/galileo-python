from importlib.metadata import PackageNotFoundError, version


def get_package_version() -> str:
    """Get the package version of galileo."""
    try:
        return version("galileo")
    except PackageNotFoundError:
        return ""
