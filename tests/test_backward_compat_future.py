"""Tests that all migrated symbols remain importable from galileo.__future__ and resolve to the same objects."""


def test_project_is_same_class():
    from galileo.__future__ import Project as FutureProject
    from galileo.project import Project as RootProject

    assert FutureProject is RootProject


def test_collaborator_is_same_class():
    from galileo.__future__ import Collaborator as FutureCollaborator
    from galileo.collaborator import Collaborator as RootCollaborator

    assert FutureCollaborator is RootCollaborator


def test_collaborator_role_is_same_class():
    from galileo.__future__ import CollaboratorRole as FutureRole
    from galileo.collaborator import CollaboratorRole as RootRole

    assert FutureRole is RootRole


def test_sync_state_is_same_class():
    from galileo.__future__.shared.base import SyncState as FutureSyncState
    from galileo.shared.base import SyncState as RootSyncState

    assert FutureSyncState is RootSyncState


def test_state_management_mixin_is_same_class():
    from galileo.__future__.shared.base import StateManagementMixin as FutureMixin
    from galileo.shared.base import StateManagementMixin as RootMixin

    assert FutureMixin is RootMixin


def test_exceptions_are_same_classes():
    from galileo.__future__.shared.exceptions import APIError as FutureAPIError
    from galileo.__future__.shared.exceptions import ConfigurationError as FutureConfigError
    from galileo.__future__.shared.exceptions import GalileoFutureError as FutureBaseError
    from galileo.__future__.shared.exceptions import IntegrationNotConfiguredError as FutureIntError
    from galileo.__future__.shared.exceptions import ResourceConflictError as FutureConflictError
    from galileo.__future__.shared.exceptions import ResourceNotFoundError as FutureNotFoundError
    from galileo.__future__.shared.exceptions import SyncError as FutureSyncError
    from galileo.__future__.shared.exceptions import ValidationError as FutureValidationError
    from galileo.shared.exceptions import (
        APIError,
        ConfigurationError,
        GalileoFutureError,
        IntegrationNotConfiguredError,
        ResourceConflictError,
        ResourceNotFoundError,
        SyncError,
        ValidationError,
    )

    assert FutureAPIError is APIError
    assert FutureConfigError is ConfigurationError
    assert FutureBaseError is GalileoFutureError
    assert FutureIntError is IntegrationNotConfiguredError
    assert FutureConflictError is ResourceConflictError
    assert FutureNotFoundError is ResourceNotFoundError
    assert FutureSyncError is SyncError
    assert FutureValidationError is ValidationError


def test_root_init_exports():
    """Test that the new exports are available from the galileo package root."""
    from galileo import Collaborator, CollaboratorRole, Project, SyncState

    assert Project is not None
    assert Collaborator is not None
    assert CollaboratorRole is not None
    assert SyncState is not None


def test_configuration_is_same_class():
    from galileo.__future__.configuration import Configuration as FutureConfiguration
    from galileo.configuration import Configuration as RootConfiguration

    assert FutureConfiguration is RootConfiguration


def test_model_is_same_class():
    from galileo.__future__.model import Model as FutureModel
    from galileo.model import Model as RootModel

    assert FutureModel is RootModel


def test_dataset_is_same_class():
    from galileo.__future__.dataset import Dataset as FutureDataset
    from galileo.dataset import Dataset as RootDataset

    assert FutureDataset is RootDataset


def test_prompt_is_same_class():
    from galileo.__future__.prompt import Prompt as FuturePrompt
    from galileo.prompt import Prompt as RootPrompt

    assert FuturePrompt is RootPrompt


def test_integration_is_same_class():
    from galileo.__future__.integration import Integration as FutureIntegration
    from galileo.integration import Integration as RootIntegration

    assert FutureIntegration is RootIntegration


def test_provider_classes_are_same():
    from galileo.__future__.provider import AnthropicProvider as FutureAnthropic
    from galileo.__future__.provider import AzureProvider as FutureAzure
    from galileo.__future__.provider import BedrockProvider as FutureBedrock
    from galileo.__future__.provider import OpenAIProvider as FutureOpenAI
    from galileo.__future__.provider import Provider as FutureProvider
    from galileo.provider import AnthropicProvider, AzureProvider, BedrockProvider, OpenAIProvider, Provider

    assert FutureAnthropic is AnthropicProvider
    assert FutureAzure is AzureProvider
    assert FutureBedrock is BedrockProvider
    assert FutureOpenAI is OpenAIProvider
    assert FutureProvider is Provider


def test_metric_classes_are_same():
    from galileo.__future__.metric import CodeMetric as FutureCodeMetric
    from galileo.__future__.metric import GalileoMetric as FutureGalileoMetric
    from galileo.__future__.metric import LlmMetric as FutureLlmMetric
    from galileo.__future__.metric import LocalMetric as FutureLocalMetric
    from galileo.__future__.metric import Metric as FutureMetric
    from galileo.metric import CodeMetric, GalileoMetric, LlmMetric, LocalMetric, Metric

    assert FutureMetric is Metric
    assert FutureCodeMetric is CodeMetric
    assert FutureGalileoMetric is GalileoMetric
    assert FutureLlmMetric is LlmMetric
    assert FutureLocalMetric is LocalMetric


def test_experiment_is_same_class():
    from galileo.__future__.experiment import Experiment as FutureExperiment
    from galileo.experiment import Experiment as RootExperiment

    assert FutureExperiment is RootExperiment


def test_log_stream_is_same_class():
    from galileo.__future__.log_stream import LogStream as FutureLogStream
    from galileo.log_stream import LogStream as RootLogStream

    assert FutureLogStream is RootLogStream


def test_shared_filter_functions_are_same():
    from galileo.__future__.shared.filter import boolean as future_boolean
    from galileo.__future__.shared.filter import date as future_date
    from galileo.__future__.shared.filter import number as future_number
    from galileo.__future__.shared.filter import text as future_text
    from galileo.shared.filter import boolean, date, number, text

    assert future_boolean is boolean
    assert future_date is date
    assert future_number is number
    assert future_text is text


def test_shared_sort_is_same():
    from galileo.__future__.shared.sort import sort as future_sort
    from galileo.shared.sort import sort

    assert future_sort is sort


def test_shared_column_classes_are_same():
    from galileo.__future__.shared.column import Column as FutureColumn
    from galileo.__future__.shared.column import ColumnCollection as FutureColumnCollection
    from galileo.shared.column import Column, ColumnCollection

    assert FutureColumn is Column
    assert FutureColumnCollection is ColumnCollection


def test_shared_query_result_is_same():
    from galileo.__future__.shared.query_result import QueryResult as FutureQueryResult
    from galileo.shared.query_result import QueryResult

    assert FutureQueryResult is QueryResult


def test_shared_experiment_result_classes_are_same():
    from galileo.__future__.shared.experiment_result import ExperimentRunResult as FutureRunResult
    from galileo.__future__.shared.experiment_result import ExperimentStatusInfo as FutureStatusInfo
    from galileo.shared.experiment_result import ExperimentRunResult, ExperimentStatusInfo

    assert FutureRunResult is ExperimentRunResult
    assert FutureStatusInfo is ExperimentStatusInfo


def test_types_metric_spec_is_same():
    from galileo.__future__.types import MetricSpec as FutureMetricSpec
    from galileo.types import MetricSpec

    assert FutureMetricSpec is MetricSpec


def test_provider_generic_and_unconfigured_are_same():
    from galileo.__future__.provider import GenericProvider as FutureGeneric
    from galileo.__future__.provider import UnconfiguredProvider as FutureUnconfigured
    from galileo.provider import GenericProvider, UnconfiguredProvider

    assert FutureGeneric is GenericProvider
    assert FutureUnconfigured is UnconfiguredProvider


def test_metric_builtin_metrics_is_same():
    from galileo.__future__.metric import BuiltInMetrics as FutureBuiltIn
    from galileo.metric import BuiltInMetrics

    assert FutureBuiltIn is BuiltInMetrics


def test_prompt_private_symbols_are_same():
    from galileo.__future__.prompt import PromptVersion as FuturePromptVersion
    from galileo.__future__.prompt import _parse_template_to_messages as future_parse
    from galileo.prompt import PromptVersion, _parse_template_to_messages

    assert FuturePromptVersion is PromptVersion
    assert future_parse is _parse_template_to_messages


def test_shared_column_unwrap_unset_is_same():
    from galileo.__future__.shared.column import _unwrap_unset as future_unwrap
    from galileo.shared.column import _unwrap_unset

    assert future_unwrap is _unwrap_unset


def test_shared_query_result_flatten_dict_is_same():
    from galileo.__future__.shared.query_result import _flatten_dict as future_flatten
    from galileo.shared.query_result import _flatten_dict

    assert future_flatten is _flatten_dict


def test_shared_experiment_result_phase_info_is_same():
    from galileo.__future__.shared.experiment_result import ExperimentPhaseInfo as FuturePhaseInfo
    from galileo.shared.experiment_result import ExperimentPhaseInfo

    assert FuturePhaseInfo is ExperimentPhaseInfo


def test_shared_utils_classproperty_is_same():
    from galileo.__future__.shared.utils import classproperty as future_classproperty
    from galileo.shared.utils import classproperty

    assert future_classproperty is classproperty


def test_configuration_private_symbols_are_same():
    from galileo.__future__.configuration import _CONFIGURATION_KEYS as future_keys
    from galileo.__future__.configuration import VALID_LOG_LEVELS as future_levels
    from galileo.__future__.configuration import parse_log_level as future_parse
    from galileo.configuration import _CONFIGURATION_KEYS, VALID_LOG_LEVELS, parse_log_level

    assert future_keys is _CONFIGURATION_KEYS
    assert future_levels is VALID_LOG_LEVELS
    assert future_parse is parse_log_level


def test_shared_sort_class_is_same():
    from galileo.__future__.shared.sort import Sort as FutureSort
    from galileo.shared.sort import Sort

    assert FutureSort is Sort


def test_root_init_has_new_exports():
    """Test that all newly migrated domain objects are available from galileo package root."""
    from galileo import (
        AnthropicProvider,
        AzureProvider,
        BedrockProvider,
        CodeMetric,
        Configuration,
        Dataset,
        Experiment,
        GalileoMetric,
        Integration,
        LlmMetric,
        LocalMetric,
        LogStream,
        Metric,
        MetricSpec,
        Model,
        OpenAIProvider,
        Prompt,
        Provider,
    )

    assert Configuration is not None
    assert Dataset is not None
    assert Experiment is not None
    assert Integration is not None
    assert LogStream is not None
    assert Metric is not None
    assert CodeMetric is not None
    assert GalileoMetric is not None
    assert LlmMetric is not None
    assert LocalMetric is not None
    assert MetricSpec is not None
    assert Model is not None
    assert Prompt is not None
    assert Provider is not None
    assert AnthropicProvider is not None
    assert AzureProvider is not None
    assert BedrockProvider is not None
    assert OpenAIProvider is not None
