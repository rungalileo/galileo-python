# flake: noqa: F401, F811
# ruff: noqa: F401, F811
from typing import Any

from pydantic import BaseModel

from galileo_core.constants.config import ConfigEnvironmentVariables
from galileo_core.constants.config import ConfigEnvironmentVariables as GalileoCoreConfigEnvironmentVariablesClass
from galileo_core.constants.dataset_format import DatasetFormat
from galileo_core.constants.dataset_format import DatasetFormat as GalileoCoreDatasetFormatClass
from galileo_core.constants.http_headers import HttpHeaders
from galileo_core.constants.http_headers import HttpHeaders as GalileoCoreHttpHeadersClass
from galileo_core.constants.processing_headers import ProcessingHeaders
from galileo_core.constants.processing_headers import ProcessingHeaders as GalileoCoreProcessingHeadersClass
from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.request_method import RequestMethod as GalileoCoreRequestMethodClass
from galileo_core.constants.routes import Routes
from galileo_core.constants.routes import Routes as GalileoCoreRoutesClass
from galileo_core.exceptions.base import BaseGalileoException
from galileo_core.exceptions.base import BaseGalileoException as GalileoCoreBaseGalileoExceptionClass
from galileo_core.exceptions.execution import BaseGalileoException, ExecutionError
from galileo_core.exceptions.execution import BaseGalileoException as GalileoCoreBaseGalileoExceptionClass
from galileo_core.exceptions.execution import ExecutionError as GalileoCoreExecutionErrorClass
from galileo_core.exceptions.http import GalileoHTTPException
from galileo_core.exceptions.http import GalileoHTTPException as GalileoCoreGalileoHTTPExceptionClass
from galileo_core.helpers.api_client import ApiClient, GalileoHTTPException, HttpHeaders, RequestMethod
from galileo_core.helpers.api_client import ApiClient as GalileoCoreApiClientClass
from galileo_core.helpers.api_client import GalileoHTTPException as GalileoCoreGalileoHTTPExceptionClass
from galileo_core.helpers.api_client import HttpHeaders as GalileoCoreHttpHeadersClass
from galileo_core.helpers.api_client import RequestMethod as GalileoCoreRequestMethodClass
from galileo_core.helpers.api_key import (
    ApiKeyResponse,
    CollaboratorRole,
    CreateApiKeyRequest,
    CreateApiKeyResponse,
    GalileoConfig,
    RequestMethod,
    Routes,
)
from galileo_core.helpers.api_key import ApiKeyResponse as GalileoCoreApiKeyResponseClass
from galileo_core.helpers.api_key import CollaboratorRole as GalileoCoreCollaboratorRoleClass
from galileo_core.helpers.api_key import CreateApiKeyRequest as GalileoCoreCreateApiKeyRequestClass
from galileo_core.helpers.api_key import CreateApiKeyResponse as GalileoCoreCreateApiKeyResponseClass
from galileo_core.helpers.api_key import GalileoConfig as GalileoCoreGalileoConfigClass
from galileo_core.helpers.api_key import RequestMethod as GalileoCoreRequestMethodClass
from galileo_core.helpers.api_key import Routes as GalileoCoreRoutesClass
from galileo_core.helpers.dataset import Dataset, GalileoConfig, RequestMethod, Routes, UploadDatasetRequest
from galileo_core.helpers.dataset import Dataset as GalileoCoreDatasetClass
from galileo_core.helpers.dataset import GalileoConfig as GalileoCoreGalileoConfigClass
from galileo_core.helpers.dataset import RequestMethod as GalileoCoreRequestMethodClass
from galileo_core.helpers.dataset import Routes as GalileoCoreRoutesClass
from galileo_core.helpers.dataset import UploadDatasetRequest as GalileoCoreUploadDatasetRequestClass
from galileo_core.helpers.execution import AsyncExecutor
from galileo_core.helpers.execution import AsyncExecutor as GalileoCoreAsyncExecutorClass
from galileo_core.helpers.group import (
    AddGroupMemberRequest,
    AddGroupMemberResponse,
    CreateGroupRequest,
    CreateGroupResponse,
    GalileoConfig,
    GroupRole,
    GroupVisibility,
    RequestMethod,
    Routes,
)
from galileo_core.helpers.group import AddGroupMemberRequest as GalileoCoreAddGroupMemberRequestClass
from galileo_core.helpers.group import AddGroupMemberResponse as GalileoCoreAddGroupMemberResponseClass
from galileo_core.helpers.group import CreateGroupRequest as GalileoCoreCreateGroupRequestClass
from galileo_core.helpers.group import CreateGroupResponse as GalileoCoreCreateGroupResponseClass
from galileo_core.helpers.group import GalileoConfig as GalileoCoreGalileoConfigClass
from galileo_core.helpers.group import GroupRole as GalileoCoreGroupRoleClass
from galileo_core.helpers.group import GroupVisibility as GalileoCoreGroupVisibilityClass
from galileo_core.helpers.group import RequestMethod as GalileoCoreRequestMethodClass
from galileo_core.helpers.group import Routes as GalileoCoreRoutesClass
from galileo_core.helpers.group_project import (
    CollaboratorRole,
    GalileoConfig,
    GroupProjectCollaboratorRequest,
    GroupProjectCollaboratorResponse,
    RequestMethod,
    Routes,
)
from galileo_core.helpers.group_project import CollaboratorRole as GalileoCoreCollaboratorRoleClass
from galileo_core.helpers.group_project import GalileoConfig as GalileoCoreGalileoConfigClass
from galileo_core.helpers.group_project import (
    GroupProjectCollaboratorRequest as GalileoCoreGroupProjectCollaboratorRequestClass,
)
from galileo_core.helpers.group_project import (
    GroupProjectCollaboratorResponse as GalileoCoreGroupProjectCollaboratorResponseClass,
)
from galileo_core.helpers.group_project import RequestMethod as GalileoCoreRequestMethodClass
from galileo_core.helpers.group_project import Routes as GalileoCoreRoutesClass
from galileo_core.helpers.health import GalileoConfig, RequestMethod, Routes
from galileo_core.helpers.health import GalileoConfig as GalileoCoreGalileoConfigClass
from galileo_core.helpers.health import RequestMethod as GalileoCoreRequestMethodClass
from galileo_core.helpers.health import Routes as GalileoCoreRoutesClass
from galileo_core.helpers.pagination import PaginationRequest, PaginationResponse
from galileo_core.helpers.pagination import PaginationRequest as GalileoCorePaginationRequestClass
from galileo_core.helpers.pagination import PaginationResponse as GalileoCorePaginationResponseClass
from galileo_core.helpers.project import (
    CreateProjectRequest,
    GalileoConfig,
    ProjectResponse,
    ProjectType,
    RequestMethod,
    Routes,
)
from galileo_core.helpers.project import CreateProjectRequest as GalileoCoreCreateProjectRequestClass
from galileo_core.helpers.project import GalileoConfig as GalileoCoreGalileoConfigClass
from galileo_core.helpers.project import ProjectResponse as GalileoCoreProjectResponseClass
from galileo_core.helpers.project import ProjectType as GalileoCoreProjectTypeClass
from galileo_core.helpers.project import RequestMethod as GalileoCoreRequestMethodClass
from galileo_core.helpers.project import Routes as GalileoCoreRoutesClass
from galileo_core.helpers.user import (
    AuthMethod,
    GalileoConfig,
    InviteUsersRequest,
    RequestMethod,
    Routes,
    UpdateUserRoleRequest,
    User,
    UserRole,
)
from galileo_core.helpers.user import AuthMethod as GalileoCoreAuthMethodClass
from galileo_core.helpers.user import GalileoConfig as GalileoCoreGalileoConfigClass
from galileo_core.helpers.user import InviteUsersRequest as GalileoCoreInviteUsersRequestClass
from galileo_core.helpers.user import RequestMethod as GalileoCoreRequestMethodClass
from galileo_core.helpers.user import Routes as GalileoCoreRoutesClass
from galileo_core.helpers.user import UpdateUserRoleRequest as GalileoCoreUpdateUserRoleRequestClass
from galileo_core.helpers.user import User as GalileoCoreUserClass
from galileo_core.helpers.user import UserRole as GalileoCoreUserRoleClass
from galileo_core.helpers.user_project import (
    CollaboratorRole,
    GalileoConfig,
    RequestMethod,
    Routes,
    UserProjectCollaboratorRequest,
    UserProjectCollaboratorResponse,
)
from galileo_core.helpers.user_project import CollaboratorRole as GalileoCoreCollaboratorRoleClass
from galileo_core.helpers.user_project import GalileoConfig as GalileoCoreGalileoConfigClass
from galileo_core.helpers.user_project import RequestMethod as GalileoCoreRequestMethodClass
from galileo_core.helpers.user_project import Routes as GalileoCoreRoutesClass
from galileo_core.helpers.user_project import (
    UserProjectCollaboratorRequest as GalileoCoreUserProjectCollaboratorRequestClass,
)
from galileo_core.helpers.user_project import (
    UserProjectCollaboratorResponse as GalileoCoreUserProjectCollaboratorResponseClass,
)
from galileo_core.schemas.base_config import ApiClient, GalileoConfig, RequestMethod, Routes, User
from galileo_core.schemas.base_config import ApiClient as GalileoCoreApiClientClass
from galileo_core.schemas.base_config import GalileoConfig as GalileoCoreGalileoConfigClass
from galileo_core.schemas.base_config import RequestMethod as GalileoCoreRequestMethodClass
from galileo_core.schemas.base_config import Routes as GalileoCoreRoutesClass
from galileo_core.schemas.base_config import User as GalileoCoreUserClass
from galileo_core.schemas.core.api_key import (
    ApiKeyResponse,
    BaseApiKey,
    CollaboratorRole,
    CreateApiKeyRequest,
    CreateApiKeyResponse,
)
from galileo_core.schemas.core.api_key import ApiKeyResponse as GalileoCoreApiKeyResponseClass
from galileo_core.schemas.core.api_key import BaseApiKey as GalileoCoreBaseApiKeyClass
from galileo_core.schemas.core.api_key import CollaboratorRole as GalileoCoreCollaboratorRoleClass
from galileo_core.schemas.core.api_key import CreateApiKeyRequest as GalileoCoreCreateApiKeyRequestClass
from galileo_core.schemas.core.api_key import CreateApiKeyResponse as GalileoCoreCreateApiKeyResponseClass
from galileo_core.schemas.core.auth_method import AuthMethod
from galileo_core.schemas.core.auth_method import AuthMethod as GalileoCoreAuthMethodClass
from galileo_core.schemas.core.collaboration_role import CollaboratorRole
from galileo_core.schemas.core.collaboration_role import CollaboratorRole as GalileoCoreCollaboratorRoleClass
from galileo_core.schemas.core.dataset import BaseDatasetRequest, Dataset, DatasetFormat, UploadDatasetRequest
from galileo_core.schemas.core.dataset import BaseDatasetRequest as GalileoCoreBaseDatasetRequestClass
from galileo_core.schemas.core.dataset import Dataset as GalileoCoreDatasetClass
from galileo_core.schemas.core.dataset import DatasetFormat as GalileoCoreDatasetFormatClass
from galileo_core.schemas.core.dataset import UploadDatasetRequest as GalileoCoreUploadDatasetRequestClass
from galileo_core.schemas.core.group import (
    AddGroupMemberRequest,
    AddGroupMemberResponse,
    CreateGroupRequest,
    CreateGroupResponse,
    GroupRole,
    GroupVisibility,
)
from galileo_core.schemas.core.group import AddGroupMemberRequest as GalileoCoreAddGroupMemberRequestClass
from galileo_core.schemas.core.group import AddGroupMemberResponse as GalileoCoreAddGroupMemberResponseClass
from galileo_core.schemas.core.group import CreateGroupRequest as GalileoCoreCreateGroupRequestClass
from galileo_core.schemas.core.group import CreateGroupResponse as GalileoCoreCreateGroupResponseClass
from galileo_core.schemas.core.group import GroupRole as GalileoCoreGroupRoleClass
from galileo_core.schemas.core.group import GroupVisibility as GalileoCoreGroupVisibilityClass
from galileo_core.schemas.core.group_project import (
    CollaboratorRole,
    GroupProjectCollaboratorRequest,
    GroupProjectCollaboratorResponse,
)
from galileo_core.schemas.core.group_project import CollaboratorRole as GalileoCoreCollaboratorRoleClass
from galileo_core.schemas.core.group_project import (
    GroupProjectCollaboratorRequest as GalileoCoreGroupProjectCollaboratorRequestClass,
)
from galileo_core.schemas.core.group_project import (
    GroupProjectCollaboratorResponse as GalileoCoreGroupProjectCollaboratorResponseClass,
)
from galileo_core.schemas.core.group_role import GroupRole
from galileo_core.schemas.core.group_role import GroupRole as GalileoCoreGroupRoleClass
from galileo_core.schemas.core.group_visibility import GroupVisibility
from galileo_core.schemas.core.group_visibility import GroupVisibility as GalileoCoreGroupVisibilityClass
from galileo_core.schemas.core.pagination import PaginationRequest, PaginationResponse
from galileo_core.schemas.core.pagination import PaginationRequest as GalileoCorePaginationRequestClass
from galileo_core.schemas.core.pagination import PaginationResponse as GalileoCorePaginationResponseClass
from galileo_core.schemas.core.project import CreateProjectRequest, ProjectResponse, ProjectType
from galileo_core.schemas.core.project import CreateProjectRequest as GalileoCoreCreateProjectRequestClass
from galileo_core.schemas.core.project import ProjectResponse as GalileoCoreProjectResponseClass
from galileo_core.schemas.core.project import ProjectType as GalileoCoreProjectTypeClass
from galileo_core.schemas.core.user import AuthMethod, InviteUsersRequest, UpdateUserRoleRequest, User, UserRole
from galileo_core.schemas.core.user import AuthMethod as GalileoCoreAuthMethodClass
from galileo_core.schemas.core.user import InviteUsersRequest as GalileoCoreInviteUsersRequestClass
from galileo_core.schemas.core.user import UpdateUserRoleRequest as GalileoCoreUpdateUserRoleRequestClass
from galileo_core.schemas.core.user import User as GalileoCoreUserClass
from galileo_core.schemas.core.user import UserRole as GalileoCoreUserRoleClass
from galileo_core.schemas.core.user_project import (
    CollaboratorRole,
    UserProjectCollaboratorRequest,
    UserProjectCollaboratorResponse,
)
from galileo_core.schemas.core.user_project import CollaboratorRole as GalileoCoreCollaboratorRoleClass
from galileo_core.schemas.core.user_project import (
    UserProjectCollaboratorRequest as GalileoCoreUserProjectCollaboratorRequestClass,
)
from galileo_core.schemas.core.user_project import (
    UserProjectCollaboratorResponse as GalileoCoreUserProjectCollaboratorResponseClass,
)
from galileo_core.schemas.core.user_role import SystemRole, UserRole
from galileo_core.schemas.core.user_role import SystemRole as GalileoCoreSystemRoleClass
from galileo_core.schemas.core.user_role import UserRole as GalileoCoreUserRoleClass
from galileo_core.schemas.logging.llm import Message, MessageRole, Messages, ToolCall, ToolCallFunction
from galileo_core.schemas.logging.llm import Message as GalileoCoreMessageClass
from galileo_core.schemas.logging.llm import MessageRole as GalileoCoreMessageRoleClass
from galileo_core.schemas.logging.llm import Messages as GalileoCoreMessagesClass
from galileo_core.schemas.logging.llm import ToolCall as GalileoCoreToolCallClass
from galileo_core.schemas.logging.llm import ToolCallFunction as GalileoCoreToolCallFunctionClass
from galileo_core.schemas.logging.span import (
    BaseStep,
    BaseWorkflowSpan,
    Document,
    LlmMetrics,
    LlmSpan,
    Message,
    MessageRole,
    Metrics,
    PydanticJsonEncoder,
    RetrieverSpan,
    Span,
    StepType,
    StepWithChildSpans,
    ToolSpan,
    WorkflowSpan,
)
from galileo_core.schemas.logging.span import BaseStep as GalileoCoreBaseStepClass
from galileo_core.schemas.logging.span import BaseWorkflowSpan as GalileoCoreBaseWorkflowSpanClass
from galileo_core.schemas.logging.span import Document as GalileoCoreDocumentClass
from galileo_core.schemas.logging.span import LlmMetrics as GalileoCoreLlmMetricsClass
from galileo_core.schemas.logging.span import LlmSpan as GalileoCoreLlmSpanClass
from galileo_core.schemas.logging.span import Message as GalileoCoreMessageClass
from galileo_core.schemas.logging.span import MessageRole as GalileoCoreMessageRoleClass
from galileo_core.schemas.logging.span import Metrics as GalileoCoreMetricsClass
from galileo_core.schemas.logging.span import PydanticJsonEncoder as GalileoCorePydanticJsonEncoderClass
from galileo_core.schemas.logging.span import RetrieverSpan as GalileoCoreRetrieverSpanClass
from galileo_core.schemas.logging.span import StepType as GalileoCoreStepTypeClass
from galileo_core.schemas.logging.span import StepWithChildSpans as GalileoCoreStepWithChildSpansClass
from galileo_core.schemas.logging.span import ToolSpan as GalileoCoreToolSpanClass
from galileo_core.schemas.logging.span import WorkflowSpan as GalileoCoreWorkflowSpanClass
from galileo_core.schemas.logging.step import BaseStep, Document, Message, Metrics, PydanticJsonEncoder, StepType
from galileo_core.schemas.logging.step import BaseStep as GalileoCoreBaseStepClass
from galileo_core.schemas.logging.step import Document as GalileoCoreDocumentClass
from galileo_core.schemas.logging.step import Message as GalileoCoreMessageClass
from galileo_core.schemas.logging.step import Metrics as GalileoCoreMetricsClass
from galileo_core.schemas.logging.step import PydanticJsonEncoder as GalileoCorePydanticJsonEncoderClass
from galileo_core.schemas.logging.step import StepType as GalileoCoreStepTypeClass
from galileo_core.schemas.logging.trace import BaseStep, BaseTrace, Span, StepType, StepWithChildSpans, Trace
from galileo_core.schemas.logging.trace import BaseStep as GalileoCoreBaseStepClass
from galileo_core.schemas.logging.trace import BaseTrace as GalileoCoreBaseTraceClass
from galileo_core.schemas.logging.trace import StepType as GalileoCoreStepTypeClass
from galileo_core.schemas.logging.trace import StepWithChildSpans as GalileoCoreStepWithChildSpansClass
from galileo_core.schemas.logging.trace import Trace as GalileoCoreTraceClass
from galileo_core.schemas.protect.action import (
    Action,
    ActionResult,
    ActionType,
    BaseAction,
    OverrideAction,
    PassthroughAction,
    SubscriptionConfig,
)
from galileo_core.schemas.protect.action import ActionResult as GalileoCoreActionResultClass
from galileo_core.schemas.protect.action import ActionType as GalileoCoreActionTypeClass
from galileo_core.schemas.protect.action import BaseAction as GalileoCoreBaseActionClass
from galileo_core.schemas.protect.action import OverrideAction as GalileoCoreOverrideActionClass
from galileo_core.schemas.protect.action import PassthroughAction as GalileoCorePassthroughActionClass
from galileo_core.schemas.protect.action import SubscriptionConfig as GalileoCoreSubscriptionConfigClass
from galileo_core.schemas.protect.execution_status import ExecutionStatus, ExecutionStatusMixIn
from galileo_core.schemas.protect.execution_status import ExecutionStatus as GalileoCoreExecutionStatusClass
from galileo_core.schemas.protect.execution_status import ExecutionStatusMixIn as GalileoCoreExecutionStatusMixInClass
from galileo_core.schemas.protect.metric import MetricComputation, MetricComputationStatus
from galileo_core.schemas.protect.metric import MetricComputation as GalileoCoreMetricComputationClass
from galileo_core.schemas.protect.metric import MetricComputationStatus as GalileoCoreMetricComputationStatusClass
from galileo_core.schemas.protect.payload import Payload
from galileo_core.schemas.protect.payload import Payload as GalileoCorePayloadClass
from galileo_core.schemas.protect.request import Payload, Request, Rule, RulesetsMixin
from galileo_core.schemas.protect.request import Payload as GalileoCorePayloadClass
from galileo_core.schemas.protect.request import Request as GalileoCoreRequestClass
from galileo_core.schemas.protect.request import Rule as GalileoCoreRuleClass
from galileo_core.schemas.protect.request import RulesetsMixin as GalileoCoreRulesetsMixinClass
from galileo_core.schemas.protect.response import (
    BaseTraceMetadata,
    ExecutionStatus,
    ExecutionStatusMixIn,
    Response,
    TraceMetadata,
)
from galileo_core.schemas.protect.response import BaseTraceMetadata as GalileoCoreBaseTraceMetadataClass
from galileo_core.schemas.protect.response import ExecutionStatus as GalileoCoreExecutionStatusClass
from galileo_core.schemas.protect.response import ExecutionStatusMixIn as GalileoCoreExecutionStatusMixInClass
from galileo_core.schemas.protect.response import Response as GalileoCoreResponseClass
from galileo_core.schemas.protect.response import TraceMetadata as GalileoCoreTraceMetadataClass
from galileo_core.schemas.protect.rule import Rule, RuleOperator
from galileo_core.schemas.protect.rule import Rule as GalileoCoreRuleClass
from galileo_core.schemas.protect.rule import RuleOperator as GalileoCoreRuleOperatorClass

############################################################
from galileo_core.schemas.protect.ruleset import Action, BaseAction, PassthroughAction, Rule, Ruleset, RulesetsMixin
from galileo_core.schemas.protect.ruleset import BaseAction as GalileoCoreBaseActionClass
from galileo_core.schemas.protect.ruleset import PassthroughAction as GalileoCorePassthroughActionClass
from galileo_core.schemas.protect.ruleset import Rule as GalileoCoreRuleClass
from galileo_core.schemas.protect.ruleset import Ruleset as GalileoCoreRulesetClass
from galileo_core.schemas.protect.ruleset import RulesetsMixin as GalileoCoreRulesetsMixinClass
from galileo_core.schemas.protect.stage import RulesetsMixin, Stage, StageType, StageWithRulesets
from galileo_core.schemas.protect.stage import RulesetsMixin as GalileoCoreRulesetsMixinClass
from galileo_core.schemas.protect.stage import Stage as GalileoCoreStageClass
from galileo_core.schemas.protect.stage import StageType as GalileoCoreStageTypeClass
from galileo_core.schemas.protect.stage import StageWithRulesets as GalileoCoreStageWithRulesetsClass
from galileo_core.schemas.protect.subscription_config import ExecutionStatus, SubscriptionConfig
from galileo_core.schemas.protect.subscription_config import ExecutionStatus as GalileoCoreExecutionStatusClass
from galileo_core.schemas.protect.subscription_config import SubscriptionConfig as GalileoCoreSubscriptionConfigClass
from galileo_core.schemas.shared.customized_scorer import CustomizedScorer, CustomizedScorerName
from galileo_core.schemas.shared.customized_scorer import CustomizedScorer as GalileoCoreCustomizedScorerClass
from galileo_core.schemas.shared.customized_scorer import CustomizedScorerName as GalileoCoreCustomizedScorerNameClass
from galileo_core.schemas.shared.document import Document
from galileo_core.schemas.shared.document import Document as GalileoCoreDocumentClass
from galileo_core.schemas.shared.filtered_collection import (
    CollectionFilter,
    CustomBooleanFilter,
    CustomNumberFilter,
    CustomUUIDFilter,
    DateFilter,
    EnumFilter,
    FilterBase,
    FilterType,
    IDFilter,
    MapFilter,
    Operator,
    QueryFilterV2,
    StringFilter,
)
from galileo_core.schemas.shared.filtered_collection import CollectionFilter as GalileoCoreCollectionFilterClass
from galileo_core.schemas.shared.filtered_collection import CustomBooleanFilter as GalileoCoreCustomBooleanFilterClass
from galileo_core.schemas.shared.filtered_collection import CustomNumberFilter as GalileoCoreCustomNumberFilterClass
from galileo_core.schemas.shared.filtered_collection import CustomUUIDFilter as GalileoCoreCustomUUIDFilterClass
from galileo_core.schemas.shared.filtered_collection import DateFilter as GalileoCoreDateFilterClass
from galileo_core.schemas.shared.filtered_collection import EnumFilter as GalileoCoreEnumFilterClass
from galileo_core.schemas.shared.filtered_collection import FilterBase as GalileoCoreFilterBaseClass
from galileo_core.schemas.shared.filtered_collection import FilterType as GalileoCoreFilterTypeClass
from galileo_core.schemas.shared.filtered_collection import IDFilter as GalileoCoreIDFilterClass
from galileo_core.schemas.shared.filtered_collection import MapFilter as GalileoCoreMapFilterClass
from galileo_core.schemas.shared.filtered_collection import Operator as GalileoCoreOperatorClass
from galileo_core.schemas.shared.filtered_collection import StringFilter as GalileoCoreStringFilterClass
from galileo_core.schemas.shared.message import Message, MessageRole
from galileo_core.schemas.shared.message import Message as GalileoCoreMessageClass
from galileo_core.schemas.shared.message import MessageRole as GalileoCoreMessageRoleClass
from galileo_core.schemas.shared.message_role import MessageRole
from galileo_core.schemas.shared.message_role import MessageRole as GalileoCoreMessageRoleClass
from galileo_core.schemas.shared.messages import Message, MessageRole, Messages
from galileo_core.schemas.shared.messages import Message as GalileoCoreMessageClass
from galileo_core.schemas.shared.messages import MessageRole as GalileoCoreMessageRoleClass
from galileo_core.schemas.shared.messages import Messages as GalileoCoreMessagesClass
from galileo_core.schemas.shared.scorers.base_configs import (
    BaseScorerConfig,
    GalileoScorerConfig,
    GeneratedScorerConfig,
    LunaOrPlusScorerTypeConfig,
    PlusScorerConfig,
    PlusScorerTypeConfig,
    PlusScorerWithNumJudgesConfig,
    RegisteredScorerConfig,
    ScorerJobFilter,
    ScorerName,
    ScorerNameValidatorMixin,
    ScorerType,
)
from galileo_core.schemas.shared.scorers.base_configs import BaseScorerConfig as GalileoCoreBaseScorerConfigClass
from galileo_core.schemas.shared.scorers.base_configs import GalileoScorerConfig as GalileoCoreGalileoScorerConfigClass
from galileo_core.schemas.shared.scorers.base_configs import (
    GeneratedScorerConfig as GalileoCoreGeneratedScorerConfigClass,
)
from galileo_core.schemas.shared.scorers.base_configs import (
    LunaOrPlusScorerTypeConfig as GalileoCoreLunaOrPlusScorerTypeConfigClass,
)
from galileo_core.schemas.shared.scorers.base_configs import PlusScorerConfig as GalileoCorePlusScorerConfigClass
from galileo_core.schemas.shared.scorers.base_configs import (
    PlusScorerTypeConfig as GalileoCorePlusScorerTypeConfigClass,
)
from galileo_core.schemas.shared.scorers.base_configs import (
    PlusScorerWithNumJudgesConfig as GalileoCorePlusScorerWithNumJudgesConfigClass,
)
from galileo_core.schemas.shared.scorers.base_configs import (
    RegisteredScorerConfig as GalileoCoreRegisteredScorerConfigClass,
)
from galileo_core.schemas.shared.scorers.base_configs import ScorerName as GalileoCoreScorerNameClass
from galileo_core.schemas.shared.scorers.base_configs import (
    ScorerNameValidatorMixin as GalileoCoreScorerNameValidatorMixinClass,
)
from galileo_core.schemas.shared.scorers.base_configs import ScorerType as GalileoCoreScorerTypeClass
from galileo_core.schemas.shared.scorers.chain_aggregation import ChainAggregationStrategy
from galileo_core.schemas.shared.scorers.chain_aggregation import (
    ChainAggregationStrategy as GalileoCoreChainAggregationStrategyClass,
)
from galileo_core.schemas.shared.scorers.filters import (
    MapFilter,
    MetadataFilter,
    NodeNameFilter,
    ScorerJobFilter,
    ScorerJobFilterNames,
    StringFilter,
)
from galileo_core.schemas.shared.scorers.filters import MapFilter as GalileoCoreMapFilterClass
from galileo_core.schemas.shared.scorers.filters import MetadataFilter as GalileoCoreMetadataFilterClass
from galileo_core.schemas.shared.scorers.filters import NodeNameFilter as GalileoCoreNodeNameFilterClass
from galileo_core.schemas.shared.scorers.filters import ScorerJobFilterNames as GalileoCoreScorerJobFilterNamesClass
from galileo_core.schemas.shared.scorers.filters import StringFilter as GalileoCoreStringFilterClass
from galileo_core.schemas.shared.scorers.mixins import ScorerNameValidatorMixin
from galileo_core.schemas.shared.scorers.mixins import (
    ScorerNameValidatorMixin as GalileoCoreScorerNameValidatorMixinClass,
)
from galileo_core.schemas.shared.scorers.scorer_configuration import (
    GalileoScorer,
    GeneratedScorerConfig,
    RegisteredScorerConfig,
    ScorerConfiguration,
)
from galileo_core.schemas.shared.scorers.scorer_configuration import (
    GeneratedScorerConfig as GalileoCoreGeneratedScorerConfigClass,
)
from galileo_core.schemas.shared.scorers.scorer_configuration import (
    RegisteredScorerConfig as GalileoCoreRegisteredScorerConfigClass,
)
from galileo_core.schemas.shared.scorers.scorer_configuration import (
    ScorerConfiguration as GalileoCoreScorerConfigurationClass,
)
from galileo_core.schemas.shared.scorers.scorer_name import ScorerName
from galileo_core.schemas.shared.scorers.scorer_name import ScorerName as GalileoCoreScorerNameClass
from galileo_core.schemas.shared.scorers.scorer_type import ScorerType
from galileo_core.schemas.shared.scorers.scorer_type import ScorerType as GalileoCoreScorerTypeClass
from galileo_core.schemas.shared.scorers.scorers import (
    AgenticSessionSuccessScorer,
    AgenticWorkflowSuccessScorer,
    BleuScorer,
    ChunkAttributionUtilizationScorer,
    CompletenessScorer,
    ContextAdherenceScorer,
    ContextRelevanceScorer,
    CorrectnessScorer,
    GalileoScorer,
    GalileoScorerConfig,
    GroundTruthAdherenceScorer,
    InputPIIScorer,
    InputSexistScorer,
    InputToneScorer,
    InputToxicityScorer,
    InstructionAdherenceScorer,
    LunaOrPlusScorerTypeConfig,
    OutputPIIScorer,
    OutputSexistScorer,
    OutputToneScorer,
    OutputToxicityScorer,
    PlusScorerConfig,
    PlusScorerTypeConfig,
    PlusScorerWithNumJudgesConfig,
    PromptInjectionScorer,
    PromptPerplexityScorer,
    RougeScorer,
    ScorerName,
    ToolErrorRateScorer,
    ToolSelectionQualityScorer,
    UncertaintyScorer,
)
from galileo_core.schemas.shared.scorers.scorers import (
    AgenticSessionSuccessScorer as GalileoCoreAgenticSessionSuccessScorerClass,
)
from galileo_core.schemas.shared.scorers.scorers import (
    AgenticWorkflowSuccessScorer as GalileoCoreAgenticWorkflowSuccessScorerClass,
)
from galileo_core.schemas.shared.scorers.scorers import BleuScorer as GalileoCoreBleuScorerClass
from galileo_core.schemas.shared.scorers.scorers import (
    ChunkAttributionUtilizationScorer as GalileoCoreChunkAttributionUtilizationScorerClass,
)
from galileo_core.schemas.shared.scorers.scorers import CompletenessScorer as GalileoCoreCompletenessScorerClass
from galileo_core.schemas.shared.scorers.scorers import ContextAdherenceScorer as GalileoCoreContextAdherenceScorerClass
from galileo_core.schemas.shared.scorers.scorers import ContextRelevanceScorer as GalileoCoreContextRelevanceScorerClass
from galileo_core.schemas.shared.scorers.scorers import CorrectnessScorer as GalileoCoreCorrectnessScorerClass
from galileo_core.schemas.shared.scorers.scorers import GalileoScorerConfig as GalileoCoreGalileoScorerConfigClass
from galileo_core.schemas.shared.scorers.scorers import (
    GroundTruthAdherenceScorer as GalileoCoreGroundTruthAdherenceScorerClass,
)
from galileo_core.schemas.shared.scorers.scorers import InputPIIScorer as GalileoCoreInputPIIScorerClass
from galileo_core.schemas.shared.scorers.scorers import InputSexistScorer as GalileoCoreInputSexistScorerClass
from galileo_core.schemas.shared.scorers.scorers import InputToneScorer as GalileoCoreInputToneScorerClass
from galileo_core.schemas.shared.scorers.scorers import InputToxicityScorer as GalileoCoreInputToxicityScorerClass
from galileo_core.schemas.shared.scorers.scorers import (
    InstructionAdherenceScorer as GalileoCoreInstructionAdherenceScorerClass,
)
from galileo_core.schemas.shared.scorers.scorers import (
    LunaOrPlusScorerTypeConfig as GalileoCoreLunaOrPlusScorerTypeConfigClass,
)
from galileo_core.schemas.shared.scorers.scorers import OutputPIIScorer as GalileoCoreOutputPIIScorerClass
from galileo_core.schemas.shared.scorers.scorers import OutputSexistScorer as GalileoCoreOutputSexistScorerClass
from galileo_core.schemas.shared.scorers.scorers import OutputToneScorer as GalileoCoreOutputToneScorerClass
from galileo_core.schemas.shared.scorers.scorers import OutputToxicityScorer as GalileoCoreOutputToxicityScorerClass
from galileo_core.schemas.shared.scorers.scorers import PlusScorerConfig as GalileoCorePlusScorerConfigClass
from galileo_core.schemas.shared.scorers.scorers import PlusScorerTypeConfig as GalileoCorePlusScorerTypeConfigClass
from galileo_core.schemas.shared.scorers.scorers import (
    PlusScorerWithNumJudgesConfig as GalileoCorePlusScorerWithNumJudgesConfigClass,
)
from galileo_core.schemas.shared.scorers.scorers import PromptInjectionScorer as GalileoCorePromptInjectionScorerClass
from galileo_core.schemas.shared.scorers.scorers import PromptPerplexityScorer as GalileoCorePromptPerplexityScorerClass
from galileo_core.schemas.shared.scorers.scorers import RougeScorer as GalileoCoreRougeScorerClass
from galileo_core.schemas.shared.scorers.scorers import ScorerName as GalileoCoreScorerNameClass
from galileo_core.schemas.shared.scorers.scorers import ToolErrorRateScorer as GalileoCoreToolErrorRateScorerClass
from galileo_core.schemas.shared.scorers.scorers import (
    ToolSelectionQualityScorer as GalileoCoreToolSelectionQualityScorerClass,
)
from galileo_core.schemas.shared.scorers.scorers import UncertaintyScorer as GalileoCoreUncertaintyScorerClass
from galileo_core.schemas.shared.traces.trace import (
    LlmSpan,
    RetrieverSpan,
    StepWithChildSpans,
    ToolSpan,
    Trace,
    Traces,
    WorkflowSpan,
)
from galileo_core.schemas.shared.traces.trace import LlmSpan as GalileoCoreLlmSpanClass
from galileo_core.schemas.shared.traces.trace import RetrieverSpan as GalileoCoreRetrieverSpanClass
from galileo_core.schemas.shared.traces.trace import StepWithChildSpans as GalileoCoreStepWithChildSpansClass
from galileo_core.schemas.shared.traces.trace import ToolSpan as GalileoCoreToolSpanClass
from galileo_core.schemas.shared.traces.trace import Trace as GalileoCoreTraceClass
from galileo_core.schemas.shared.traces.trace import Traces as GalileoCoreTracesClass
from galileo_core.schemas.shared.traces.trace import WorkflowSpan as GalileoCoreWorkflowSpanClass
from galileo_core.schemas.shared.traces.types import (
    BaseStep,
    BaseStepWithChildren,
    LlmSpan,
    LlmStep,
    NodeType,
    RetrieverSpan,
    RetrieverStep,
    Span,
    SpanWithParentStep,
    StepWithChildSpans,
    ToolSpan,
    ToolStep,
    Trace,
    WorkflowSpan,
)
from galileo_core.schemas.shared.traces.types import BaseStep as GalileoCoreBaseStepClass
from galileo_core.schemas.shared.traces.types import BaseStepWithChildren as GalileoCoreBaseStepWithChildrenClass
from galileo_core.schemas.shared.traces.types import LlmSpan as GalileoCoreLlmSpanClass
from galileo_core.schemas.shared.traces.types import LlmStep as GalileoCoreLlmStepClass
from galileo_core.schemas.shared.traces.types import NodeType as GalileoCoreNodeTypeClass
from galileo_core.schemas.shared.traces.types import RetrieverSpan as GalileoCoreRetrieverSpanClass
from galileo_core.schemas.shared.traces.types import RetrieverStep as GalileoCoreRetrieverStepClass
from galileo_core.schemas.shared.traces.types import SpanWithParentStep as GalileoCoreSpanWithParentStepClass
from galileo_core.schemas.shared.traces.types import StepWithChildSpans as GalileoCoreStepWithChildSpansClass
from galileo_core.schemas.shared.traces.types import ToolSpan as GalileoCoreToolSpanClass
from galileo_core.schemas.shared.traces.types import ToolStep as GalileoCoreToolStepClass
from galileo_core.schemas.shared.traces.types import Trace as GalileoCoreTraceClass
from galileo_core.schemas.shared.traces.types import WorkflowSpan as GalileoCoreWorkflowSpanClass
from galileo_core.schemas.shared.traces_logger import (
    Document,
    LlmMetrics,
    LlmSpan,
    Metrics,
    PydanticJsonEncoder,
    RetrieverSpan,
    Span,
    StepWithChildSpans,
    ToolSpan,
    Trace,
    TracesLogger,
    WorkflowSpan,
)
from galileo_core.schemas.shared.traces_logger import Document as GalileoCoreDocumentClass
from galileo_core.schemas.shared.traces_logger import LlmMetrics as GalileoCoreLlmMetricsClass
from galileo_core.schemas.shared.traces_logger import LlmSpan as GalileoCoreLlmSpanClass
from galileo_core.schemas.shared.traces_logger import Metrics as GalileoCoreMetricsClass
from galileo_core.schemas.shared.traces_logger import PydanticJsonEncoder as GalileoCorePydanticJsonEncoderClass
from galileo_core.schemas.shared.traces_logger import RetrieverSpan as GalileoCoreRetrieverSpanClass
from galileo_core.schemas.shared.traces_logger import StepWithChildSpans as GalileoCoreStepWithChildSpansClass
from galileo_core.schemas.shared.traces_logger import ToolSpan as GalileoCoreToolSpanClass
from galileo_core.schemas.shared.traces_logger import Trace as GalileoCoreTraceClass
from galileo_core.schemas.shared.traces_logger import TracesLogger as GalileoCoreTracesLoggerClass
from galileo_core.schemas.shared.traces_logger import WorkflowSpan as GalileoCoreWorkflowSpanClass
from galileo_core.schemas.shared.workflows.node_type import NodeType
from galileo_core.schemas.shared.workflows.node_type import NodeType as GalileoCoreNodeTypeClass
from galileo_core.schemas.shared.workflows.step import (
    AgentStep,
    AWorkflowStep,
    BaseStep,
    BaseStepWithChildren,
    ChainStep,
    Document,
    LlmStep,
    Message,
    NodeType,
    Payload,
    PydanticJsonEncoder,
    Response,
    RetrieverStep,
    StepWithChildren,
    ToolStep,
    WorkflowStep,
)
from galileo_core.schemas.shared.workflows.step import AgentStep as GalileoCoreAgentStepClass
from galileo_core.schemas.shared.workflows.step import BaseStep as GalileoCoreBaseStepClass
from galileo_core.schemas.shared.workflows.step import BaseStepWithChildren as GalileoCoreBaseStepWithChildrenClass
from galileo_core.schemas.shared.workflows.step import ChainStep as GalileoCoreChainStepClass
from galileo_core.schemas.shared.workflows.step import Document as GalileoCoreDocumentClass
from galileo_core.schemas.shared.workflows.step import LlmStep as GalileoCoreLlmStepClass
from galileo_core.schemas.shared.workflows.step import Message as GalileoCoreMessageClass
from galileo_core.schemas.shared.workflows.step import NodeType as GalileoCoreNodeTypeClass
from galileo_core.schemas.shared.workflows.step import Payload as GalileoCorePayloadClass
from galileo_core.schemas.shared.workflows.step import PydanticJsonEncoder as GalileoCorePydanticJsonEncoderClass
from galileo_core.schemas.shared.workflows.step import Response as GalileoCoreResponseClass
from galileo_core.schemas.shared.workflows.step import RetrieverStep as GalileoCoreRetrieverStepClass
from galileo_core.schemas.shared.workflows.step import StepWithChildren as GalileoCoreStepWithChildrenClass
from galileo_core.schemas.shared.workflows.step import ToolStep as GalileoCoreToolStepClass
from galileo_core.schemas.shared.workflows.step import WorkflowStep as GalileoCoreWorkflowStepClass
from galileo_core.schemas.shared.workflows.workflow import (
    AgentStep,
    AWorkflowStep,
    LlmStep,
    Payload,
    Response,
    RetrieverStep,
    StepWithChildren,
    ToolStep,
    Workflows,
    WorkflowStep,
)
from galileo_core.schemas.shared.workflows.workflow import AgentStep as GalileoCoreAgentStepClass
from galileo_core.schemas.shared.workflows.workflow import LlmStep as GalileoCoreLlmStepClass
from galileo_core.schemas.shared.workflows.workflow import Payload as GalileoCorePayloadClass
from galileo_core.schemas.shared.workflows.workflow import Response as GalileoCoreResponseClass
from galileo_core.schemas.shared.workflows.workflow import RetrieverStep as GalileoCoreRetrieverStepClass
from galileo_core.schemas.shared.workflows.workflow import StepWithChildren as GalileoCoreStepWithChildrenClass
from galileo_core.schemas.shared.workflows.workflow import ToolStep as GalileoCoreToolStepClass
from galileo_core.schemas.shared.workflows.workflow import Workflows as GalileoCoreWorkflowsClass
from galileo_core.schemas.shared.workflows.workflow import WorkflowStep as GalileoCoreWorkflowStepClass
from galileo_core.utils.dataset import DatasetFormat
from galileo_core.utils.dataset import DatasetFormat as GalileoCoreDatasetFormatClass
from galileo_core.utils.json import PydanticJsonEncoder
from galileo_core.utils.json import PydanticJsonEncoder as GalileoCorePydanticJsonEncoderClass
from galileo_core.utils.scorer_validation import ChainAggregationStrategy, ExecutionError, NodeType
from galileo_core.utils.scorer_validation import ChainAggregationStrategy as GalileoCoreChainAggregationStrategyClass
from galileo_core.utils.scorer_validation import ExecutionError as GalileoCoreExecutionErrorClass
from galileo_core.utils.scorer_validation import NodeType as GalileoCoreNodeTypeClass

if issubclass(GalileoCoreConfigEnvironmentVariablesClass, BaseModel):

    class ConfigEnvironmentVariables(GalileoCoreConfigEnvironmentVariablesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ConfigEnvironmentVariables":
            return cls.model_validate(src_dict)

    ConfigEnvironmentVariables.model_rebuild()
else:
    ConfigEnvironmentVariables = GalileoCoreConfigEnvironmentVariablesClass


if issubclass(GalileoCoreProcessingHeadersClass, BaseModel):

    class ProcessingHeaders(GalileoCoreProcessingHeadersClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ProcessingHeaders":
            return cls.model_validate(src_dict)

    ProcessingHeaders.model_rebuild()
else:
    ProcessingHeaders = GalileoCoreProcessingHeadersClass


if issubclass(GalileoCoreDatasetFormatClass, BaseModel):

    class DatasetFormat(GalileoCoreDatasetFormatClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "DatasetFormat":
            return cls.model_validate(src_dict)

    DatasetFormat.model_rebuild()
else:
    DatasetFormat = GalileoCoreDatasetFormatClass


if issubclass(GalileoCoreHttpHeadersClass, BaseModel):

    class HttpHeaders(GalileoCoreHttpHeadersClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "HttpHeaders":
            return cls.model_validate(src_dict)

    HttpHeaders.model_rebuild()
else:
    HttpHeaders = GalileoCoreHttpHeadersClass


if issubclass(GalileoCoreRequestMethodClass, BaseModel):

    class RequestMethod(GalileoCoreRequestMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RequestMethod":
            return cls.model_validate(src_dict)

    RequestMethod.model_rebuild()
else:
    RequestMethod = GalileoCoreRequestMethodClass


if issubclass(GalileoCoreRoutesClass, BaseModel):

    class Routes(GalileoCoreRoutesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Routes":
            return cls.model_validate(src_dict)

    Routes.model_rebuild()
else:
    Routes = GalileoCoreRoutesClass


if issubclass(GalileoCoreChainAggregationStrategyClass, BaseModel):

    class ChainAggregationStrategy(GalileoCoreChainAggregationStrategyClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ChainAggregationStrategy":
            return cls.model_validate(src_dict)

    ChainAggregationStrategy.model_rebuild()
else:
    ChainAggregationStrategy = GalileoCoreChainAggregationStrategyClass


if issubclass(GalileoCoreExecutionErrorClass, BaseModel):

    class ExecutionError(GalileoCoreExecutionErrorClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ExecutionError":
            return cls.model_validate(src_dict)

    ExecutionError.model_rebuild()
else:
    ExecutionError = GalileoCoreExecutionErrorClass


if issubclass(GalileoCoreNodeTypeClass, BaseModel):

    class NodeType(GalileoCoreNodeTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "NodeType":
            return cls.model_validate(src_dict)

    NodeType.model_rebuild()
else:
    NodeType = GalileoCoreNodeTypeClass


if issubclass(GalileoCoreDatasetFormatClass, BaseModel):

    class DatasetFormat(GalileoCoreDatasetFormatClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "DatasetFormat":
            return cls.model_validate(src_dict)

    DatasetFormat.model_rebuild()
else:
    DatasetFormat = GalileoCoreDatasetFormatClass


if issubclass(GalileoCorePydanticJsonEncoderClass, BaseModel):

    class PydanticJsonEncoder(GalileoCorePydanticJsonEncoderClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PydanticJsonEncoder":
            return cls.model_validate(src_dict)

    PydanticJsonEncoder.model_rebuild()
else:
    PydanticJsonEncoder = GalileoCorePydanticJsonEncoderClass


if issubclass(GalileoCoreBaseGalileoExceptionClass, BaseModel):

    class BaseGalileoException(GalileoCoreBaseGalileoExceptionClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseGalileoException":
            return cls.model_validate(src_dict)

    BaseGalileoException.model_rebuild()
else:
    BaseGalileoException = GalileoCoreBaseGalileoExceptionClass


if issubclass(GalileoCoreExecutionErrorClass, BaseModel):

    class ExecutionError(GalileoCoreExecutionErrorClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ExecutionError":
            return cls.model_validate(src_dict)

    ExecutionError.model_rebuild()
else:
    ExecutionError = GalileoCoreExecutionErrorClass


if issubclass(GalileoCoreGalileoHTTPExceptionClass, BaseModel):

    class GalileoHTTPException(GalileoCoreGalileoHTTPExceptionClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoHTTPException":
            return cls.model_validate(src_dict)

    GalileoHTTPException.model_rebuild()
else:
    GalileoHTTPException = GalileoCoreGalileoHTTPExceptionClass


if issubclass(GalileoCoreBaseGalileoExceptionClass, BaseModel):

    class BaseGalileoException(GalileoCoreBaseGalileoExceptionClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseGalileoException":
            return cls.model_validate(src_dict)

    BaseGalileoException.model_rebuild()
else:
    BaseGalileoException = GalileoCoreBaseGalileoExceptionClass


if issubclass(GalileoCoreApiClientClass, BaseModel):

    class ApiClient(GalileoCoreApiClientClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ApiClient":
            return cls.model_validate(src_dict)

    ApiClient.model_rebuild()
else:
    ApiClient = GalileoCoreApiClientClass


if issubclass(GalileoCoreGalileoConfigClass, BaseModel):

    class GalileoConfig(GalileoCoreGalileoConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoConfig":
            return cls.model_validate(src_dict)

    GalileoConfig.model_rebuild()
else:
    GalileoConfig = GalileoCoreGalileoConfigClass


if issubclass(GalileoCoreRequestMethodClass, BaseModel):

    class RequestMethod(GalileoCoreRequestMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RequestMethod":
            return cls.model_validate(src_dict)

    RequestMethod.model_rebuild()
else:
    RequestMethod = GalileoCoreRequestMethodClass


if issubclass(GalileoCoreRoutesClass, BaseModel):

    class Routes(GalileoCoreRoutesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Routes":
            return cls.model_validate(src_dict)

    Routes.model_rebuild()
else:
    Routes = GalileoCoreRoutesClass


if issubclass(GalileoCoreUserClass, BaseModel):

    class User(GalileoCoreUserClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "User":
            return cls.model_validate(src_dict)

    User.model_rebuild()
else:
    User = GalileoCoreUserClass


if issubclass(GalileoCoreAuthMethodClass, BaseModel):

    class AuthMethod(GalileoCoreAuthMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AuthMethod":
            return cls.model_validate(src_dict)

    AuthMethod.model_rebuild()
else:
    AuthMethod = GalileoCoreAuthMethodClass


if issubclass(GalileoCoreInviteUsersRequestClass, BaseModel):

    class InviteUsersRequest(GalileoCoreInviteUsersRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "InviteUsersRequest":
            return cls.model_validate(src_dict)

    InviteUsersRequest.model_rebuild()
else:
    InviteUsersRequest = GalileoCoreInviteUsersRequestClass


if issubclass(GalileoCoreUpdateUserRoleRequestClass, BaseModel):

    class UpdateUserRoleRequest(GalileoCoreUpdateUserRoleRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UpdateUserRoleRequest":
            return cls.model_validate(src_dict)

    UpdateUserRoleRequest.model_rebuild()
else:
    UpdateUserRoleRequest = GalileoCoreUpdateUserRoleRequestClass


if issubclass(GalileoCoreUserClass, BaseModel):

    class User(GalileoCoreUserClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "User":
            return cls.model_validate(src_dict)

    User.model_rebuild()
else:
    User = GalileoCoreUserClass


if issubclass(GalileoCoreUserRoleClass, BaseModel):

    class UserRole(GalileoCoreUserRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UserRole":
            return cls.model_validate(src_dict)

    UserRole.model_rebuild()
else:
    UserRole = GalileoCoreUserRoleClass


if issubclass(GalileoCoreSystemRoleClass, BaseModel):

    class SystemRole(GalileoCoreSystemRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "SystemRole":
            return cls.model_validate(src_dict)

    SystemRole.model_rebuild()
else:
    SystemRole = GalileoCoreSystemRoleClass


if issubclass(GalileoCoreUserRoleClass, BaseModel):

    class UserRole(GalileoCoreUserRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UserRole":
            return cls.model_validate(src_dict)

    UserRole.model_rebuild()
else:
    UserRole = GalileoCoreUserRoleClass


if issubclass(GalileoCoreGroupRoleClass, BaseModel):

    class GroupRole(GalileoCoreGroupRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GroupRole":
            return cls.model_validate(src_dict)

    GroupRole.model_rebuild()
else:
    GroupRole = GalileoCoreGroupRoleClass


if issubclass(GalileoCoreCollaboratorRoleClass, BaseModel):

    class CollaboratorRole(GalileoCoreCollaboratorRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CollaboratorRole":
            return cls.model_validate(src_dict)

    CollaboratorRole.model_rebuild()
else:
    CollaboratorRole = GalileoCoreCollaboratorRoleClass


if issubclass(GalileoCoreUserProjectCollaboratorRequestClass, BaseModel):

    class UserProjectCollaboratorRequest(GalileoCoreUserProjectCollaboratorRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UserProjectCollaboratorRequest":
            return cls.model_validate(src_dict)

    UserProjectCollaboratorRequest.model_rebuild()
else:
    UserProjectCollaboratorRequest = GalileoCoreUserProjectCollaboratorRequestClass


if issubclass(GalileoCoreUserProjectCollaboratorResponseClass, BaseModel):

    class UserProjectCollaboratorResponse(GalileoCoreUserProjectCollaboratorResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UserProjectCollaboratorResponse":
            return cls.model_validate(src_dict)

    UserProjectCollaboratorResponse.model_rebuild()
else:
    UserProjectCollaboratorResponse = GalileoCoreUserProjectCollaboratorResponseClass


if issubclass(GalileoCoreCollaboratorRoleClass, BaseModel):

    class CollaboratorRole(GalileoCoreCollaboratorRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CollaboratorRole":
            return cls.model_validate(src_dict)

    CollaboratorRole.model_rebuild()
else:
    CollaboratorRole = GalileoCoreCollaboratorRoleClass


if issubclass(GalileoCoreApiKeyResponseClass, BaseModel):

    class ApiKeyResponse(GalileoCoreApiKeyResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ApiKeyResponse":
            return cls.model_validate(src_dict)

    ApiKeyResponse.model_rebuild()
else:
    ApiKeyResponse = GalileoCoreApiKeyResponseClass


if issubclass(GalileoCoreBaseApiKeyClass, BaseModel):

    class BaseApiKey(GalileoCoreBaseApiKeyClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseApiKey":
            return cls.model_validate(src_dict)

    BaseApiKey.model_rebuild()
else:
    BaseApiKey = GalileoCoreBaseApiKeyClass


if issubclass(GalileoCoreCollaboratorRoleClass, BaseModel):

    class CollaboratorRole(GalileoCoreCollaboratorRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CollaboratorRole":
            return cls.model_validate(src_dict)

    CollaboratorRole.model_rebuild()
else:
    CollaboratorRole = GalileoCoreCollaboratorRoleClass


if issubclass(GalileoCoreCreateApiKeyRequestClass, BaseModel):

    class CreateApiKeyRequest(GalileoCoreCreateApiKeyRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CreateApiKeyRequest":
            return cls.model_validate(src_dict)

    CreateApiKeyRequest.model_rebuild()
else:
    CreateApiKeyRequest = GalileoCoreCreateApiKeyRequestClass


if issubclass(GalileoCoreCreateApiKeyResponseClass, BaseModel):

    class CreateApiKeyResponse(GalileoCoreCreateApiKeyResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CreateApiKeyResponse":
            return cls.model_validate(src_dict)

    CreateApiKeyResponse.model_rebuild()
else:
    CreateApiKeyResponse = GalileoCoreCreateApiKeyResponseClass


if issubclass(GalileoCoreBaseDatasetRequestClass, BaseModel):

    class BaseDatasetRequest(GalileoCoreBaseDatasetRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseDatasetRequest":
            return cls.model_validate(src_dict)

    BaseDatasetRequest.model_rebuild()
else:
    BaseDatasetRequest = GalileoCoreBaseDatasetRequestClass


if issubclass(GalileoCoreDatasetClass, BaseModel):

    class Dataset(GalileoCoreDatasetClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Dataset":
            return cls.model_validate(src_dict)

    Dataset.model_rebuild()
else:
    Dataset = GalileoCoreDatasetClass


if issubclass(GalileoCoreDatasetFormatClass, BaseModel):

    class DatasetFormat(GalileoCoreDatasetFormatClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "DatasetFormat":
            return cls.model_validate(src_dict)

    DatasetFormat.model_rebuild()
else:
    DatasetFormat = GalileoCoreDatasetFormatClass


if issubclass(GalileoCoreUploadDatasetRequestClass, BaseModel):

    class UploadDatasetRequest(GalileoCoreUploadDatasetRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UploadDatasetRequest":
            return cls.model_validate(src_dict)

    UploadDatasetRequest.model_rebuild()
else:
    UploadDatasetRequest = GalileoCoreUploadDatasetRequestClass


if issubclass(GalileoCoreGroupVisibilityClass, BaseModel):

    class GroupVisibility(GalileoCoreGroupVisibilityClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GroupVisibility":
            return cls.model_validate(src_dict)

    GroupVisibility.model_rebuild()
else:
    GroupVisibility = GalileoCoreGroupVisibilityClass


if issubclass(GalileoCoreAddGroupMemberRequestClass, BaseModel):

    class AddGroupMemberRequest(GalileoCoreAddGroupMemberRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AddGroupMemberRequest":
            return cls.model_validate(src_dict)

    AddGroupMemberRequest.model_rebuild()
else:
    AddGroupMemberRequest = GalileoCoreAddGroupMemberRequestClass


if issubclass(GalileoCoreAddGroupMemberResponseClass, BaseModel):

    class AddGroupMemberResponse(GalileoCoreAddGroupMemberResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AddGroupMemberResponse":
            return cls.model_validate(src_dict)

    AddGroupMemberResponse.model_rebuild()
else:
    AddGroupMemberResponse = GalileoCoreAddGroupMemberResponseClass


if issubclass(GalileoCoreCreateGroupRequestClass, BaseModel):

    class CreateGroupRequest(GalileoCoreCreateGroupRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CreateGroupRequest":
            return cls.model_validate(src_dict)

    CreateGroupRequest.model_rebuild()
else:
    CreateGroupRequest = GalileoCoreCreateGroupRequestClass


if issubclass(GalileoCoreCreateGroupResponseClass, BaseModel):

    class CreateGroupResponse(GalileoCoreCreateGroupResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CreateGroupResponse":
            return cls.model_validate(src_dict)

    CreateGroupResponse.model_rebuild()
else:
    CreateGroupResponse = GalileoCoreCreateGroupResponseClass


if issubclass(GalileoCoreGroupRoleClass, BaseModel):

    class GroupRole(GalileoCoreGroupRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GroupRole":
            return cls.model_validate(src_dict)

    GroupRole.model_rebuild()
else:
    GroupRole = GalileoCoreGroupRoleClass


if issubclass(GalileoCoreGroupVisibilityClass, BaseModel):

    class GroupVisibility(GalileoCoreGroupVisibilityClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GroupVisibility":
            return cls.model_validate(src_dict)

    GroupVisibility.model_rebuild()
else:
    GroupVisibility = GalileoCoreGroupVisibilityClass


if issubclass(GalileoCoreAuthMethodClass, BaseModel):

    class AuthMethod(GalileoCoreAuthMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AuthMethod":
            return cls.model_validate(src_dict)

    AuthMethod.model_rebuild()
else:
    AuthMethod = GalileoCoreAuthMethodClass


if issubclass(GalileoCorePaginationRequestClass, BaseModel):

    class PaginationRequest(GalileoCorePaginationRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PaginationRequest":
            return cls.model_validate(src_dict)

    PaginationRequest.model_rebuild()
else:
    PaginationRequest = GalileoCorePaginationRequestClass


if issubclass(GalileoCorePaginationResponseClass, BaseModel):

    class PaginationResponse(GalileoCorePaginationResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PaginationResponse":
            return cls.model_validate(src_dict)

    PaginationResponse.model_rebuild()
else:
    PaginationResponse = GalileoCorePaginationResponseClass


if issubclass(GalileoCoreCollaboratorRoleClass, BaseModel):

    class CollaboratorRole(GalileoCoreCollaboratorRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CollaboratorRole":
            return cls.model_validate(src_dict)

    CollaboratorRole.model_rebuild()
else:
    CollaboratorRole = GalileoCoreCollaboratorRoleClass


if issubclass(GalileoCoreGroupProjectCollaboratorRequestClass, BaseModel):

    class GroupProjectCollaboratorRequest(GalileoCoreGroupProjectCollaboratorRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GroupProjectCollaboratorRequest":
            return cls.model_validate(src_dict)

    GroupProjectCollaboratorRequest.model_rebuild()
else:
    GroupProjectCollaboratorRequest = GalileoCoreGroupProjectCollaboratorRequestClass


if issubclass(GalileoCoreGroupProjectCollaboratorResponseClass, BaseModel):

    class GroupProjectCollaboratorResponse(GalileoCoreGroupProjectCollaboratorResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GroupProjectCollaboratorResponse":
            return cls.model_validate(src_dict)

    GroupProjectCollaboratorResponse.model_rebuild()
else:
    GroupProjectCollaboratorResponse = GalileoCoreGroupProjectCollaboratorResponseClass


if issubclass(GalileoCoreCreateProjectRequestClass, BaseModel):

    class CreateProjectRequest(GalileoCoreCreateProjectRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CreateProjectRequest":
            return cls.model_validate(src_dict)

    CreateProjectRequest.model_rebuild()
else:
    CreateProjectRequest = GalileoCoreCreateProjectRequestClass


if issubclass(GalileoCoreProjectResponseClass, BaseModel):

    class ProjectResponse(GalileoCoreProjectResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ProjectResponse":
            return cls.model_validate(src_dict)

    ProjectResponse.model_rebuild()
else:
    ProjectResponse = GalileoCoreProjectResponseClass


if issubclass(GalileoCoreProjectTypeClass, BaseModel):

    class ProjectType(GalileoCoreProjectTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ProjectType":
            return cls.model_validate(src_dict)

    ProjectType.model_rebuild()
else:
    ProjectType = GalileoCoreProjectTypeClass


if issubclass(GalileoCoreBaseActionClass, BaseModel):

    class BaseAction(GalileoCoreBaseActionClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseAction":
            return cls.model_validate(src_dict)

    BaseAction.model_rebuild()
else:
    BaseAction = GalileoCoreBaseActionClass


if issubclass(GalileoCorePassthroughActionClass, BaseModel):

    class PassthroughAction(GalileoCorePassthroughActionClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PassthroughAction":
            return cls.model_validate(src_dict)

    PassthroughAction.model_rebuild()
else:
    PassthroughAction = GalileoCorePassthroughActionClass


if issubclass(GalileoCoreRuleClass, BaseModel):

    class Rule(GalileoCoreRuleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Rule":
            return cls.model_validate(src_dict)

    Rule.model_rebuild()
else:
    Rule = GalileoCoreRuleClass


if issubclass(GalileoCoreRulesetClass, BaseModel):

    class Ruleset(GalileoCoreRulesetClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Ruleset":
            return cls.model_validate(src_dict)

    Ruleset.model_rebuild()
else:
    Ruleset = GalileoCoreRulesetClass


if issubclass(GalileoCoreRulesetsMixinClass, BaseModel):

    class RulesetsMixin(GalileoCoreRulesetsMixinClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RulesetsMixin":
            return cls.model_validate(src_dict)

    RulesetsMixin.model_rebuild()
else:
    RulesetsMixin = GalileoCoreRulesetsMixinClass


if issubclass(GalileoCoreExecutionStatusClass, BaseModel):

    class ExecutionStatus(GalileoCoreExecutionStatusClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ExecutionStatus":
            return cls.model_validate(src_dict)

    ExecutionStatus.model_rebuild()
else:
    ExecutionStatus = GalileoCoreExecutionStatusClass


if issubclass(GalileoCoreSubscriptionConfigClass, BaseModel):

    class SubscriptionConfig(GalileoCoreSubscriptionConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "SubscriptionConfig":
            return cls.model_validate(src_dict)

    SubscriptionConfig.model_rebuild()
else:
    SubscriptionConfig = GalileoCoreSubscriptionConfigClass


if issubclass(GalileoCoreExecutionStatusClass, BaseModel):

    class ExecutionStatus(GalileoCoreExecutionStatusClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ExecutionStatus":
            return cls.model_validate(src_dict)

    ExecutionStatus.model_rebuild()
else:
    ExecutionStatus = GalileoCoreExecutionStatusClass


if issubclass(GalileoCoreExecutionStatusMixInClass, BaseModel):

    class ExecutionStatusMixIn(GalileoCoreExecutionStatusMixInClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ExecutionStatusMixIn":
            return cls.model_validate(src_dict)

    ExecutionStatusMixIn.model_rebuild()
else:
    ExecutionStatusMixIn = GalileoCoreExecutionStatusMixInClass


if issubclass(GalileoCorePayloadClass, BaseModel):

    class Payload(GalileoCorePayloadClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Payload":
            return cls.model_validate(src_dict)

    Payload.model_rebuild()
else:
    Payload = GalileoCorePayloadClass


if issubclass(GalileoCoreRequestClass, BaseModel):

    class Request(GalileoCoreRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Request":
            return cls.model_validate(src_dict)

    Request.model_rebuild()
else:
    Request = GalileoCoreRequestClass


if issubclass(GalileoCoreRuleClass, BaseModel):

    class Rule(GalileoCoreRuleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Rule":
            return cls.model_validate(src_dict)

    Rule.model_rebuild()
else:
    Rule = GalileoCoreRuleClass


if issubclass(GalileoCoreRulesetsMixinClass, BaseModel):

    class RulesetsMixin(GalileoCoreRulesetsMixinClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RulesetsMixin":
            return cls.model_validate(src_dict)

    RulesetsMixin.model_rebuild()
else:
    RulesetsMixin = GalileoCoreRulesetsMixinClass


if issubclass(GalileoCoreBaseTraceMetadataClass, BaseModel):

    class BaseTraceMetadata(GalileoCoreBaseTraceMetadataClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseTraceMetadata":
            return cls.model_validate(src_dict)

    BaseTraceMetadata.model_rebuild()
else:
    BaseTraceMetadata = GalileoCoreBaseTraceMetadataClass


if issubclass(GalileoCoreExecutionStatusClass, BaseModel):

    class ExecutionStatus(GalileoCoreExecutionStatusClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ExecutionStatus":
            return cls.model_validate(src_dict)

    ExecutionStatus.model_rebuild()
else:
    ExecutionStatus = GalileoCoreExecutionStatusClass


if issubclass(GalileoCoreExecutionStatusMixInClass, BaseModel):

    class ExecutionStatusMixIn(GalileoCoreExecutionStatusMixInClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ExecutionStatusMixIn":
            return cls.model_validate(src_dict)

    ExecutionStatusMixIn.model_rebuild()
else:
    ExecutionStatusMixIn = GalileoCoreExecutionStatusMixInClass


if issubclass(GalileoCoreResponseClass, BaseModel):

    class Response(GalileoCoreResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Response":
            return cls.model_validate(src_dict)

    Response.model_rebuild()
else:
    Response = GalileoCoreResponseClass


if issubclass(GalileoCoreTraceMetadataClass, BaseModel):

    class TraceMetadata(GalileoCoreTraceMetadataClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "TraceMetadata":
            return cls.model_validate(src_dict)

    TraceMetadata.model_rebuild()
else:
    TraceMetadata = GalileoCoreTraceMetadataClass


if issubclass(GalileoCoreActionResultClass, BaseModel):

    class ActionResult(GalileoCoreActionResultClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ActionResult":
            return cls.model_validate(src_dict)

    ActionResult.model_rebuild()
else:
    ActionResult = GalileoCoreActionResultClass


if issubclass(GalileoCoreActionTypeClass, BaseModel):

    class ActionType(GalileoCoreActionTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ActionType":
            return cls.model_validate(src_dict)

    ActionType.model_rebuild()
else:
    ActionType = GalileoCoreActionTypeClass


if issubclass(GalileoCoreBaseActionClass, BaseModel):

    class BaseAction(GalileoCoreBaseActionClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseAction":
            return cls.model_validate(src_dict)

    BaseAction.model_rebuild()
else:
    BaseAction = GalileoCoreBaseActionClass


if issubclass(GalileoCoreOverrideActionClass, BaseModel):

    class OverrideAction(GalileoCoreOverrideActionClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "OverrideAction":
            return cls.model_validate(src_dict)

    OverrideAction.model_rebuild()
else:
    OverrideAction = GalileoCoreOverrideActionClass


if issubclass(GalileoCorePassthroughActionClass, BaseModel):

    class PassthroughAction(GalileoCorePassthroughActionClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PassthroughAction":
            return cls.model_validate(src_dict)

    PassthroughAction.model_rebuild()
else:
    PassthroughAction = GalileoCorePassthroughActionClass


if issubclass(GalileoCoreSubscriptionConfigClass, BaseModel):

    class SubscriptionConfig(GalileoCoreSubscriptionConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "SubscriptionConfig":
            return cls.model_validate(src_dict)

    SubscriptionConfig.model_rebuild()
else:
    SubscriptionConfig = GalileoCoreSubscriptionConfigClass


if issubclass(GalileoCorePayloadClass, BaseModel):

    class Payload(GalileoCorePayloadClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Payload":
            return cls.model_validate(src_dict)

    Payload.model_rebuild()
else:
    Payload = GalileoCorePayloadClass


if issubclass(GalileoCoreMetricComputationClass, BaseModel):

    class MetricComputation(GalileoCoreMetricComputationClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "MetricComputation":
            return cls.model_validate(src_dict)

    MetricComputation.model_rebuild()
else:
    MetricComputation = GalileoCoreMetricComputationClass


if issubclass(GalileoCoreMetricComputationStatusClass, BaseModel):

    class MetricComputationStatus(GalileoCoreMetricComputationStatusClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "MetricComputationStatus":
            return cls.model_validate(src_dict)

    MetricComputationStatus.model_rebuild()
else:
    MetricComputationStatus = GalileoCoreMetricComputationStatusClass


if issubclass(GalileoCoreRuleClass, BaseModel):

    class Rule(GalileoCoreRuleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Rule":
            return cls.model_validate(src_dict)

    Rule.model_rebuild()
else:
    Rule = GalileoCoreRuleClass


if issubclass(GalileoCoreRuleOperatorClass, BaseModel):

    class RuleOperator(GalileoCoreRuleOperatorClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RuleOperator":
            return cls.model_validate(src_dict)

    RuleOperator.model_rebuild()
else:
    RuleOperator = GalileoCoreRuleOperatorClass


if issubclass(GalileoCoreRulesetsMixinClass, BaseModel):

    class RulesetsMixin(GalileoCoreRulesetsMixinClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RulesetsMixin":
            return cls.model_validate(src_dict)

    RulesetsMixin.model_rebuild()
else:
    RulesetsMixin = GalileoCoreRulesetsMixinClass


if issubclass(GalileoCoreStageClass, BaseModel):

    class Stage(GalileoCoreStageClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Stage":
            return cls.model_validate(src_dict)

    Stage.model_rebuild()
else:
    Stage = GalileoCoreStageClass


if issubclass(GalileoCoreStageTypeClass, BaseModel):

    class StageType(GalileoCoreStageTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StageType":
            return cls.model_validate(src_dict)

    StageType.model_rebuild()
else:
    StageType = GalileoCoreStageTypeClass


if issubclass(GalileoCoreStageWithRulesetsClass, BaseModel):

    class StageWithRulesets(GalileoCoreStageWithRulesetsClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StageWithRulesets":
            return cls.model_validate(src_dict)

    StageWithRulesets.model_rebuild()
else:
    StageWithRulesets = GalileoCoreStageWithRulesetsClass


if issubclass(GalileoCoreCustomizedScorerClass, BaseModel):

    class CustomizedScorer(GalileoCoreCustomizedScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CustomizedScorer":
            return cls.model_validate(src_dict)

    CustomizedScorer.model_rebuild()
else:
    CustomizedScorer = GalileoCoreCustomizedScorerClass


if issubclass(GalileoCoreCustomizedScorerNameClass, BaseModel):

    class CustomizedScorerName(GalileoCoreCustomizedScorerNameClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CustomizedScorerName":
            return cls.model_validate(src_dict)

    CustomizedScorerName.model_rebuild()
else:
    CustomizedScorerName = GalileoCoreCustomizedScorerNameClass


if issubclass(GalileoCoreMessageRoleClass, BaseModel):

    class MessageRole(GalileoCoreMessageRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "MessageRole":
            return cls.model_validate(src_dict)

    MessageRole.model_rebuild()
else:
    MessageRole = GalileoCoreMessageRoleClass


if issubclass(GalileoCoreMessageClass, BaseModel):

    class Message(GalileoCoreMessageClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Message":
            return cls.model_validate(src_dict)

    Message.model_rebuild()
else:
    Message = GalileoCoreMessageClass


if issubclass(GalileoCoreMessageRoleClass, BaseModel):

    class MessageRole(GalileoCoreMessageRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "MessageRole":
            return cls.model_validate(src_dict)

    MessageRole.model_rebuild()
else:
    MessageRole = GalileoCoreMessageRoleClass


if issubclass(GalileoCoreDocumentClass, BaseModel):

    class Document(GalileoCoreDocumentClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Document":
            return cls.model_validate(src_dict)

    Document.model_rebuild()
else:
    Document = GalileoCoreDocumentClass


if issubclass(GalileoCoreLlmMetricsClass, BaseModel):

    class LlmMetrics(GalileoCoreLlmMetricsClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "LlmMetrics":
            return cls.model_validate(src_dict)

    LlmMetrics.model_rebuild()
else:
    LlmMetrics = GalileoCoreLlmMetricsClass


if issubclass(GalileoCoreLlmSpanClass, BaseModel):

    class LlmSpan(GalileoCoreLlmSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "LlmSpan":
            return cls.model_validate(src_dict)

    LlmSpan.model_rebuild()
else:
    LlmSpan = GalileoCoreLlmSpanClass


if issubclass(GalileoCoreMetricsClass, BaseModel):

    class Metrics(GalileoCoreMetricsClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Metrics":
            return cls.model_validate(src_dict)

    Metrics.model_rebuild()
else:
    Metrics = GalileoCoreMetricsClass


if issubclass(GalileoCorePydanticJsonEncoderClass, BaseModel):

    class PydanticJsonEncoder(GalileoCorePydanticJsonEncoderClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PydanticJsonEncoder":
            return cls.model_validate(src_dict)

    PydanticJsonEncoder.model_rebuild()
else:
    PydanticJsonEncoder = GalileoCorePydanticJsonEncoderClass


if issubclass(GalileoCoreRetrieverSpanClass, BaseModel):

    class RetrieverSpan(GalileoCoreRetrieverSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RetrieverSpan":
            return cls.model_validate(src_dict)

    RetrieverSpan.model_rebuild()
else:
    RetrieverSpan = GalileoCoreRetrieverSpanClass


if issubclass(GalileoCoreStepWithChildSpansClass, BaseModel):

    class StepWithChildSpans(GalileoCoreStepWithChildSpansClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StepWithChildSpans":
            return cls.model_validate(src_dict)

    StepWithChildSpans.model_rebuild()
else:
    StepWithChildSpans = GalileoCoreStepWithChildSpansClass


if issubclass(GalileoCoreToolSpanClass, BaseModel):

    class ToolSpan(GalileoCoreToolSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ToolSpan":
            return cls.model_validate(src_dict)

    ToolSpan.model_rebuild()
else:
    ToolSpan = GalileoCoreToolSpanClass


if issubclass(GalileoCoreTraceClass, BaseModel):

    class Trace(GalileoCoreTraceClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Trace":
            return cls.model_validate(src_dict)

    Trace.model_rebuild()
else:
    Trace = GalileoCoreTraceClass


if issubclass(GalileoCoreTracesLoggerClass, BaseModel):

    class TracesLogger(GalileoCoreTracesLoggerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "TracesLogger":
            return cls.model_validate(src_dict)

    TracesLogger.model_rebuild()
else:
    TracesLogger = GalileoCoreTracesLoggerClass


if issubclass(GalileoCoreWorkflowSpanClass, BaseModel):

    class WorkflowSpan(GalileoCoreWorkflowSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "WorkflowSpan":
            return cls.model_validate(src_dict)

    WorkflowSpan.model_rebuild()
else:
    WorkflowSpan = GalileoCoreWorkflowSpanClass


if issubclass(GalileoCoreCollectionFilterClass, BaseModel):

    class CollectionFilter(GalileoCoreCollectionFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CollectionFilter":
            return cls.model_validate(src_dict)

    CollectionFilter.model_rebuild()
else:
    CollectionFilter = GalileoCoreCollectionFilterClass


if issubclass(GalileoCoreCustomBooleanFilterClass, BaseModel):

    class CustomBooleanFilter(GalileoCoreCustomBooleanFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CustomBooleanFilter":
            return cls.model_validate(src_dict)

    CustomBooleanFilter.model_rebuild()
else:
    CustomBooleanFilter = GalileoCoreCustomBooleanFilterClass


if issubclass(GalileoCoreCustomNumberFilterClass, BaseModel):

    class CustomNumberFilter(GalileoCoreCustomNumberFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CustomNumberFilter":
            return cls.model_validate(src_dict)

    CustomNumberFilter.model_rebuild()
else:
    CustomNumberFilter = GalileoCoreCustomNumberFilterClass


if issubclass(GalileoCoreCustomUUIDFilterClass, BaseModel):

    class CustomUUIDFilter(GalileoCoreCustomUUIDFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CustomUUIDFilter":
            return cls.model_validate(src_dict)

    CustomUUIDFilter.model_rebuild()
else:
    CustomUUIDFilter = GalileoCoreCustomUUIDFilterClass


if issubclass(GalileoCoreDateFilterClass, BaseModel):

    class DateFilter(GalileoCoreDateFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "DateFilter":
            return cls.model_validate(src_dict)

    DateFilter.model_rebuild()
else:
    DateFilter = GalileoCoreDateFilterClass


if issubclass(GalileoCoreEnumFilterClass, BaseModel):

    class EnumFilter(GalileoCoreEnumFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "EnumFilter":
            return cls.model_validate(src_dict)

    EnumFilter.model_rebuild()
else:
    EnumFilter = GalileoCoreEnumFilterClass


if issubclass(GalileoCoreFilterBaseClass, BaseModel):

    class FilterBase(GalileoCoreFilterBaseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "FilterBase":
            return cls.model_validate(src_dict)

    FilterBase.model_rebuild()
else:
    FilterBase = GalileoCoreFilterBaseClass


if issubclass(GalileoCoreFilterTypeClass, BaseModel):

    class FilterType(GalileoCoreFilterTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "FilterType":
            return cls.model_validate(src_dict)

    FilterType.model_rebuild()
else:
    FilterType = GalileoCoreFilterTypeClass


if issubclass(GalileoCoreIDFilterClass, BaseModel):

    class IDFilter(GalileoCoreIDFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "IDFilter":
            return cls.model_validate(src_dict)

    IDFilter.model_rebuild()
else:
    IDFilter = GalileoCoreIDFilterClass


if issubclass(GalileoCoreMapFilterClass, BaseModel):

    class MapFilter(GalileoCoreMapFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "MapFilter":
            return cls.model_validate(src_dict)

    MapFilter.model_rebuild()
else:
    MapFilter = GalileoCoreMapFilterClass


if issubclass(GalileoCoreOperatorClass, BaseModel):

    class Operator(GalileoCoreOperatorClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Operator":
            return cls.model_validate(src_dict)

    Operator.model_rebuild()
else:
    Operator = GalileoCoreOperatorClass


if issubclass(GalileoCoreStringFilterClass, BaseModel):

    class StringFilter(GalileoCoreStringFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StringFilter":
            return cls.model_validate(src_dict)

    StringFilter.model_rebuild()
else:
    StringFilter = GalileoCoreStringFilterClass


if issubclass(GalileoCoreDocumentClass, BaseModel):

    class Document(GalileoCoreDocumentClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Document":
            return cls.model_validate(src_dict)

    Document.model_rebuild()
else:
    Document = GalileoCoreDocumentClass


if issubclass(GalileoCoreMessageClass, BaseModel):

    class Message(GalileoCoreMessageClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Message":
            return cls.model_validate(src_dict)

    Message.model_rebuild()
else:
    Message = GalileoCoreMessageClass


if issubclass(GalileoCoreMessageRoleClass, BaseModel):

    class MessageRole(GalileoCoreMessageRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "MessageRole":
            return cls.model_validate(src_dict)

    MessageRole.model_rebuild()
else:
    MessageRole = GalileoCoreMessageRoleClass


if issubclass(GalileoCoreMessagesClass, BaseModel):

    class Messages(GalileoCoreMessagesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Messages":
            return cls.model_validate(src_dict)

    Messages.model_rebuild()
else:
    Messages = GalileoCoreMessagesClass


if issubclass(GalileoCoreLlmSpanClass, BaseModel):

    class LlmSpan(GalileoCoreLlmSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "LlmSpan":
            return cls.model_validate(src_dict)

    LlmSpan.model_rebuild()
else:
    LlmSpan = GalileoCoreLlmSpanClass


if issubclass(GalileoCoreRetrieverSpanClass, BaseModel):

    class RetrieverSpan(GalileoCoreRetrieverSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RetrieverSpan":
            return cls.model_validate(src_dict)

    RetrieverSpan.model_rebuild()
else:
    RetrieverSpan = GalileoCoreRetrieverSpanClass


if issubclass(GalileoCoreStepWithChildSpansClass, BaseModel):

    class StepWithChildSpans(GalileoCoreStepWithChildSpansClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StepWithChildSpans":
            return cls.model_validate(src_dict)

    StepWithChildSpans.model_rebuild()
else:
    StepWithChildSpans = GalileoCoreStepWithChildSpansClass


if issubclass(GalileoCoreToolSpanClass, BaseModel):

    class ToolSpan(GalileoCoreToolSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ToolSpan":
            return cls.model_validate(src_dict)

    ToolSpan.model_rebuild()
else:
    ToolSpan = GalileoCoreToolSpanClass


if issubclass(GalileoCoreTraceClass, BaseModel):

    class Trace(GalileoCoreTraceClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Trace":
            return cls.model_validate(src_dict)

    Trace.model_rebuild()
else:
    Trace = GalileoCoreTraceClass


if issubclass(GalileoCoreTracesClass, BaseModel):

    class Traces(GalileoCoreTracesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Traces":
            return cls.model_validate(src_dict)

    Traces.model_rebuild()
else:
    Traces = GalileoCoreTracesClass


if issubclass(GalileoCoreWorkflowSpanClass, BaseModel):

    class WorkflowSpan(GalileoCoreWorkflowSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "WorkflowSpan":
            return cls.model_validate(src_dict)

    WorkflowSpan.model_rebuild()
else:
    WorkflowSpan = GalileoCoreWorkflowSpanClass


if issubclass(GalileoCoreBaseStepClass, BaseModel):

    class BaseStep(GalileoCoreBaseStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseStep":
            return cls.model_validate(src_dict)

    BaseStep.model_rebuild()
else:
    BaseStep = GalileoCoreBaseStepClass


if issubclass(GalileoCoreBaseStepWithChildrenClass, BaseModel):

    class BaseStepWithChildren(GalileoCoreBaseStepWithChildrenClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseStepWithChildren":
            return cls.model_validate(src_dict)

    BaseStepWithChildren.model_rebuild()
else:
    BaseStepWithChildren = GalileoCoreBaseStepWithChildrenClass


if issubclass(GalileoCoreLlmSpanClass, BaseModel):

    class LlmSpan(GalileoCoreLlmSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "LlmSpan":
            return cls.model_validate(src_dict)

    LlmSpan.model_rebuild()
else:
    LlmSpan = GalileoCoreLlmSpanClass


if issubclass(GalileoCoreLlmStepClass, BaseModel):

    class LlmStep(GalileoCoreLlmStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "LlmStep":
            return cls.model_validate(src_dict)

    LlmStep.model_rebuild()
else:
    LlmStep = GalileoCoreLlmStepClass


if issubclass(GalileoCoreNodeTypeClass, BaseModel):

    class NodeType(GalileoCoreNodeTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "NodeType":
            return cls.model_validate(src_dict)

    NodeType.model_rebuild()
else:
    NodeType = GalileoCoreNodeTypeClass


if issubclass(GalileoCoreRetrieverSpanClass, BaseModel):

    class RetrieverSpan(GalileoCoreRetrieverSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RetrieverSpan":
            return cls.model_validate(src_dict)

    RetrieverSpan.model_rebuild()
else:
    RetrieverSpan = GalileoCoreRetrieverSpanClass


if issubclass(GalileoCoreRetrieverStepClass, BaseModel):

    class RetrieverStep(GalileoCoreRetrieverStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RetrieverStep":
            return cls.model_validate(src_dict)

    RetrieverStep.model_rebuild()
else:
    RetrieverStep = GalileoCoreRetrieverStepClass


if issubclass(GalileoCoreSpanWithParentStepClass, BaseModel):

    class SpanWithParentStep(GalileoCoreSpanWithParentStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "SpanWithParentStep":
            return cls.model_validate(src_dict)

    SpanWithParentStep.model_rebuild()
else:
    SpanWithParentStep = GalileoCoreSpanWithParentStepClass


if issubclass(GalileoCoreStepWithChildSpansClass, BaseModel):

    class StepWithChildSpans(GalileoCoreStepWithChildSpansClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StepWithChildSpans":
            return cls.model_validate(src_dict)

    StepWithChildSpans.model_rebuild()
else:
    StepWithChildSpans = GalileoCoreStepWithChildSpansClass


if issubclass(GalileoCoreToolSpanClass, BaseModel):

    class ToolSpan(GalileoCoreToolSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ToolSpan":
            return cls.model_validate(src_dict)

    ToolSpan.model_rebuild()
else:
    ToolSpan = GalileoCoreToolSpanClass


if issubclass(GalileoCoreToolStepClass, BaseModel):

    class ToolStep(GalileoCoreToolStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ToolStep":
            return cls.model_validate(src_dict)

    ToolStep.model_rebuild()
else:
    ToolStep = GalileoCoreToolStepClass


if issubclass(GalileoCoreTraceClass, BaseModel):

    class Trace(GalileoCoreTraceClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Trace":
            return cls.model_validate(src_dict)

    Trace.model_rebuild()
else:
    Trace = GalileoCoreTraceClass


if issubclass(GalileoCoreWorkflowSpanClass, BaseModel):

    class WorkflowSpan(GalileoCoreWorkflowSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "WorkflowSpan":
            return cls.model_validate(src_dict)

    WorkflowSpan.model_rebuild()
else:
    WorkflowSpan = GalileoCoreWorkflowSpanClass


if issubclass(GalileoCoreAgentStepClass, BaseModel):

    class AgentStep(GalileoCoreAgentStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AgentStep":
            return cls.model_validate(src_dict)

    AgentStep.model_rebuild()
else:
    AgentStep = GalileoCoreAgentStepClass


if issubclass(GalileoCoreBaseStepClass, BaseModel):

    class BaseStep(GalileoCoreBaseStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseStep":
            return cls.model_validate(src_dict)

    BaseStep.model_rebuild()
else:
    BaseStep = GalileoCoreBaseStepClass


if issubclass(GalileoCoreBaseStepWithChildrenClass, BaseModel):

    class BaseStepWithChildren(GalileoCoreBaseStepWithChildrenClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseStepWithChildren":
            return cls.model_validate(src_dict)

    BaseStepWithChildren.model_rebuild()
else:
    BaseStepWithChildren = GalileoCoreBaseStepWithChildrenClass


if issubclass(GalileoCoreChainStepClass, BaseModel):

    class ChainStep(GalileoCoreChainStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ChainStep":
            return cls.model_validate(src_dict)

    ChainStep.model_rebuild()
else:
    ChainStep = GalileoCoreChainStepClass


if issubclass(GalileoCoreDocumentClass, BaseModel):

    class Document(GalileoCoreDocumentClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Document":
            return cls.model_validate(src_dict)

    Document.model_rebuild()
else:
    Document = GalileoCoreDocumentClass


if issubclass(GalileoCoreLlmStepClass, BaseModel):

    class LlmStep(GalileoCoreLlmStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "LlmStep":
            return cls.model_validate(src_dict)

    LlmStep.model_rebuild()
else:
    LlmStep = GalileoCoreLlmStepClass


if issubclass(GalileoCoreMessageClass, BaseModel):

    class Message(GalileoCoreMessageClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Message":
            return cls.model_validate(src_dict)

    Message.model_rebuild()
else:
    Message = GalileoCoreMessageClass


if issubclass(GalileoCoreNodeTypeClass, BaseModel):

    class NodeType(GalileoCoreNodeTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "NodeType":
            return cls.model_validate(src_dict)

    NodeType.model_rebuild()
else:
    NodeType = GalileoCoreNodeTypeClass


if issubclass(GalileoCorePayloadClass, BaseModel):

    class Payload(GalileoCorePayloadClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Payload":
            return cls.model_validate(src_dict)

    Payload.model_rebuild()
else:
    Payload = GalileoCorePayloadClass


if issubclass(GalileoCorePydanticJsonEncoderClass, BaseModel):

    class PydanticJsonEncoder(GalileoCorePydanticJsonEncoderClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PydanticJsonEncoder":
            return cls.model_validate(src_dict)

    PydanticJsonEncoder.model_rebuild()
else:
    PydanticJsonEncoder = GalileoCorePydanticJsonEncoderClass


if issubclass(GalileoCoreResponseClass, BaseModel):

    class Response(GalileoCoreResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Response":
            return cls.model_validate(src_dict)

    Response.model_rebuild()
else:
    Response = GalileoCoreResponseClass


if issubclass(GalileoCoreRetrieverStepClass, BaseModel):

    class RetrieverStep(GalileoCoreRetrieverStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RetrieverStep":
            return cls.model_validate(src_dict)

    RetrieverStep.model_rebuild()
else:
    RetrieverStep = GalileoCoreRetrieverStepClass


if issubclass(GalileoCoreStepWithChildrenClass, BaseModel):

    class StepWithChildren(GalileoCoreStepWithChildrenClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StepWithChildren":
            return cls.model_validate(src_dict)

    StepWithChildren.model_rebuild()
else:
    StepWithChildren = GalileoCoreStepWithChildrenClass


if issubclass(GalileoCoreToolStepClass, BaseModel):

    class ToolStep(GalileoCoreToolStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ToolStep":
            return cls.model_validate(src_dict)

    ToolStep.model_rebuild()
else:
    ToolStep = GalileoCoreToolStepClass


if issubclass(GalileoCoreWorkflowStepClass, BaseModel):

    class WorkflowStep(GalileoCoreWorkflowStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "WorkflowStep":
            return cls.model_validate(src_dict)

    WorkflowStep.model_rebuild()
else:
    WorkflowStep = GalileoCoreWorkflowStepClass


if issubclass(GalileoCoreAgentStepClass, BaseModel):

    class AgentStep(GalileoCoreAgentStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AgentStep":
            return cls.model_validate(src_dict)

    AgentStep.model_rebuild()
else:
    AgentStep = GalileoCoreAgentStepClass


if issubclass(GalileoCoreLlmStepClass, BaseModel):

    class LlmStep(GalileoCoreLlmStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "LlmStep":
            return cls.model_validate(src_dict)

    LlmStep.model_rebuild()
else:
    LlmStep = GalileoCoreLlmStepClass


if issubclass(GalileoCorePayloadClass, BaseModel):

    class Payload(GalileoCorePayloadClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Payload":
            return cls.model_validate(src_dict)

    Payload.model_rebuild()
else:
    Payload = GalileoCorePayloadClass


if issubclass(GalileoCoreResponseClass, BaseModel):

    class Response(GalileoCoreResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Response":
            return cls.model_validate(src_dict)

    Response.model_rebuild()
else:
    Response = GalileoCoreResponseClass


if issubclass(GalileoCoreRetrieverStepClass, BaseModel):

    class RetrieverStep(GalileoCoreRetrieverStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RetrieverStep":
            return cls.model_validate(src_dict)

    RetrieverStep.model_rebuild()
else:
    RetrieverStep = GalileoCoreRetrieverStepClass


if issubclass(GalileoCoreStepWithChildrenClass, BaseModel):

    class StepWithChildren(GalileoCoreStepWithChildrenClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StepWithChildren":
            return cls.model_validate(src_dict)

    StepWithChildren.model_rebuild()
else:
    StepWithChildren = GalileoCoreStepWithChildrenClass


if issubclass(GalileoCoreToolStepClass, BaseModel):

    class ToolStep(GalileoCoreToolStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ToolStep":
            return cls.model_validate(src_dict)

    ToolStep.model_rebuild()
else:
    ToolStep = GalileoCoreToolStepClass


if issubclass(GalileoCoreWorkflowStepClass, BaseModel):

    class WorkflowStep(GalileoCoreWorkflowStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "WorkflowStep":
            return cls.model_validate(src_dict)

    WorkflowStep.model_rebuild()
else:
    WorkflowStep = GalileoCoreWorkflowStepClass


if issubclass(GalileoCoreWorkflowsClass, BaseModel):

    class Workflows(GalileoCoreWorkflowsClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Workflows":
            return cls.model_validate(src_dict)

    Workflows.model_rebuild()
else:
    Workflows = GalileoCoreWorkflowsClass


if issubclass(GalileoCoreNodeTypeClass, BaseModel):

    class NodeType(GalileoCoreNodeTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "NodeType":
            return cls.model_validate(src_dict)

    NodeType.model_rebuild()
else:
    NodeType = GalileoCoreNodeTypeClass


if issubclass(GalileoCoreAgenticSessionSuccessScorerClass, BaseModel):

    class AgenticSessionSuccessScorer(GalileoCoreAgenticSessionSuccessScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AgenticSessionSuccessScorer":
            return cls.model_validate(src_dict)

    AgenticSessionSuccessScorer.model_rebuild()
else:
    AgenticSessionSuccessScorer = GalileoCoreAgenticSessionSuccessScorerClass


if issubclass(GalileoCoreAgenticWorkflowSuccessScorerClass, BaseModel):

    class AgenticWorkflowSuccessScorer(GalileoCoreAgenticWorkflowSuccessScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AgenticWorkflowSuccessScorer":
            return cls.model_validate(src_dict)

    AgenticWorkflowSuccessScorer.model_rebuild()
else:
    AgenticWorkflowSuccessScorer = GalileoCoreAgenticWorkflowSuccessScorerClass


if issubclass(GalileoCoreBleuScorerClass, BaseModel):

    class BleuScorer(GalileoCoreBleuScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BleuScorer":
            return cls.model_validate(src_dict)

    BleuScorer.model_rebuild()
else:
    BleuScorer = GalileoCoreBleuScorerClass


if issubclass(GalileoCoreChunkAttributionUtilizationScorerClass, BaseModel):

    class ChunkAttributionUtilizationScorer(GalileoCoreChunkAttributionUtilizationScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ChunkAttributionUtilizationScorer":
            return cls.model_validate(src_dict)

    ChunkAttributionUtilizationScorer.model_rebuild()
else:
    ChunkAttributionUtilizationScorer = GalileoCoreChunkAttributionUtilizationScorerClass


if issubclass(GalileoCoreCompletenessScorerClass, BaseModel):

    class CompletenessScorer(GalileoCoreCompletenessScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CompletenessScorer":
            return cls.model_validate(src_dict)

    CompletenessScorer.model_rebuild()
else:
    CompletenessScorer = GalileoCoreCompletenessScorerClass


if issubclass(GalileoCoreContextAdherenceScorerClass, BaseModel):

    class ContextAdherenceScorer(GalileoCoreContextAdherenceScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ContextAdherenceScorer":
            return cls.model_validate(src_dict)

    ContextAdherenceScorer.model_rebuild()
else:
    ContextAdherenceScorer = GalileoCoreContextAdherenceScorerClass


if issubclass(GalileoCoreContextRelevanceScorerClass, BaseModel):

    class ContextRelevanceScorer(GalileoCoreContextRelevanceScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ContextRelevanceScorer":
            return cls.model_validate(src_dict)

    ContextRelevanceScorer.model_rebuild()
else:
    ContextRelevanceScorer = GalileoCoreContextRelevanceScorerClass


if issubclass(GalileoCoreCorrectnessScorerClass, BaseModel):

    class CorrectnessScorer(GalileoCoreCorrectnessScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CorrectnessScorer":
            return cls.model_validate(src_dict)

    CorrectnessScorer.model_rebuild()
else:
    CorrectnessScorer = GalileoCoreCorrectnessScorerClass


if issubclass(GalileoCoreGalileoScorerConfigClass, BaseModel):

    class GalileoScorerConfig(GalileoCoreGalileoScorerConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoScorerConfig":
            return cls.model_validate(src_dict)

    GalileoScorerConfig.model_rebuild()
else:
    GalileoScorerConfig = GalileoCoreGalileoScorerConfigClass


if issubclass(GalileoCoreGroundTruthAdherenceScorerClass, BaseModel):

    class GroundTruthAdherenceScorer(GalileoCoreGroundTruthAdherenceScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GroundTruthAdherenceScorer":
            return cls.model_validate(src_dict)

    GroundTruthAdherenceScorer.model_rebuild()
else:
    GroundTruthAdherenceScorer = GalileoCoreGroundTruthAdherenceScorerClass


if issubclass(GalileoCoreInputPIIScorerClass, BaseModel):

    class InputPIIScorer(GalileoCoreInputPIIScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "InputPIIScorer":
            return cls.model_validate(src_dict)

    InputPIIScorer.model_rebuild()
else:
    InputPIIScorer = GalileoCoreInputPIIScorerClass


if issubclass(GalileoCoreInputSexistScorerClass, BaseModel):

    class InputSexistScorer(GalileoCoreInputSexistScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "InputSexistScorer":
            return cls.model_validate(src_dict)

    InputSexistScorer.model_rebuild()
else:
    InputSexistScorer = GalileoCoreInputSexistScorerClass


if issubclass(GalileoCoreInputToneScorerClass, BaseModel):

    class InputToneScorer(GalileoCoreInputToneScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "InputToneScorer":
            return cls.model_validate(src_dict)

    InputToneScorer.model_rebuild()
else:
    InputToneScorer = GalileoCoreInputToneScorerClass


if issubclass(GalileoCoreInputToxicityScorerClass, BaseModel):

    class InputToxicityScorer(GalileoCoreInputToxicityScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "InputToxicityScorer":
            return cls.model_validate(src_dict)

    InputToxicityScorer.model_rebuild()
else:
    InputToxicityScorer = GalileoCoreInputToxicityScorerClass


if issubclass(GalileoCoreInstructionAdherenceScorerClass, BaseModel):

    class InstructionAdherenceScorer(GalileoCoreInstructionAdherenceScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "InstructionAdherenceScorer":
            return cls.model_validate(src_dict)

    InstructionAdherenceScorer.model_rebuild()
else:
    InstructionAdherenceScorer = GalileoCoreInstructionAdherenceScorerClass


if issubclass(GalileoCoreLunaOrPlusScorerTypeConfigClass, BaseModel):

    class LunaOrPlusScorerTypeConfig(GalileoCoreLunaOrPlusScorerTypeConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "LunaOrPlusScorerTypeConfig":
            return cls.model_validate(src_dict)

    LunaOrPlusScorerTypeConfig.model_rebuild()
else:
    LunaOrPlusScorerTypeConfig = GalileoCoreLunaOrPlusScorerTypeConfigClass


if issubclass(GalileoCoreOutputPIIScorerClass, BaseModel):

    class OutputPIIScorer(GalileoCoreOutputPIIScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "OutputPIIScorer":
            return cls.model_validate(src_dict)

    OutputPIIScorer.model_rebuild()
else:
    OutputPIIScorer = GalileoCoreOutputPIIScorerClass


if issubclass(GalileoCoreOutputSexistScorerClass, BaseModel):

    class OutputSexistScorer(GalileoCoreOutputSexistScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "OutputSexistScorer":
            return cls.model_validate(src_dict)

    OutputSexistScorer.model_rebuild()
else:
    OutputSexistScorer = GalileoCoreOutputSexistScorerClass


if issubclass(GalileoCoreOutputToneScorerClass, BaseModel):

    class OutputToneScorer(GalileoCoreOutputToneScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "OutputToneScorer":
            return cls.model_validate(src_dict)

    OutputToneScorer.model_rebuild()
else:
    OutputToneScorer = GalileoCoreOutputToneScorerClass


if issubclass(GalileoCoreOutputToxicityScorerClass, BaseModel):

    class OutputToxicityScorer(GalileoCoreOutputToxicityScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "OutputToxicityScorer":
            return cls.model_validate(src_dict)

    OutputToxicityScorer.model_rebuild()
else:
    OutputToxicityScorer = GalileoCoreOutputToxicityScorerClass


if issubclass(GalileoCorePlusScorerConfigClass, BaseModel):

    class PlusScorerConfig(GalileoCorePlusScorerConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PlusScorerConfig":
            return cls.model_validate(src_dict)

    PlusScorerConfig.model_rebuild()
else:
    PlusScorerConfig = GalileoCorePlusScorerConfigClass


if issubclass(GalileoCorePlusScorerTypeConfigClass, BaseModel):

    class PlusScorerTypeConfig(GalileoCorePlusScorerTypeConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PlusScorerTypeConfig":
            return cls.model_validate(src_dict)

    PlusScorerTypeConfig.model_rebuild()
else:
    PlusScorerTypeConfig = GalileoCorePlusScorerTypeConfigClass


if issubclass(GalileoCorePlusScorerWithNumJudgesConfigClass, BaseModel):

    class PlusScorerWithNumJudgesConfig(GalileoCorePlusScorerWithNumJudgesConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PlusScorerWithNumJudgesConfig":
            return cls.model_validate(src_dict)

    PlusScorerWithNumJudgesConfig.model_rebuild()
else:
    PlusScorerWithNumJudgesConfig = GalileoCorePlusScorerWithNumJudgesConfigClass


if issubclass(GalileoCorePromptInjectionScorerClass, BaseModel):

    class PromptInjectionScorer(GalileoCorePromptInjectionScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PromptInjectionScorer":
            return cls.model_validate(src_dict)

    PromptInjectionScorer.model_rebuild()
else:
    PromptInjectionScorer = GalileoCorePromptInjectionScorerClass


if issubclass(GalileoCorePromptPerplexityScorerClass, BaseModel):

    class PromptPerplexityScorer(GalileoCorePromptPerplexityScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PromptPerplexityScorer":
            return cls.model_validate(src_dict)

    PromptPerplexityScorer.model_rebuild()
else:
    PromptPerplexityScorer = GalileoCorePromptPerplexityScorerClass


if issubclass(GalileoCoreRougeScorerClass, BaseModel):

    class RougeScorer(GalileoCoreRougeScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RougeScorer":
            return cls.model_validate(src_dict)

    RougeScorer.model_rebuild()
else:
    RougeScorer = GalileoCoreRougeScorerClass


if issubclass(GalileoCoreScorerNameClass, BaseModel):

    class ScorerName(GalileoCoreScorerNameClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ScorerName":
            return cls.model_validate(src_dict)

    ScorerName.model_rebuild()
else:
    ScorerName = GalileoCoreScorerNameClass


if issubclass(GalileoCoreToolErrorRateScorerClass, BaseModel):

    class ToolErrorRateScorer(GalileoCoreToolErrorRateScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ToolErrorRateScorer":
            return cls.model_validate(src_dict)

    ToolErrorRateScorer.model_rebuild()
else:
    ToolErrorRateScorer = GalileoCoreToolErrorRateScorerClass


if issubclass(GalileoCoreToolSelectionQualityScorerClass, BaseModel):

    class ToolSelectionQualityScorer(GalileoCoreToolSelectionQualityScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ToolSelectionQualityScorer":
            return cls.model_validate(src_dict)

    ToolSelectionQualityScorer.model_rebuild()
else:
    ToolSelectionQualityScorer = GalileoCoreToolSelectionQualityScorerClass


if issubclass(GalileoCoreUncertaintyScorerClass, BaseModel):

    class UncertaintyScorer(GalileoCoreUncertaintyScorerClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UncertaintyScorer":
            return cls.model_validate(src_dict)

    UncertaintyScorer.model_rebuild()
else:
    UncertaintyScorer = GalileoCoreUncertaintyScorerClass


if issubclass(GalileoCoreScorerNameValidatorMixinClass, BaseModel):

    class ScorerNameValidatorMixin(GalileoCoreScorerNameValidatorMixinClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ScorerNameValidatorMixin":
            return cls.model_validate(src_dict)

    ScorerNameValidatorMixin.model_rebuild()
else:
    ScorerNameValidatorMixin = GalileoCoreScorerNameValidatorMixinClass


if issubclass(GalileoCoreChainAggregationStrategyClass, BaseModel):

    class ChainAggregationStrategy(GalileoCoreChainAggregationStrategyClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ChainAggregationStrategy":
            return cls.model_validate(src_dict)

    ChainAggregationStrategy.model_rebuild()
else:
    ChainAggregationStrategy = GalileoCoreChainAggregationStrategyClass


if issubclass(GalileoCoreScorerNameClass, BaseModel):

    class ScorerName(GalileoCoreScorerNameClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ScorerName":
            return cls.model_validate(src_dict)

    ScorerName.model_rebuild()
else:
    ScorerName = GalileoCoreScorerNameClass


if issubclass(GalileoCoreBaseScorerConfigClass, BaseModel):

    class BaseScorerConfig(GalileoCoreBaseScorerConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseScorerConfig":
            return cls.model_validate(src_dict)

    BaseScorerConfig.model_rebuild()
else:
    BaseScorerConfig = GalileoCoreBaseScorerConfigClass


if issubclass(GalileoCoreGalileoScorerConfigClass, BaseModel):

    class GalileoScorerConfig(GalileoCoreGalileoScorerConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoScorerConfig":
            return cls.model_validate(src_dict)

    GalileoScorerConfig.model_rebuild()
else:
    GalileoScorerConfig = GalileoCoreGalileoScorerConfigClass


if issubclass(GalileoCoreGeneratedScorerConfigClass, BaseModel):

    class GeneratedScorerConfig(GalileoCoreGeneratedScorerConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GeneratedScorerConfig":
            return cls.model_validate(src_dict)

    GeneratedScorerConfig.model_rebuild()
else:
    GeneratedScorerConfig = GalileoCoreGeneratedScorerConfigClass


if issubclass(GalileoCoreLunaOrPlusScorerTypeConfigClass, BaseModel):

    class LunaOrPlusScorerTypeConfig(GalileoCoreLunaOrPlusScorerTypeConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "LunaOrPlusScorerTypeConfig":
            return cls.model_validate(src_dict)

    LunaOrPlusScorerTypeConfig.model_rebuild()
else:
    LunaOrPlusScorerTypeConfig = GalileoCoreLunaOrPlusScorerTypeConfigClass


if issubclass(GalileoCorePlusScorerConfigClass, BaseModel):

    class PlusScorerConfig(GalileoCorePlusScorerConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PlusScorerConfig":
            return cls.model_validate(src_dict)

    PlusScorerConfig.model_rebuild()
else:
    PlusScorerConfig = GalileoCorePlusScorerConfigClass


if issubclass(GalileoCorePlusScorerTypeConfigClass, BaseModel):

    class PlusScorerTypeConfig(GalileoCorePlusScorerTypeConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PlusScorerTypeConfig":
            return cls.model_validate(src_dict)

    PlusScorerTypeConfig.model_rebuild()
else:
    PlusScorerTypeConfig = GalileoCorePlusScorerTypeConfigClass


if issubclass(GalileoCorePlusScorerWithNumJudgesConfigClass, BaseModel):

    class PlusScorerWithNumJudgesConfig(GalileoCorePlusScorerWithNumJudgesConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PlusScorerWithNumJudgesConfig":
            return cls.model_validate(src_dict)

    PlusScorerWithNumJudgesConfig.model_rebuild()
else:
    PlusScorerWithNumJudgesConfig = GalileoCorePlusScorerWithNumJudgesConfigClass


if issubclass(GalileoCoreRegisteredScorerConfigClass, BaseModel):

    class RegisteredScorerConfig(GalileoCoreRegisteredScorerConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RegisteredScorerConfig":
            return cls.model_validate(src_dict)

    RegisteredScorerConfig.model_rebuild()
else:
    RegisteredScorerConfig = GalileoCoreRegisteredScorerConfigClass


if issubclass(GalileoCoreScorerNameClass, BaseModel):

    class ScorerName(GalileoCoreScorerNameClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ScorerName":
            return cls.model_validate(src_dict)

    ScorerName.model_rebuild()
else:
    ScorerName = GalileoCoreScorerNameClass


if issubclass(GalileoCoreScorerNameValidatorMixinClass, BaseModel):

    class ScorerNameValidatorMixin(GalileoCoreScorerNameValidatorMixinClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ScorerNameValidatorMixin":
            return cls.model_validate(src_dict)

    ScorerNameValidatorMixin.model_rebuild()
else:
    ScorerNameValidatorMixin = GalileoCoreScorerNameValidatorMixinClass


if issubclass(GalileoCoreScorerTypeClass, BaseModel):

    class ScorerType(GalileoCoreScorerTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ScorerType":
            return cls.model_validate(src_dict)

    ScorerType.model_rebuild()
else:
    ScorerType = GalileoCoreScorerTypeClass


if issubclass(GalileoCoreScorerTypeClass, BaseModel):

    class ScorerType(GalileoCoreScorerTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ScorerType":
            return cls.model_validate(src_dict)

    ScorerType.model_rebuild()
else:
    ScorerType = GalileoCoreScorerTypeClass


if issubclass(GalileoCoreGeneratedScorerConfigClass, BaseModel):

    class GeneratedScorerConfig(GalileoCoreGeneratedScorerConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GeneratedScorerConfig":
            return cls.model_validate(src_dict)

    GeneratedScorerConfig.model_rebuild()
else:
    GeneratedScorerConfig = GalileoCoreGeneratedScorerConfigClass


if issubclass(GalileoCoreRegisteredScorerConfigClass, BaseModel):

    class RegisteredScorerConfig(GalileoCoreRegisteredScorerConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RegisteredScorerConfig":
            return cls.model_validate(src_dict)

    RegisteredScorerConfig.model_rebuild()
else:
    RegisteredScorerConfig = GalileoCoreRegisteredScorerConfigClass


if issubclass(GalileoCoreScorerConfigurationClass, BaseModel):

    class ScorerConfiguration(GalileoCoreScorerConfigurationClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ScorerConfiguration":
            return cls.model_validate(src_dict)

    ScorerConfiguration.model_rebuild()
else:
    ScorerConfiguration = GalileoCoreScorerConfigurationClass


if issubclass(GalileoCoreMapFilterClass, BaseModel):

    class MapFilter(GalileoCoreMapFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "MapFilter":
            return cls.model_validate(src_dict)

    MapFilter.model_rebuild()
else:
    MapFilter = GalileoCoreMapFilterClass


if issubclass(GalileoCoreMetadataFilterClass, BaseModel):

    class MetadataFilter(GalileoCoreMetadataFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "MetadataFilter":
            return cls.model_validate(src_dict)

    MetadataFilter.model_rebuild()
else:
    MetadataFilter = GalileoCoreMetadataFilterClass


if issubclass(GalileoCoreNodeNameFilterClass, BaseModel):

    class NodeNameFilter(GalileoCoreNodeNameFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "NodeNameFilter":
            return cls.model_validate(src_dict)

    NodeNameFilter.model_rebuild()
else:
    NodeNameFilter = GalileoCoreNodeNameFilterClass


if issubclass(GalileoCoreScorerJobFilterNamesClass, BaseModel):

    class ScorerJobFilterNames(GalileoCoreScorerJobFilterNamesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ScorerJobFilterNames":
            return cls.model_validate(src_dict)

    ScorerJobFilterNames.model_rebuild()
else:
    ScorerJobFilterNames = GalileoCoreScorerJobFilterNamesClass


if issubclass(GalileoCoreStringFilterClass, BaseModel):

    class StringFilter(GalileoCoreStringFilterClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StringFilter":
            return cls.model_validate(src_dict)

    StringFilter.model_rebuild()
else:
    StringFilter = GalileoCoreStringFilterClass


if issubclass(GalileoCoreBaseStepClass, BaseModel):

    class BaseStep(GalileoCoreBaseStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseStep":
            return cls.model_validate(src_dict)

    BaseStep.model_rebuild()
else:
    BaseStep = GalileoCoreBaseStepClass


if issubclass(GalileoCoreBaseTraceClass, BaseModel):

    class BaseTrace(GalileoCoreBaseTraceClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseTrace":
            return cls.model_validate(src_dict)

    BaseTrace.model_rebuild()
else:
    BaseTrace = GalileoCoreBaseTraceClass


if issubclass(GalileoCoreStepTypeClass, BaseModel):

    class StepType(GalileoCoreStepTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StepType":
            return cls.model_validate(src_dict)

    StepType.model_rebuild()
else:
    StepType = GalileoCoreStepTypeClass


if issubclass(GalileoCoreStepWithChildSpansClass, BaseModel):

    class StepWithChildSpans(GalileoCoreStepWithChildSpansClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StepWithChildSpans":
            return cls.model_validate(src_dict)

    StepWithChildSpans.model_rebuild()
else:
    StepWithChildSpans = GalileoCoreStepWithChildSpansClass


if issubclass(GalileoCoreTraceClass, BaseModel):

    class Trace(GalileoCoreTraceClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Trace":
            return cls.model_validate(src_dict)

    Trace.model_rebuild()
else:
    Trace = GalileoCoreTraceClass


if issubclass(GalileoCoreMessageClass, BaseModel):

    class Message(GalileoCoreMessageClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Message":
            return cls.model_validate(src_dict)

    Message.model_rebuild()
else:
    Message = GalileoCoreMessageClass


if issubclass(GalileoCoreMessageRoleClass, BaseModel):

    class MessageRole(GalileoCoreMessageRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "MessageRole":
            return cls.model_validate(src_dict)

    MessageRole.model_rebuild()
else:
    MessageRole = GalileoCoreMessageRoleClass


if issubclass(GalileoCoreMessagesClass, BaseModel):

    class Messages(GalileoCoreMessagesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Messages":
            return cls.model_validate(src_dict)

    Messages.model_rebuild()
else:
    Messages = GalileoCoreMessagesClass


if issubclass(GalileoCoreToolCallClass, BaseModel):

    class ToolCall(GalileoCoreToolCallClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ToolCall":
            return cls.model_validate(src_dict)

    ToolCall.model_rebuild()
else:
    ToolCall = GalileoCoreToolCallClass


if issubclass(GalileoCoreToolCallFunctionClass, BaseModel):

    class ToolCallFunction(GalileoCoreToolCallFunctionClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ToolCallFunction":
            return cls.model_validate(src_dict)

    ToolCallFunction.model_rebuild()
else:
    ToolCallFunction = GalileoCoreToolCallFunctionClass


if issubclass(GalileoCoreBaseStepClass, BaseModel):

    class BaseStep(GalileoCoreBaseStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseStep":
            return cls.model_validate(src_dict)

    BaseStep.model_rebuild()
else:
    BaseStep = GalileoCoreBaseStepClass


if issubclass(GalileoCoreDocumentClass, BaseModel):

    class Document(GalileoCoreDocumentClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Document":
            return cls.model_validate(src_dict)

    Document.model_rebuild()
else:
    Document = GalileoCoreDocumentClass


if issubclass(GalileoCoreMessageClass, BaseModel):

    class Message(GalileoCoreMessageClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Message":
            return cls.model_validate(src_dict)

    Message.model_rebuild()
else:
    Message = GalileoCoreMessageClass


if issubclass(GalileoCoreMetricsClass, BaseModel):

    class Metrics(GalileoCoreMetricsClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Metrics":
            return cls.model_validate(src_dict)

    Metrics.model_rebuild()
else:
    Metrics = GalileoCoreMetricsClass


if issubclass(GalileoCorePydanticJsonEncoderClass, BaseModel):

    class PydanticJsonEncoder(GalileoCorePydanticJsonEncoderClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PydanticJsonEncoder":
            return cls.model_validate(src_dict)

    PydanticJsonEncoder.model_rebuild()
else:
    PydanticJsonEncoder = GalileoCorePydanticJsonEncoderClass


if issubclass(GalileoCoreStepTypeClass, BaseModel):

    class StepType(GalileoCoreStepTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StepType":
            return cls.model_validate(src_dict)

    StepType.model_rebuild()
else:
    StepType = GalileoCoreStepTypeClass


if issubclass(GalileoCoreBaseStepClass, BaseModel):

    class BaseStep(GalileoCoreBaseStepClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseStep":
            return cls.model_validate(src_dict)

    BaseStep.model_rebuild()
else:
    BaseStep = GalileoCoreBaseStepClass


if issubclass(GalileoCoreBaseWorkflowSpanClass, BaseModel):

    class BaseWorkflowSpan(GalileoCoreBaseWorkflowSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "BaseWorkflowSpan":
            return cls.model_validate(src_dict)

    BaseWorkflowSpan.model_rebuild()
else:
    BaseWorkflowSpan = GalileoCoreBaseWorkflowSpanClass


if issubclass(GalileoCoreDocumentClass, BaseModel):

    class Document(GalileoCoreDocumentClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Document":
            return cls.model_validate(src_dict)

    Document.model_rebuild()
else:
    Document = GalileoCoreDocumentClass


if issubclass(GalileoCoreLlmMetricsClass, BaseModel):

    class LlmMetrics(GalileoCoreLlmMetricsClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "LlmMetrics":
            return cls.model_validate(src_dict)

    LlmMetrics.model_rebuild()
else:
    LlmMetrics = GalileoCoreLlmMetricsClass


if issubclass(GalileoCoreLlmSpanClass, BaseModel):

    class LlmSpan(GalileoCoreLlmSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "LlmSpan":
            return cls.model_validate(src_dict)

    LlmSpan.model_rebuild()
else:
    LlmSpan = GalileoCoreLlmSpanClass


if issubclass(GalileoCoreMessageClass, BaseModel):

    class Message(GalileoCoreMessageClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Message":
            return cls.model_validate(src_dict)

    Message.model_rebuild()
else:
    Message = GalileoCoreMessageClass


if issubclass(GalileoCoreMessageRoleClass, BaseModel):

    class MessageRole(GalileoCoreMessageRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "MessageRole":
            return cls.model_validate(src_dict)

    MessageRole.model_rebuild()
else:
    MessageRole = GalileoCoreMessageRoleClass


if issubclass(GalileoCoreMetricsClass, BaseModel):

    class Metrics(GalileoCoreMetricsClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Metrics":
            return cls.model_validate(src_dict)

    Metrics.model_rebuild()
else:
    Metrics = GalileoCoreMetricsClass


if issubclass(GalileoCorePydanticJsonEncoderClass, BaseModel):

    class PydanticJsonEncoder(GalileoCorePydanticJsonEncoderClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PydanticJsonEncoder":
            return cls.model_validate(src_dict)

    PydanticJsonEncoder.model_rebuild()
else:
    PydanticJsonEncoder = GalileoCorePydanticJsonEncoderClass


if issubclass(GalileoCoreRetrieverSpanClass, BaseModel):

    class RetrieverSpan(GalileoCoreRetrieverSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RetrieverSpan":
            return cls.model_validate(src_dict)

    RetrieverSpan.model_rebuild()
else:
    RetrieverSpan = GalileoCoreRetrieverSpanClass


if issubclass(GalileoCoreStepTypeClass, BaseModel):

    class StepType(GalileoCoreStepTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StepType":
            return cls.model_validate(src_dict)

    StepType.model_rebuild()
else:
    StepType = GalileoCoreStepTypeClass


if issubclass(GalileoCoreStepWithChildSpansClass, BaseModel):

    class StepWithChildSpans(GalileoCoreStepWithChildSpansClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "StepWithChildSpans":
            return cls.model_validate(src_dict)

    StepWithChildSpans.model_rebuild()
else:
    StepWithChildSpans = GalileoCoreStepWithChildSpansClass


if issubclass(GalileoCoreToolSpanClass, BaseModel):

    class ToolSpan(GalileoCoreToolSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ToolSpan":
            return cls.model_validate(src_dict)

    ToolSpan.model_rebuild()
else:
    ToolSpan = GalileoCoreToolSpanClass


if issubclass(GalileoCoreWorkflowSpanClass, BaseModel):

    class WorkflowSpan(GalileoCoreWorkflowSpanClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "WorkflowSpan":
            return cls.model_validate(src_dict)

    WorkflowSpan.model_rebuild()
else:
    WorkflowSpan = GalileoCoreWorkflowSpanClass


if issubclass(GalileoCoreAuthMethodClass, BaseModel):

    class AuthMethod(GalileoCoreAuthMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AuthMethod":
            return cls.model_validate(src_dict)

    AuthMethod.model_rebuild()
else:
    AuthMethod = GalileoCoreAuthMethodClass


if issubclass(GalileoCoreGalileoConfigClass, BaseModel):

    class GalileoConfig(GalileoCoreGalileoConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoConfig":
            return cls.model_validate(src_dict)

    GalileoConfig.model_rebuild()
else:
    GalileoConfig = GalileoCoreGalileoConfigClass


if issubclass(GalileoCoreInviteUsersRequestClass, BaseModel):

    class InviteUsersRequest(GalileoCoreInviteUsersRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "InviteUsersRequest":
            return cls.model_validate(src_dict)

    InviteUsersRequest.model_rebuild()
else:
    InviteUsersRequest = GalileoCoreInviteUsersRequestClass


if issubclass(GalileoCoreRequestMethodClass, BaseModel):

    class RequestMethod(GalileoCoreRequestMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RequestMethod":
            return cls.model_validate(src_dict)

    RequestMethod.model_rebuild()
else:
    RequestMethod = GalileoCoreRequestMethodClass


if issubclass(GalileoCoreRoutesClass, BaseModel):

    class Routes(GalileoCoreRoutesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Routes":
            return cls.model_validate(src_dict)

    Routes.model_rebuild()
else:
    Routes = GalileoCoreRoutesClass


if issubclass(GalileoCoreUpdateUserRoleRequestClass, BaseModel):

    class UpdateUserRoleRequest(GalileoCoreUpdateUserRoleRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UpdateUserRoleRequest":
            return cls.model_validate(src_dict)

    UpdateUserRoleRequest.model_rebuild()
else:
    UpdateUserRoleRequest = GalileoCoreUpdateUserRoleRequestClass


if issubclass(GalileoCoreUserClass, BaseModel):

    class User(GalileoCoreUserClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "User":
            return cls.model_validate(src_dict)

    User.model_rebuild()
else:
    User = GalileoCoreUserClass


if issubclass(GalileoCoreUserRoleClass, BaseModel):

    class UserRole(GalileoCoreUserRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UserRole":
            return cls.model_validate(src_dict)

    UserRole.model_rebuild()
else:
    UserRole = GalileoCoreUserRoleClass


if issubclass(GalileoCoreAsyncExecutorClass, BaseModel):

    class AsyncExecutor(GalileoCoreAsyncExecutorClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AsyncExecutor":
            return cls.model_validate(src_dict)

    AsyncExecutor.model_rebuild()
else:
    AsyncExecutor = GalileoCoreAsyncExecutorClass


if issubclass(GalileoCoreGalileoConfigClass, BaseModel):

    class GalileoConfig(GalileoCoreGalileoConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoConfig":
            return cls.model_validate(src_dict)

    GalileoConfig.model_rebuild()
else:
    GalileoConfig = GalileoCoreGalileoConfigClass


if issubclass(GalileoCoreRequestMethodClass, BaseModel):

    class RequestMethod(GalileoCoreRequestMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RequestMethod":
            return cls.model_validate(src_dict)

    RequestMethod.model_rebuild()
else:
    RequestMethod = GalileoCoreRequestMethodClass


if issubclass(GalileoCoreRoutesClass, BaseModel):

    class Routes(GalileoCoreRoutesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Routes":
            return cls.model_validate(src_dict)

    Routes.model_rebuild()
else:
    Routes = GalileoCoreRoutesClass


if issubclass(GalileoCoreCollaboratorRoleClass, BaseModel):

    class CollaboratorRole(GalileoCoreCollaboratorRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CollaboratorRole":
            return cls.model_validate(src_dict)

    CollaboratorRole.model_rebuild()
else:
    CollaboratorRole = GalileoCoreCollaboratorRoleClass


if issubclass(GalileoCoreGalileoConfigClass, BaseModel):

    class GalileoConfig(GalileoCoreGalileoConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoConfig":
            return cls.model_validate(src_dict)

    GalileoConfig.model_rebuild()
else:
    GalileoConfig = GalileoCoreGalileoConfigClass


if issubclass(GalileoCoreRequestMethodClass, BaseModel):

    class RequestMethod(GalileoCoreRequestMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RequestMethod":
            return cls.model_validate(src_dict)

    RequestMethod.model_rebuild()
else:
    RequestMethod = GalileoCoreRequestMethodClass


if issubclass(GalileoCoreRoutesClass, BaseModel):

    class Routes(GalileoCoreRoutesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Routes":
            return cls.model_validate(src_dict)

    Routes.model_rebuild()
else:
    Routes = GalileoCoreRoutesClass


if issubclass(GalileoCoreUserProjectCollaboratorRequestClass, BaseModel):

    class UserProjectCollaboratorRequest(GalileoCoreUserProjectCollaboratorRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UserProjectCollaboratorRequest":
            return cls.model_validate(src_dict)

    UserProjectCollaboratorRequest.model_rebuild()
else:
    UserProjectCollaboratorRequest = GalileoCoreUserProjectCollaboratorRequestClass


if issubclass(GalileoCoreUserProjectCollaboratorResponseClass, BaseModel):

    class UserProjectCollaboratorResponse(GalileoCoreUserProjectCollaboratorResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UserProjectCollaboratorResponse":
            return cls.model_validate(src_dict)

    UserProjectCollaboratorResponse.model_rebuild()
else:
    UserProjectCollaboratorResponse = GalileoCoreUserProjectCollaboratorResponseClass


if issubclass(GalileoCoreApiKeyResponseClass, BaseModel):

    class ApiKeyResponse(GalileoCoreApiKeyResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ApiKeyResponse":
            return cls.model_validate(src_dict)

    ApiKeyResponse.model_rebuild()
else:
    ApiKeyResponse = GalileoCoreApiKeyResponseClass


if issubclass(GalileoCoreCollaboratorRoleClass, BaseModel):

    class CollaboratorRole(GalileoCoreCollaboratorRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CollaboratorRole":
            return cls.model_validate(src_dict)

    CollaboratorRole.model_rebuild()
else:
    CollaboratorRole = GalileoCoreCollaboratorRoleClass


if issubclass(GalileoCoreCreateApiKeyRequestClass, BaseModel):

    class CreateApiKeyRequest(GalileoCoreCreateApiKeyRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CreateApiKeyRequest":
            return cls.model_validate(src_dict)

    CreateApiKeyRequest.model_rebuild()
else:
    CreateApiKeyRequest = GalileoCoreCreateApiKeyRequestClass


if issubclass(GalileoCoreCreateApiKeyResponseClass, BaseModel):

    class CreateApiKeyResponse(GalileoCoreCreateApiKeyResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CreateApiKeyResponse":
            return cls.model_validate(src_dict)

    CreateApiKeyResponse.model_rebuild()
else:
    CreateApiKeyResponse = GalileoCoreCreateApiKeyResponseClass


if issubclass(GalileoCoreGalileoConfigClass, BaseModel):

    class GalileoConfig(GalileoCoreGalileoConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoConfig":
            return cls.model_validate(src_dict)

    GalileoConfig.model_rebuild()
else:
    GalileoConfig = GalileoCoreGalileoConfigClass


if issubclass(GalileoCoreRequestMethodClass, BaseModel):

    class RequestMethod(GalileoCoreRequestMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RequestMethod":
            return cls.model_validate(src_dict)

    RequestMethod.model_rebuild()
else:
    RequestMethod = GalileoCoreRequestMethodClass


if issubclass(GalileoCoreRoutesClass, BaseModel):

    class Routes(GalileoCoreRoutesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Routes":
            return cls.model_validate(src_dict)

    Routes.model_rebuild()
else:
    Routes = GalileoCoreRoutesClass


if issubclass(GalileoCoreDatasetClass, BaseModel):

    class Dataset(GalileoCoreDatasetClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Dataset":
            return cls.model_validate(src_dict)

    Dataset.model_rebuild()
else:
    Dataset = GalileoCoreDatasetClass


if issubclass(GalileoCoreGalileoConfigClass, BaseModel):

    class GalileoConfig(GalileoCoreGalileoConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoConfig":
            return cls.model_validate(src_dict)

    GalileoConfig.model_rebuild()
else:
    GalileoConfig = GalileoCoreGalileoConfigClass


if issubclass(GalileoCoreRequestMethodClass, BaseModel):

    class RequestMethod(GalileoCoreRequestMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RequestMethod":
            return cls.model_validate(src_dict)

    RequestMethod.model_rebuild()
else:
    RequestMethod = GalileoCoreRequestMethodClass


if issubclass(GalileoCoreRoutesClass, BaseModel):

    class Routes(GalileoCoreRoutesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Routes":
            return cls.model_validate(src_dict)

    Routes.model_rebuild()
else:
    Routes = GalileoCoreRoutesClass


if issubclass(GalileoCoreUploadDatasetRequestClass, BaseModel):

    class UploadDatasetRequest(GalileoCoreUploadDatasetRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "UploadDatasetRequest":
            return cls.model_validate(src_dict)

    UploadDatasetRequest.model_rebuild()
else:
    UploadDatasetRequest = GalileoCoreUploadDatasetRequestClass


if issubclass(GalileoCoreAddGroupMemberRequestClass, BaseModel):

    class AddGroupMemberRequest(GalileoCoreAddGroupMemberRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AddGroupMemberRequest":
            return cls.model_validate(src_dict)

    AddGroupMemberRequest.model_rebuild()
else:
    AddGroupMemberRequest = GalileoCoreAddGroupMemberRequestClass


if issubclass(GalileoCoreAddGroupMemberResponseClass, BaseModel):

    class AddGroupMemberResponse(GalileoCoreAddGroupMemberResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "AddGroupMemberResponse":
            return cls.model_validate(src_dict)

    AddGroupMemberResponse.model_rebuild()
else:
    AddGroupMemberResponse = GalileoCoreAddGroupMemberResponseClass


if issubclass(GalileoCoreCreateGroupRequestClass, BaseModel):

    class CreateGroupRequest(GalileoCoreCreateGroupRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CreateGroupRequest":
            return cls.model_validate(src_dict)

    CreateGroupRequest.model_rebuild()
else:
    CreateGroupRequest = GalileoCoreCreateGroupRequestClass


if issubclass(GalileoCoreCreateGroupResponseClass, BaseModel):

    class CreateGroupResponse(GalileoCoreCreateGroupResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CreateGroupResponse":
            return cls.model_validate(src_dict)

    CreateGroupResponse.model_rebuild()
else:
    CreateGroupResponse = GalileoCoreCreateGroupResponseClass


if issubclass(GalileoCoreGalileoConfigClass, BaseModel):

    class GalileoConfig(GalileoCoreGalileoConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoConfig":
            return cls.model_validate(src_dict)

    GalileoConfig.model_rebuild()
else:
    GalileoConfig = GalileoCoreGalileoConfigClass


if issubclass(GalileoCoreGroupRoleClass, BaseModel):

    class GroupRole(GalileoCoreGroupRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GroupRole":
            return cls.model_validate(src_dict)

    GroupRole.model_rebuild()
else:
    GroupRole = GalileoCoreGroupRoleClass


if issubclass(GalileoCoreGroupVisibilityClass, BaseModel):

    class GroupVisibility(GalileoCoreGroupVisibilityClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GroupVisibility":
            return cls.model_validate(src_dict)

    GroupVisibility.model_rebuild()
else:
    GroupVisibility = GalileoCoreGroupVisibilityClass


if issubclass(GalileoCoreRequestMethodClass, BaseModel):

    class RequestMethod(GalileoCoreRequestMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RequestMethod":
            return cls.model_validate(src_dict)

    RequestMethod.model_rebuild()
else:
    RequestMethod = GalileoCoreRequestMethodClass


if issubclass(GalileoCoreRoutesClass, BaseModel):

    class Routes(GalileoCoreRoutesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Routes":
            return cls.model_validate(src_dict)

    Routes.model_rebuild()
else:
    Routes = GalileoCoreRoutesClass


if issubclass(GalileoCorePaginationRequestClass, BaseModel):

    class PaginationRequest(GalileoCorePaginationRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PaginationRequest":
            return cls.model_validate(src_dict)

    PaginationRequest.model_rebuild()
else:
    PaginationRequest = GalileoCorePaginationRequestClass


if issubclass(GalileoCorePaginationResponseClass, BaseModel):

    class PaginationResponse(GalileoCorePaginationResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "PaginationResponse":
            return cls.model_validate(src_dict)

    PaginationResponse.model_rebuild()
else:
    PaginationResponse = GalileoCorePaginationResponseClass


if issubclass(GalileoCoreApiClientClass, BaseModel):

    class ApiClient(GalileoCoreApiClientClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ApiClient":
            return cls.model_validate(src_dict)

    ApiClient.model_rebuild()
else:
    ApiClient = GalileoCoreApiClientClass


if issubclass(GalileoCoreGalileoHTTPExceptionClass, BaseModel):

    class GalileoHTTPException(GalileoCoreGalileoHTTPExceptionClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoHTTPException":
            return cls.model_validate(src_dict)

    GalileoHTTPException.model_rebuild()
else:
    GalileoHTTPException = GalileoCoreGalileoHTTPExceptionClass


if issubclass(GalileoCoreHttpHeadersClass, BaseModel):

    class HttpHeaders(GalileoCoreHttpHeadersClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "HttpHeaders":
            return cls.model_validate(src_dict)

    HttpHeaders.model_rebuild()
else:
    HttpHeaders = GalileoCoreHttpHeadersClass


if issubclass(GalileoCoreRequestMethodClass, BaseModel):

    class RequestMethod(GalileoCoreRequestMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RequestMethod":
            return cls.model_validate(src_dict)

    RequestMethod.model_rebuild()
else:
    RequestMethod = GalileoCoreRequestMethodClass


if issubclass(GalileoCoreCollaboratorRoleClass, BaseModel):

    class CollaboratorRole(GalileoCoreCollaboratorRoleClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CollaboratorRole":
            return cls.model_validate(src_dict)

    CollaboratorRole.model_rebuild()
else:
    CollaboratorRole = GalileoCoreCollaboratorRoleClass


if issubclass(GalileoCoreGalileoConfigClass, BaseModel):

    class GalileoConfig(GalileoCoreGalileoConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoConfig":
            return cls.model_validate(src_dict)

    GalileoConfig.model_rebuild()
else:
    GalileoConfig = GalileoCoreGalileoConfigClass


if issubclass(GalileoCoreGroupProjectCollaboratorRequestClass, BaseModel):

    class GroupProjectCollaboratorRequest(GalileoCoreGroupProjectCollaboratorRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GroupProjectCollaboratorRequest":
            return cls.model_validate(src_dict)

    GroupProjectCollaboratorRequest.model_rebuild()
else:
    GroupProjectCollaboratorRequest = GalileoCoreGroupProjectCollaboratorRequestClass


if issubclass(GalileoCoreGroupProjectCollaboratorResponseClass, BaseModel):

    class GroupProjectCollaboratorResponse(GalileoCoreGroupProjectCollaboratorResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GroupProjectCollaboratorResponse":
            return cls.model_validate(src_dict)

    GroupProjectCollaboratorResponse.model_rebuild()
else:
    GroupProjectCollaboratorResponse = GalileoCoreGroupProjectCollaboratorResponseClass


if issubclass(GalileoCoreRequestMethodClass, BaseModel):

    class RequestMethod(GalileoCoreRequestMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RequestMethod":
            return cls.model_validate(src_dict)

    RequestMethod.model_rebuild()
else:
    RequestMethod = GalileoCoreRequestMethodClass


if issubclass(GalileoCoreRoutesClass, BaseModel):

    class Routes(GalileoCoreRoutesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Routes":
            return cls.model_validate(src_dict)

    Routes.model_rebuild()
else:
    Routes = GalileoCoreRoutesClass


if issubclass(GalileoCoreCreateProjectRequestClass, BaseModel):

    class CreateProjectRequest(GalileoCoreCreateProjectRequestClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "CreateProjectRequest":
            return cls.model_validate(src_dict)

    CreateProjectRequest.model_rebuild()
else:
    CreateProjectRequest = GalileoCoreCreateProjectRequestClass


if issubclass(GalileoCoreGalileoConfigClass, BaseModel):

    class GalileoConfig(GalileoCoreGalileoConfigClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "GalileoConfig":
            return cls.model_validate(src_dict)

    GalileoConfig.model_rebuild()
else:
    GalileoConfig = GalileoCoreGalileoConfigClass


if issubclass(GalileoCoreProjectResponseClass, BaseModel):

    class ProjectResponse(GalileoCoreProjectResponseClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ProjectResponse":
            return cls.model_validate(src_dict)

    ProjectResponse.model_rebuild()
else:
    ProjectResponse = GalileoCoreProjectResponseClass


if issubclass(GalileoCoreProjectTypeClass, BaseModel):

    class ProjectType(GalileoCoreProjectTypeClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "ProjectType":
            return cls.model_validate(src_dict)

    ProjectType.model_rebuild()
else:
    ProjectType = GalileoCoreProjectTypeClass


if issubclass(GalileoCoreRequestMethodClass, BaseModel):

    class RequestMethod(GalileoCoreRequestMethodClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "RequestMethod":
            return cls.model_validate(src_dict)

    RequestMethod.model_rebuild()
else:
    RequestMethod = GalileoCoreRequestMethodClass


if issubclass(GalileoCoreRoutesClass, BaseModel):

    class Routes(GalileoCoreRoutesClass):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "Routes":
            return cls.model_validate(src_dict)

    Routes.model_rebuild()
else:
    Routes = GalileoCoreRoutesClass
