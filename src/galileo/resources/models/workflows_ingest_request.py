from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_step import AgentStep
    from ..models.chain_step import ChainStep
    from ..models.llm_step import LlmStep
    from ..models.retriever_step import RetrieverStep
    from ..models.tool_step import ToolStep
    from ..models.workflow_step import WorkflowStep


T = TypeVar("T", bound="WorkflowsIngestRequest")


@_attrs_define
class WorkflowsIngestRequest:
    """
    Attributes:
        workflows (list[Union['AgentStep', 'ChainStep', 'LlmStep', 'RetrieverStep', 'ToolStep', 'WorkflowStep']]): List
            of workflows to log.
        project_id (Union[None, Unset, str]): Project ID for the Observe project.
        project_name (Union[None, Unset, str]): Project name for the Observe project.
    """

    workflows: list[Union["AgentStep", "ChainStep", "LlmStep", "RetrieverStep", "ToolStep", "WorkflowStep"]]
    project_id: Union[None, Unset, str] = UNSET
    project_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chain_step import ChainStep
        from ..models.llm_step import LlmStep
        from ..models.retriever_step import RetrieverStep
        from ..models.tool_step import ToolStep
        from ..models.workflow_step import WorkflowStep

        workflows = []
        for workflows_item_data in self.workflows:
            workflows_item: dict[str, Any]
            if isinstance(workflows_item_data, WorkflowStep):
                workflows_item = workflows_item_data.to_dict()
            elif isinstance(workflows_item_data, ChainStep):
                workflows_item = workflows_item_data.to_dict()
            elif isinstance(workflows_item_data, LlmStep):
                workflows_item = workflows_item_data.to_dict()
            elif isinstance(workflows_item_data, RetrieverStep):
                workflows_item = workflows_item_data.to_dict()
            elif isinstance(workflows_item_data, ToolStep):
                workflows_item = workflows_item_data.to_dict()
            else:
                workflows_item = workflows_item_data.to_dict()

            workflows.append(workflows_item)

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        project_name: Union[None, Unset, str]
        if isinstance(self.project_name, Unset):
            project_name = UNSET
        else:
            project_name = self.project_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"workflows": workflows})
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if project_name is not UNSET:
            field_dict["project_name"] = project_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.agent_step import AgentStep
        from ..models.chain_step import ChainStep
        from ..models.llm_step import LlmStep
        from ..models.retriever_step import RetrieverStep
        from ..models.tool_step import ToolStep
        from ..models.workflow_step import WorkflowStep

        d = src_dict.copy()
        workflows = []
        _workflows = d.pop("workflows")
        for workflows_item_data in _workflows:

            def _parse_workflows_item(
                data: object,
            ) -> Union["AgentStep", "ChainStep", "LlmStep", "RetrieverStep", "ToolStep", "WorkflowStep"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    workflows_item_type_0 = WorkflowStep.from_dict(data)

                    return workflows_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    workflows_item_type_1 = ChainStep.from_dict(data)

                    return workflows_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    workflows_item_type_2 = LlmStep.from_dict(data)

                    return workflows_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    workflows_item_type_3 = RetrieverStep.from_dict(data)

                    return workflows_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    workflows_item_type_4 = ToolStep.from_dict(data)

                    return workflows_item_type_4
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                workflows_item_type_5 = AgentStep.from_dict(data)

                return workflows_item_type_5

            workflows_item = _parse_workflows_item(workflows_item_data)

            workflows.append(workflows_item)

        def _parse_project_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_project_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_name = _parse_project_name(d.pop("project_name", UNSET))

        workflows_ingest_request = cls(workflows=workflows, project_id=project_id, project_name=project_name)

        workflows_ingest_request.additional_properties = d
        return workflows_ingest_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
