#!/usr/bin/env python3
"""
Debug script for SSL/TLS issues with Galileo SDK.

This script helps diagnose SSL certificate verification issues when connecting
to the Galileo API.

Usage:
    # Enable debug logging and run basic tests
    GALILEO_LOG_LEVEL=DEBUG python debug_ssl.py

    # Test with SSL disabled (NOT recommended for production)
    GALILEO_SSL_CONTEXT=False GALILEO_LOG_LEVEL=DEBUG python debug_ssl.py

    # Test with custom CA bundle
    SSL_CERT_FILE=/path/to/ca-bundle.crt GALILEO_LOG_LEVEL=DEBUG python debug_ssl.py
"""

import logging
import os
import ssl
import sys
from urllib.parse import urlparse

# Set up logging BEFORE importing galileo modules
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stderr,
)

# Enable debug logging for all relevant loggers
for logger_name in ["galileo", "galileo_core", "httpx", "httpcore"]:
    logging.getLogger(logger_name).setLevel(logging.DEBUG)


def print_section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print("=" * 60)


def check_environment() -> None:
    """Check environment variables related to SSL."""
    print_section("Environment Variables")
    
    ssl_vars = [
        "GALILEO_CONSOLE_URL",
        "GALILEO_API_URL",
        "GALILEO_API_KEY",
        "GALILEO_LOG_LEVEL",
        "GALILEO_SSL_CONTEXT",
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
        "REQUESTS_CA_BUNDLE",
        "CURL_CA_BUNDLE",
        "HTTPS_PROXY",
        "HTTP_PROXY",
        "NO_PROXY",
    ]
    
    for var in ssl_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            if "KEY" in var or "TOKEN" in var:
                display_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
            else:
                display_value = value
            print(f"  {var}={display_value}")
        else:
            print(f"  {var}=(not set)")


def check_python_ssl() -> None:
    """Check Python's SSL configuration."""
    print_section("Python SSL Configuration")
    
    print(f"  Python version: {sys.version}")
    print(f"  SSL library: {ssl.OPENSSL_VERSION}")
    print(f"  SSL version: {ssl.OPENSSL_VERSION_NUMBER}")
    
    # Check default CA certificates
    try:
        import certifi
        print(f"  certifi CA bundle: {certifi.where()}")
    except ImportError:
        print("  certifi: (not installed)")
    
    # Check system CA paths
    default_context = ssl.create_default_context()
    print(f"  Default verify mode: {default_context.verify_mode}")
    print(f"  Check hostname: {default_context.check_hostname}")


def test_raw_ssl_connection(url: str) -> bool:
    """Test raw SSL connection to a URL."""
    print_section(f"Raw SSL Test to {url}")
    
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    
    if parsed.scheme != "https":
        print(f"  Skipping SSL test for non-HTTPS URL: {url}")
        return True
    
    import socket
    
    try:
        # Test with default SSL context
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                print(f"  ✅ SSL connection successful!")
                print(f"     Cipher: {ssock.cipher()}")
                print(f"     Version: {ssock.version()}")
                cert = ssock.getpeercert()
                if cert:
                    print(f"     Subject: {cert.get('subject', 'N/A')}")
                    print(f"     Issuer: {cert.get('issuer', 'N/A')}")
                    print(f"     Not After: {cert.get('notAfter', 'N/A')}")
                return True
    except ssl.SSLCertVerificationError as e:
        print(f"  ❌ SSL Certificate Verification Error: {e}")
        print(f"     This typically means:")
        print(f"     - The server's certificate is not trusted by your system")
        print(f"     - The certificate chain is incomplete")
        print(f"     - Self-signed certificate without proper CA setup")
        return False
    except ssl.SSLError as e:
        print(f"  ❌ SSL Error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Connection Error: {type(e).__name__}: {e}")
        return False


def test_httpx_connection(url: str, verify: bool = True) -> bool:
    """Test httpx connection."""
    print_section(f"HTTPX Test to {url} (verify={verify})")
    
    try:
        import httpx
        
        with httpx.Client(verify=verify, timeout=30.0) as client:
            response = client.get(url)
            print(f"  ✅ HTTPX request successful!")
            print(f"     Status: {response.status_code}")
            print(f"     Headers: {dict(response.headers)}")
            return True
    except httpx.ConnectError as e:
        print(f"  ❌ Connection Error: {e}")
        if "SSL" in str(e) or "certificate" in str(e).lower():
            print("     This is an SSL/certificate error.")
        return False
    except Exception as e:
        print(f"  ❌ Error: {type(e).__name__}: {e}")
        return False


def test_galileo_config() -> bool:
    """Test Galileo configuration initialization."""
    print_section("Galileo Config Test")
    
    console_url = os.environ.get("GALILEO_CONSOLE_URL")
    api_key = os.environ.get("GALILEO_API_KEY")
    
    if not console_url:
        print("  ⚠️ GALILEO_CONSOLE_URL not set, skipping Galileo config test")
        return False
    
    if not api_key:
        print("  ⚠️ GALILEO_API_KEY not set, skipping Galileo config test")
        return False
    
    try:
        # Import after logging is set up
        from galileo_core.schemas.base_config import GalileoConfig
        
        print("  Initializing GalileoConfig...")
        config = GalileoConfig.get()
        
        print(f"  ✅ GalileoConfig initialized!")
        print(f"     Console URL: {config.console_url}")
        print(f"     API URL: {config.api_url}")
        print(f"     SSL Context: {config.ssl_context}")
        print(f"     SSL Context Type: {type(config.ssl_context).__name__}")
        
        return True
    except Exception as e:
        print(f"  ❌ Config initialization failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_list_api_keys() -> bool:
    """Test list_api_keys function."""
    print_section("list_api_keys() Test")
    
    console_url = os.environ.get("GALILEO_CONSOLE_URL")
    api_key = os.environ.get("GALILEO_API_KEY")
    
    if not console_url or not api_key:
        print("  ⚠️ GALILEO_CONSOLE_URL or GALILEO_API_KEY not set, skipping")
        return False
    
    try:
        from galileo import list_api_keys
        
        print("  Calling list_api_keys()...")
        keys = list_api_keys()
        
        print(f"  ✅ list_api_keys() succeeded!")
        print(f"     Found {len(keys)} API key(s)")
        return True
    except Exception as e:
        print(f"  ❌ list_api_keys() failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main() -> None:
    """Run all debug checks."""
    print("\n" + "=" * 60)
    print(" Galileo SDK SSL Debug Tool")
    print("=" * 60)
    
    check_environment()
    check_python_ssl()
    
    # Test raw SSL if we have a console URL
    console_url = os.environ.get("GALILEO_CONSOLE_URL")
    if console_url:
        # Derive API URL
        if "localhost" in console_url or "127.0.0.1" in console_url:
            api_url = "http://localhost:8088"
        elif "app.galileo.ai" in console_url:
            api_url = "https://api.galileo.ai"
        else:
            api_url = console_url.replace("console", "api")
        
        test_raw_ssl_connection(api_url)
        test_httpx_connection(f"{api_url}/healthcheck", verify=True)
        
        # Test with verify=False to see if it's a cert issue
        print("\n  Testing with verify=False to isolate cert issue...")
        test_httpx_connection(f"{api_url}/healthcheck", verify=False)
    
    test_galileo_config()
    test_list_api_keys()
    
    print_section("Summary & Recommendations")
    print("""
If you're seeing SSL errors, try these solutions:

1. **Custom CA Bundle** (most common for enterprise deployments):
   export SSL_CERT_FILE=/path/to/your/ca-bundle.crt
   export GALILEO_LOG_LEVEL=DEBUG
   python your_script.py

2. **Disable SSL verification** (NOT recommended for production):
   export GALILEO_SSL_CONTEXT=False
   python your_script.py
   
   Or in code:
   from galileo_core.schemas.base_config import GalileoConfig
   config = GalileoConfig.get(ssl_context=False)

3. **Check if behind a proxy**:
   - Enterprise proxies often do SSL interception
   - You may need to add the proxy's CA to your bundle

4. **Check network connectivity**:
   - Ensure you can reach the API URL from your machine
   - Check firewall rules

For more details, see the debug output above.
""")


if __name__ == "__main__":
    main()

