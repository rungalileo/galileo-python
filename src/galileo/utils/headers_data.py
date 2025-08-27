try:
    # Python 3.8+
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    # Python < 3.8
    from importlib_metadata import PackageNotFoundError, version  # type: ignore[no-redef]


def get_package_version() -> str:
    """Get the package version of galileo."""
    try:
        return version("galileo")
    except PackageNotFoundError:
        return ""
