import json
from functools import cached_property
from typing import Any, Optional

from pydantic import BaseModel, field_validator, model_validator


class DatasetRecord(BaseModel):
    """
    A single record in a Galileo dataset.

    Attributes
    ----------
    id : Optional[str]
        Unique identifier for the record.
    input : str
        The input data (string or JSON-serializable object).
    output : Optional[str]
        The expected output / ground truth. 
        **Note:** This field can also be provided as `ground_truth` when creating records.
        Displayed as "Ground Truth" in the Galileo UI.
    generated_output : Optional[str]
        The model-generated output. Note: Displayed as "Generated Output" in the Galileo UI.
    metadata : Optional[dict[str, str]]
        Key-value metadata for the record.

    Note
    ----
    UI Terminology: The ``output`` field is shown as "Ground Truth" in the UI,
    while ``generated_output`` is shown as "Generated Output".
    
    Migration: You can use either ``output`` or ``ground_truth`` when creating records.
    Both will be stored as ``output`` internally. We recommend using ``output`` for consistency.
    
    Examples
    --------
    >>> # Using 'output' (also supported)
    >>> record1 = DatasetRecord(input="What is 2+2?", output="4")
    >>> 
    >>> # Using 'ground_truth' (recommended)
    >>> record2 = DatasetRecord(input="What is 2+2?", ground_truth="4")
    >>> assert record2.output == "4"  # Normalized to 'output'
    >>> assert record2.ground_truth == "4"  # Property accessor
    """

    id: Optional[str] = None
    input: str
    output: Optional[str] = None
    metadata: Optional[dict[str, str]] = None
    generated_output: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_ground_truth(cls, data: Any) -> dict[str, Any]:
        """
        Normalize ground_truth to output for backward compatibility.
        
        Accepts 'ground_truth' as input and maps it to 'output' internally.
        If both are provided, 'output' takes precedence (backward compatibility).
        """
        if isinstance(data, dict):
            # If ground_truth is provided but output is not, copy it to output
            if "ground_truth" in data and "output" not in data:
                data["output"] = data["ground_truth"]
            # Remove ground_truth from the data (we'll handle it via property only)
            if "ground_truth" in data:
                data.pop("ground_truth")
        return data

    @field_validator("input", mode="before")
    @classmethod
    def validate_input(cls, value: Any) -> str:
        if not isinstance(value, str):
            value = json.dumps(value)
        return value

    @field_validator("output", mode="before")
    @classmethod
    def validate_output(cls, value: Any) -> Optional[str]:
        if value is None:
            return None
        if not isinstance(value, str):
            value = json.dumps(value)
        return value

    @field_validator("metadata", mode="before")
    @classmethod
    def validate_metadata(cls, value: Any) -> Optional[dict[str, str]]:
        if value is None:
            return None
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                value = {"metadata": value}
        if not isinstance(value, dict):
            raise ValueError("Dataset metadata field must be either a string or dictionary")
        for _key, v in value.items():
            if not isinstance(v, str):
                raise ValueError("Dataset metadata field dictionary values must be strings")
        return value

    @field_validator("generated_output", mode="before")
    @classmethod
    def validate_generated_output(cls, value: Any) -> Optional[str]:
        if value is None:
            return None
        if not isinstance(value, str):
            value = json.dumps(value)
        return value

    @cached_property
    def deserialized_input(self) -> Any:
        try:
            return json.loads(self.input)
        except json.decoder.JSONDecodeError:
            return self.input

    @cached_property
    def deserialized_output(self) -> Optional[Any]:
        if self.output is None:
            return None
        try:
            return json.loads(self.output)
        except json.decoder.JSONDecodeError:
            return self.output

    @cached_property
    def deserialized_generated_output(self) -> Optional[Any]:
        if self.generated_output is None:
            return None
        try:
            return json.loads(self.generated_output)
        except json.decoder.JSONDecodeError:
            return self.generated_output

    @property
    def ground_truth(self) -> Optional[str]:
        """
        Get ground truth value (alias for output).
        
        This property provides read-only access to the 'output' field using
        the 'ground_truth' name for clarity.
        
        Returns
        -------
        Optional[str]
            The ground truth value (same as output field).
        """
        return self.output
