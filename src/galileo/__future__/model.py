from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class Model:
    """
    Immutable representation of a model from an integration provider.

    Models are associated with specific providers (OpenAI, Azure, Bedrock, etc.)
    and represent available LLM models that can be used in experiments and logging.

    The Model class is immutable once created and serializes to a string (model alias)
    when used in API calls or function parameters.

    Attributes
    ----------
        name (str): The model name (e.g., "gpt-4o-mini").
        alias (str): The model alias used in API calls.
        provider_name (str): The name of the provider this model belongs to.

    Examples
    --------
        # Create a model from a provider
        openai_provider = Integration.create_openai(token="sk-...")
        models = openai_provider.models
        model = models[0]

        # Use model in experiment (serializes to string)
        experiment = Experiment(
            name="test",
            dataset_name="dataset",
            prompt_name="prompt",
            project_name="project",
            model=model  # Automatically converts to string alias
        )

        # Model is immutable
        model.alias = "new-value"  # Raises AttributeError
    """

    _name: str
    _alias: str
    _provider_name: str

    def __init__(self, *, name: str, alias: str, provider_name: str) -> None:
        """
        Initialize a Model instance.

        Args:
            name (str): The model name.
            alias (str): The model alias used in API calls.
            provider_name (str): The provider name (e.g., "openai", "azure").
        """
        # Use object.__setattr__ to bypass __setattr__ immutability
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_alias", alias)
        object.__setattr__(self, "_provider_name", provider_name)

    @property
    def name(self) -> str:
        """Get the model name."""
        return self._name

    @property
    def alias(self) -> str:
        """Get the model alias."""
        return self._alias

    @property
    def provider_name(self) -> str:
        """Get the provider name."""
        return self._provider_name

    def __str__(self) -> str:
        """
        Convert model to string (returns alias).

        This allows models to be used directly in function parameters
        that expect a model name string.

        Returns
        -------
            str: The model alias.
        """
        return self._alias

    def __repr__(self) -> str:
        """Detailed string representation of the model."""
        return f"Model(name='{self._name}', alias='{self._alias}', provider='{self._provider_name}')"

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Prevent modification of model attributes (immutability).

        Raises
        ------
            AttributeError: Always, since models are immutable.
        """
        raise AttributeError(f"Model objects are immutable. Cannot set attribute '{name}'")

    def __delattr__(self, name: str) -> None:
        """
        Prevent deletion of model attributes (immutability).

        Raises
        ------
            AttributeError: Always, since models are immutable.
        """
        raise AttributeError(f"Model objects are immutable. Cannot delete attribute '{name}'")

    def __eq__(self, other: object) -> bool:
        """
        Check equality based on alias and provider.

        Args:
            other: Object to compare with.

        Returns
        -------
            bool: True if models have the same alias and provider.
        """
        if not isinstance(other, Model):
            return False
        return self._alias == other._alias and self._provider_name == other._provider_name

    def __hash__(self) -> int:
        """
        Hash based on alias and provider.

        Returns
        -------
            int: Hash value.
        """
        return hash((self._alias, self._provider_name))

    def to_dict(self) -> dict[str, Any]:
        """
        Convert model to dictionary representation.

        Returns
        -------
            dict: Dictionary with model properties.
        """
        return {"name": self._name, "alias": self._alias, "provider_name": self._provider_name}
