# Spec: Rename `GALILEO_*` Environment Variables to `SPLUNK_AO_*`

**Jira Tickets:** [HYBIM-713](https://splunk.atlassian.net/browse/HYBIM-713) · [HYBIM-716](https://splunk.atlassian.net/browse/HYBIM-716) · [HYBIM-727](https://splunk.atlassian.net/browse/HYBIM-727)  
**Status:** Draft / In Review  
**Author:** Aditya Mehra  
**Date:** 2026-06-04

---

> **Repository migration notice**  
> The changes in this PR are authored against the current `rungalileo/galileo-python` repository.  
> Once the Splunk Agent Observability (Splunk AO) project is formally open-sourced, this code will
> be re-homed to **[signalfx/splunk-ao-python](https://github.com/signalfx/splunk-ao-python)** on
> GitHub. A corresponding notice applies to the companion PRs:
> - `sdk-examples` → `signalfx/splunk-ao-python-examples`
> - `e2e-testing` → internal Splunk AO QA repo
>
> These PRs are opened now to facilitate early review. **Do not merge** until the migration is
> complete and the target repositories exist.

---

## 1. Background

The Galileo Python SDK is being rebranded as part of the **Splunk Agent Observability (Splunk AO)**
initiative. Environment variables currently prefixed with `GALILEO_` will be replaced with
`SPLUNK_AO_` to align with Splunk naming conventions and the new product identity.

Tickets in scope for this change:

| Ticket | Title |
|--------|-------|
| HYBIM-713 | Rename `GALILEO_API_KEY` → `SPLUNK_AO_API_KEY` |
| HYBIM-716 | Rename `GALILEO_PROJECT` / `GALILEO_LOG_STREAM` → `SPLUNK_AO_*` |
| HYBIM-727 | Rename remaining `GALILEO_*` env vars to `SPLUNK_AO_*` |

> **Out of scope:** `GALILEO_HEADER_PREFIX` — tracked separately as [HYBIM-729](https://splunk.atlassian.net/browse/HYBIM-729).

---

## 2. Scope of Changes

### 2.1 Environment Variable Mapping

| Old (`GALILEO_*`) | New (`SPLUNK_AO_*`) |
|-------------------|---------------------|
| `GALILEO_API_KEY` | `SPLUNK_AO_API_KEY` |
| `GALILEO_CONSOLE_URL` | `SPLUNK_AO_CONSOLE_URL` |
| `GALILEO_PROJECT` | `SPLUNK_AO_PROJECT` |
| `GALILEO_PROJECT_ID` | `SPLUNK_AO_PROJECT_ID` |
| `GALILEO_LOG_STREAM` | `SPLUNK_AO_LOG_STREAM` |
| `GALILEO_LOG_STREAM_ID` | `SPLUNK_AO_LOG_STREAM_ID` |
| `GALILEO_JWT_TOKEN` | `SPLUNK_AO_JWT_TOKEN` |
| `GALILEO_SSO_ID_TOKEN` | `SPLUNK_AO_SSO_ID_TOKEN` |
| `GALILEO_SSO_PROVIDER` | `SPLUNK_AO_SSO_PROVIDER` |
| `GALILEO_USERNAME` | `SPLUNK_AO_USERNAME` |
| `GALILEO_PASSWORD` | `SPLUNK_AO_PASSWORD` |
| `GALILEO_MODE` | `SPLUNK_AO_MODE` |
| `GALILEO_LOGGING_DISABLED` | `SPLUNK_AO_LOGGING_DISABLED` |
| `GALILEO_INGEST_BETA_DISABLED` | `SPLUNK_AO_INGEST_BETA_DISABLED` |

### 2.2 Compatibility Strategy

This is a **hard cut-over** — only `SPLUNK_AO_*` environment variables are supported after this
change. There is no backward-compatibility shim for external consumers.

**Exception — `galileo-core` bridge:**  
The `galileo-core` package (a private dependency) continues to read `GALILEO_*` variables
internally. Until `galileo-core` is updated (tracked separately), the SDK automatically bridges
`SPLUNK_AO_*` → `GALILEO_*` at startup via `GalileoPythonConfig._bridge_env_vars()`. This is a
transparent, temporary compatibility layer that does not expose `GALILEO_*` names to SDK consumers.

```python
# src/galileo/config.py — bridge called inside GalileoPythonConfig.get()
@staticmethod
def _bridge_env_vars() -> None:
    """Copy SPLUNK_AO_* values into GALILEO_* so galileo-core can authenticate.
    Only sets GALILEO_* if it is not already present — explicit overrides win.
    """
    _BRIDGE = [
        ("SPLUNK_AO_API_KEY",       "GALILEO_API_KEY"),
        ("SPLUNK_AO_CONSOLE_URL",   "GALILEO_CONSOLE_URL"),
        ("SPLUNK_AO_PROJECT",       "GALILEO_PROJECT"),
        ...
    ]
    for new_key, old_key in _BRIDGE:
        if new_key in os.environ and old_key not in os.environ:
            os.environ[old_key] = os.environ[new_key]
```

---

## 3. Files Changed

### `galileo-python` (this repo)

| File | Change |
|------|--------|
| `src/galileo/configuration.py` | 14 `ConfigKey.env_var` fields renamed |
| `src/galileo/config.py` | Auth validation + `_bridge_env_vars()` added |
| `src/galileo/utils/env_helpers.py` | `os.getenv()` calls updated |
| `src/galileo/utils/decorators/telemetry_toggle.py` | `GALILEO_LOGGING_DISABLED` renamed |
| `src/galileo/logger/logger.py` | `GALILEO_INGEST_BETA_DISABLED` renamed |
| `src/galileo/{agent_control,decorator,exceptions,experiment,experiments,log_stream,log_streams,metric,middleware/tracing,otel,projects,prompt,shared/exceptions,utils/singleton}.py` | Docstrings / comments / error strings updated |
| `src/galileo/README_API_CLIENT.md` | Docs updated |
| `tests/**` | All `GALILEO_*` references in test files renamed to `SPLUNK_AO_*` |

### `sdk-examples`

| File | Change |
|------|--------|
| `python/agent/langchain-agent/.env.example` | Renamed keys to `SPLUNK_AO_*` |
| `python/agent/langchain-agent/main.py` | `os.environ["GALILEO_*"]` → `os.environ["SPLUNK_AO_*"]` |
| `python/agent/strands-agents/.env.example` | Renamed keys to `SPLUNK_AO_*` |

### `e2e-testing`

| File | Change |
|------|--------|
| `py-sdk-and-ui/.env.example` | New file — `SPLUNK_AO_*` keys, no values |

---

## 4. Testing

### Unit Tests

```bash
cd galileo-python
poetry run pytest                # 2015 passed, 5 skipped
```

### E2E Tests

```bash
cd e2e-testing/py-sdk-and-ui
poetry run playwright install --with-deps
poetry run pytest tests/ -k "langchain" --headed
```

Result: all targeted tests passed (one pre-existing 404 on `test_log_session_with_multiple_traces`
is a server-side issue unrelated to this change).

### Examples

```bash
# langchain-agent
cd sdk-examples/python/agent/langchain-agent
source .venv/bin/activate && python main.py
# → "Hello, Erin! 👋"   exit 0

# strands-agents
cd sdk-examples/python/agent/strands-agents
source .venv/bin/activate && python agent.py
# → Tool results returned   exit 0
```

---

## 5. Decisions & Rationale

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backward compatibility | Hard cut-over | No dual-support maintenance burden; clean break aligned with rebrand |
| `galileo-core` handling | Bridge only in SDK | `galileo-core` changes tracked separately; bridge is transparent to consumers |
| `GALILEO_HEADER_PREFIX` | **Not renamed** | Separate ticket HYBIM-729 |
| Test files | Renamed to `SPLUNK_AO_*` | Consistency; tests document the new public API |

---

## 6. Open Questions / Follow-ups

- [ ] Update `galileo-core` to read `SPLUNK_AO_*` natively and remove `_bridge_env_vars()`
- [ ] Rename `GALILEO_HEADER_PREFIX` (HYBIM-729)
- [ ] Update CI/CD secrets and deployment configs to use `SPLUNK_AO_*` names
- [ ] Migrate this repo to `signalfx/splunk-ao-python`
