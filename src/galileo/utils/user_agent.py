"""User-Agent generation utilities for the Galileo SDK."""

import sys


def _get_package_version() -> str:
    """Get the package version dynamically to avoid circular imports."""
    try:
        from importlib.metadata import version

        return version("galileo")
    except ImportError:
        # Fallback approach if importlib.metadata fails
        try:
            import pkg_resources

            return pkg_resources.get_distribution("galileo").version
        except ImportError:
            # Final fallback - empty string if version cannot be determined
            return ""


def get_default_user_agent() -> str:
    """Generate a default User-Agent header for the SDK."""
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    package_version = _get_package_version()

    # Handle empty version gracefully
    if package_version:
        return f"galileo-python-sdk/{package_version} (Python {python_version})"
    else:
        return f"galileo-python-sdk (Python {python_version})"


def get_default_headers() -> dict[str, str]:
    """Get default headers including User-Agent for API requests."""
    return {"User-Agent": get_default_user_agent()}
