"""TypeSafe discovery uses metadata responses without exposing chat model operations."""

from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock

import httpx
import pytest

from galileo.config import GalileoPythonConfig
from galileo.integration import Integration
from galileo.provider import GenericProvider, OpenAIProvider
from galileo.resources.api.integrations import (
    list_available_integrations_integrations_available_get,
    list_integrations_integrations_get,
)
from galileo.resources.models.available_integrations import AvailableIntegrations
from galileo.resources.models.integration_db import IntegrationDB
from galileo.resources.models.integration_provider import IntegrationProvider
from galileo.shared.base import SyncState
from galileo.shared.exceptions import APIError, ValidationError


def _integration_row(provider: str, *, integration_id: str = "integration-id", **metadata: Any) -> dict[str, Any]:
    return {
        "id": integration_id,
        "name": f"{provider} workspace",
        "provider": provider,
        "created_at": "2026-10-01T10:00:00Z",
        "updated_at": "2026-10-02T10:00:00Z",
        "created_by": "owner-id",
        "permissions": [{"action": "read_secrets", "allowed": False}],
        "is_selected": False,
        "is_disabled": False,
        **metadata,
    }


@pytest.fixture
def raw_client(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Replace transport only so the real generated response parsers still run."""
    client = MagicMock()
    monkeypatch.setattr(GalileoPythonConfig, "get", MagicMock(return_value=SimpleNamespace(api_client=client)))
    return client


def test_typesafe_integration_db_decodes_wire_provider() -> None:
    # Given: a TypeSafe metadata row with a separate display name
    row = _integration_row("typesafe", name="Decision service")

    # When: decoding the API metadata response
    integration = IntegrationDB.from_dict(row)

    # Then: the provider is recognized and the display name and metadata survive
    assert integration.provider is IntegrationProvider.TYPESAFE
    assert integration.name == "Decision service"
    assert integration.created_by == "owner-id"
    assert integration.to_dict() == row | {
        "created_at": "2026-10-01T10:00:00+00:00",
        "updated_at": "2026-10-02T10:00:00+00:00",
    }


def test_available_integrations_decodes_typesafe_with_chat_providers() -> None:
    # Given: the available integration response contains chat and decision providers
    payload = {"integrations": ["openai", "typesafe", "anthropic"]}

    # When: decoding the API response
    available = AvailableIntegrations.from_dict(payload)

    # Then: all providers are retained in their original order
    assert available.integrations == [
        IntegrationProvider.OPENAI,
        IntegrationProvider.TYPESAFE,
        IntegrationProvider.ANTHROPIC,
    ]
    assert available.to_dict() == payload


def test_configured_integrations_parser_accepts_mixed_raw_response(raw_client: MagicMock) -> None:
    # Given: a raw HTTP response includes OpenAI and TypeSafe metadata rows
    response = httpx.Response(200, json=[_integration_row("openai"), _integration_row("typesafe")])

    # When: the generated configured integration endpoint parses the response
    integrations = list_integrations_integrations_get._parse_response(client=raw_client, response=response)

    # Then: one TypeSafe row does not prevent decoding the existing chat integration
    assert [integration.provider for integration in integrations] == [
        IntegrationProvider.OPENAI,
        IntegrationProvider.TYPESAFE,
    ]


def test_available_integrations_parser_accepts_mixed_raw_response(raw_client: MagicMock) -> None:
    # Given: the raw available integration response advertises TypeSafe beside OpenAI
    response = httpx.Response(200, json={"integrations": ["openai", "typesafe"]})

    # When: the generated available integration endpoint parses the response
    available = list_available_integrations_integrations_available_get._parse_response(
        client=raw_client, response=response
    )

    # Then: both integration providers are available to the SDK
    assert available.integrations == [IntegrationProvider.OPENAI, IntegrationProvider.TYPESAFE]


def test_list_hydrates_typesafe_generic_provider_from_raw_metadata(raw_client: MagicMock) -> None:
    # Given: the transport returns mixed metadata without provider credentials
    raw_client.request.return_value = httpx.Response(
        200,
        json=[
            _integration_row("openai", integration_id="openai-id"),
            _integration_row("typesafe", integration_id="decision-id", is_selected=True, is_disabled=True),
        ],
    )

    # When: listing configured integrations through the public SDK
    providers = Integration.list()

    # Then: TypeSafe reuses the generic metadata provider alongside the existing OpenAI provider
    assert len(providers) == 2
    assert isinstance(providers[0], OpenAIProvider)
    typesafe = providers[1]
    assert isinstance(typesafe, GenericProvider)
    assert typesafe.id == "decision-id"
    assert typesafe.name == "typesafe workspace"
    assert typesafe.created_by == "owner-id"
    assert typesafe.created_at == datetime(2026, 10, 1, 10, tzinfo=timezone.utc)
    assert typesafe.updated_at == datetime(2026, 10, 2, 10, tzinfo=timezone.utc)
    assert typesafe.is_selected is True
    assert typesafe.is_disabled is True
    assert typesafe.permissions is not None
    assert [permission.to_dict() for permission in typesafe.permissions] == [
        {"action": "read_secrets", "allowed": False}
    ]
    assert typesafe._get_integration_provider() is IntegrationProvider.TYPESAFE
    assert typesafe.sync_state is SyncState.SYNCED
    assert raw_client.request.call_args.kwargs["path"] == "/integrations"
    assert raw_client.request.call_args.kwargs["content_headers"]["X-Galileo-Integration-Capabilities"] == "typesafe"


def test_list_all_includes_typesafe_from_raw_response(raw_client: MagicMock) -> None:
    # Given: the transport advertises TypeSafe with the existing chat provider
    raw_client.request.return_value = httpx.Response(200, json={"integrations": ["openai", "typesafe"]})

    # When: listing all available integration types
    available = Integration.list(all=True)

    # Then: the public result contains wire provider names and opts into TypeSafe discovery
    assert available == ["openai", "typesafe"]
    assert raw_client.request.call_args.kwargs["path"] == "/integrations/available"
    assert raw_client.request.call_args.kwargs["content_headers"]["X-Galileo-Integration-Capabilities"] == "typesafe"


def test_openai_shortcut_still_selects_openai_with_typesafe_present(raw_client: MagicMock) -> None:
    # Given: a TypeSafe row and two OpenAI rows with independent display names
    raw_client.request.return_value = httpx.Response(
        200,
        json=[
            _integration_row("typesafe", integration_id="decision-id", is_selected=True),
            _integration_row("openai", integration_id="shared-openai", name="Team OpenAI"),
            _integration_row("openai", integration_id="selected-openai", name="My OpenAI", is_selected=True),
        ],
    )

    # When: accessing the existing OpenAI convenience property
    openai = Integration.openai

    # Then: provider type and selection identify the configured OpenAI integration
    assert isinstance(openai, OpenAIProvider)
    assert openai.id == "selected-openai"
    assert openai.name == "My OpenAI"


@pytest.mark.parametrize("provider_name", ["typesafe", "openai"])
def test_provider_refresh_matches_exact_id_and_updates_metadata(raw_client: MagicMock, provider_name: str) -> None:
    # Given: a listed provider and another shared integration of the same provider type
    provider = Integration._to_provider(
        IntegrationDB.from_dict(_integration_row(provider_name, integration_id="target-id"))
    )
    refreshed_row = _integration_row(
        provider_name,
        integration_id="target-id",
        name="Renamed workspace",
        created_by="new-owner-id",
        created_at="2026-09-20T12:00:00Z",
        updated_at="2026-10-12T13:00:00Z",
        permissions=[{"action": "read_secrets", "allowed": True}],
        is_selected=True,
        is_disabled=True,
    )
    raw_client.request.return_value = httpx.Response(
        200, json=[_integration_row(provider_name, integration_id="other-id", name="Other workspace"), refreshed_row]
    )

    # When: refreshing the listed provider
    provider.refresh()

    # Then: metadata is refreshed by identity through the list endpoint without credential retrieval
    assert provider.id == "target-id"
    assert provider.name == "Renamed workspace"
    assert provider.created_by == "new-owner-id"
    assert provider.created_at == datetime(2026, 9, 20, 12, tzinfo=timezone.utc)
    assert provider.updated_at == datetime(2026, 10, 12, 13, tzinfo=timezone.utc)
    assert provider.is_selected is True
    assert provider.is_disabled is True
    assert provider.permissions is not None
    assert [permission.to_dict() for permission in provider.permissions] == [
        {"action": "read_secrets", "allowed": True}
    ]
    assert provider._get_integration_provider() is IntegrationProvider(provider_name)
    assert provider.sync_state is SyncState.SYNCED
    raw_client.request.assert_called_once()
    assert raw_client.request.call_args.kwargs["path"] == "/integrations"
    assert raw_client.request.call_args.kwargs["content_headers"]["X-Galileo-Integration-Capabilities"] == "typesafe"


@pytest.mark.parametrize("remaining_rows", [[], [_integration_row("typesafe", integration_id="other-id")]])
def test_provider_refresh_fails_when_its_id_is_absent(raw_client: MagicMock, remaining_rows: list[dict]) -> None:
    # Given: the current provider ID is absent from the latest metadata response
    provider = Integration._to_provider(IntegrationDB.from_dict(_integration_row("typesafe", integration_id="gone-id")))
    raw_client.request.return_value = httpx.Response(200, json=remaining_rows)

    # When/Then: refreshing reports the missing identity and preserves the local metadata
    with pytest.raises(APIError, match="gone-id.*not found"):
        provider.refresh()
    assert provider.id == "gone-id"
    assert provider.name == "typesafe workspace"
    assert provider.sync_state is SyncState.FAILED_SYNC
    assert raw_client.request.call_args.kwargs["path"] == "/integrations"


def test_provider_refresh_without_id_fails_before_request(raw_client: MagicMock) -> None:
    # Given: a metadata provider has lost its integration ID
    provider = Integration._to_provider(IntegrationDB.from_dict(_integration_row("typesafe")))
    provider.id = None

    # When/Then: refreshing fails before calling the API
    with pytest.raises(ValidationError, match="without an ID"):
        provider.refresh()
    assert provider.sync_state is SyncState.FAILED_SYNC
    raw_client.request.assert_not_called()


@pytest.mark.parametrize("operation", ["models", "get_model"])
def test_typesafe_rejects_chat_models_before_http_request(raw_client: MagicMock, operation: str) -> None:
    # Given: a synced TypeSafe metadata provider
    provider = Integration._to_provider(IntegrationDB.from_dict(_integration_row("typesafe")))

    # When/Then: chat model access raises a provider-specific SDK validation error without making a request
    with pytest.raises(ValidationError, match="typesafe"):
        if operation == "models":
            _ = provider.models
        else:
            provider.get_model(name="decision-model")
    raw_client.request.assert_not_called()
