# fmt: off
# CRITICAL: Set test environment variables BEFORE any other imports.
# This MUST be at the absolute top of conftest.py before any import statements.
# Required for pytest-xdist compatibility on Python 3.14+.
#
# NOTE: We unconditionally override these vars (not setdefault) to ensure:
# 1. Tests never accidentally use real credentials from developer's environment
# 2. Test isolation - all tests see the same predictable values
# 3. Security - prevents real API keys from leaking into test logs
import os

os.environ["GALILEO_CONSOLE_URL"] = "http://localtest:8088"
os.environ["GALILEO_API_KEY"] = "api-1234567890"
os.environ["GALILEO_PROJECT"] = "test-project"
os.environ["GALILEO_LOG_STREAM"] = "test-log-stream"
# fmt: on
