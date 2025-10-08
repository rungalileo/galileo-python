"""
Tests for global prompt template functionality only.

This test file covers the simplified global-only prompt templates API.
"""
import json
from http import HTTPStatus
from unittest.mock import Mock, patch

import httpx
import pytest
from respx import MockRouter

from galileo import Message, MessageRole
from galileo.prompts import (
    PromptTemplateAPIException,
    create_prompt,
    delete_prompt,
    get_prompt,
    get_prompts,
)
@pytest.fixture
def prompt_template_response():
    """Create a sample prompt template response dict."""
    return {
        "id": "template-id-123",
        "name": "test-template",
        "template": '[{"role":"system","content":"test"}]',
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "selected_version": 1,
        "selected_version_id": "version-id-123",
        "versions": [
            {
                "id": "version-id-123",
                "template_id": "template-id-123",
                "version": 1,
                "messages": [{"role": "system", "content": "test"}],
                "raw": False,
            }
        ],
    }


class TestGlobalPromptTemplates:
    """Test global prompt template CRUD operations."""

    def test_create_global_prompt(self, respx_mock: MockRouter, prompt_template_response):
        """Test creating a global prompt template."""
        # Mock the query API (for uniqueness check)
        query_route = respx_mock.post("http://localtest:8088/templates/query").mock(
            return_value=httpx.Response(200, json={"templates": []})
        )
        
        # Mock the create API
        create_route = respx_mock.post("http://localtest:8088/templates").mock(
            return_value=httpx.Response(200, json=prompt_template_response)
        )

        # Create template
        template = create_prompt(
            name="test-template",
            template=[Message(role=MessageRole.SYSTEM, content="test")]
        )

        assert template.name == "test-template"
        assert query_route.called
        assert create_route.called

    def test_get_global_prompt_by_id(self, respx_mock: MockRouter, prompt_template_response):
        """Test retrieving a global prompt template by ID."""
        get_route = respx_mock.get(f"http://localtest:8088/templates/{prompt_template_response['id']}").mock(
            return_value=prompt_template_response
        )

        template = get_prompt(id=prompt_template_response['id'])

        assert template is not None
        assert template.name == "test-template"
        assert get_route.called

    def test_get_global_prompt_by_name(self, respx_mock: MockRouter, prompt_template_response):
        """Test retrieving a global prompt template by name."""
        query_route = respx_mock.post("http://localtest:8088/templates/query").mock(
            return_value={
                "templates": [prompt_template_response],
                "next_starting_token": None
            }
        )

        template = get_prompt(name="test-template")

        assert template is not None
        assert template.name == "test-template"
        assert query_route.called

    def test_list_global_prompts(self, respx_mock: MockRouter, prompt_template_response):
        """Test listing global prompt templates."""
        query_route = respx_mock.post("http://localtest:8088/templates/query").mock(
            return_value={
                "templates": [prompt_template_response],
                "next_starting_token": None
            }
        )

        templates = get_prompts()

        assert len(templates) == 1
        assert templates[0].name == "test-template"
        assert query_route.called

    def test_delete_global_prompt_by_id(self, respx_mock: MockRouter):
        """Test deleting a global prompt template by ID."""
        delete_route = respx_mock.delete("http://localtest:8088/templates/template-id-123").mock(
            return_value={}
        )

        delete_prompt(id="template-id-123")

        assert delete_route.called

    def test_delete_global_prompt_by_name(self, respx_mock: MockRouter, prompt_template_response):
        """Test deleting a global prompt template by name."""
        # Mock query to find template by name
        query_route = respx_mock.post("http://localtest:8088/templates/query").mock(
            return_value={
                "templates": [prompt_template_response],
                "next_starting_token": None
            }
        )
        
        # Mock delete
        delete_route = respx_mock.delete(f"http://localtest:8088/templates/{prompt_template_response['id']}").mock(
            return_value={}
        )

        delete_prompt(name="test-template")

        assert query_route.called
        assert delete_route.called

    def test_create_prompt_with_unique_name(self, respx_mock: MockRouter, prompt_template_response):
        """Test that duplicate names get auto-incremented."""
        # Mock query to find existing template
        existing_template = {**prompt_template_response, "name": "test-template"}
        query_route = respx_mock.post("http://localtest:8088/templates/query").mock(
            return_value={
                "templates": [existing_template],
                "next_starting_token": None
            }
        )

        # Mock create with new unique name
        new_template = {**prompt_template_response, "name": "test-template (1)"}
        create_route = respx_mock.post("http://localtest:8088/templates").mock(
            return_value=new_template
        )

        template = create_prompt(
            name="test-template",
            template=[Message(role=MessageRole.SYSTEM, content="test")]
        )

        # Should have been renamed to avoid conflict
        assert template.name == "test-template (1)"
        assert query_route.called
        assert create_route.called
