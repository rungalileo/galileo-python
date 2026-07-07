from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_poll_template import ChainPollTemplate
    from ..models.file_content_part import FileContentPart
    from ..models.generated_scorer_configuration import GeneratedScorerConfiguration
    from ..models.text_content_part import TextContentPart
    from ..models.validate_llm_scorer_dataset_request_sort_type_0 import ValidateLLMScorerDatasetRequestSortType0


T = TypeVar("T", bound="ValidateLLMScorerDatasetRequest")


@_attrs_define
class ValidateLLMScorerDatasetRequest:
    """Request to validate a new LLM scorer against a dataset.

    Attributes:
        query (str):
        response (str):
        chain_poll_template (ChainPollTemplate): Template for a chainpoll metric prompt,
            containing all the info necessary to send a chainpoll prompt.
        scorer_configuration (GeneratedScorerConfiguration):
        user_prompt (str):
        dataset_id (str):
        normalized_input (Union[None, Unset, list[Union['FileContentPart', 'TextContentPart']]]): Optional multimodal
            content parts. When set, replaces the text-only query/response formatting in the validation job so that file
            content is passed through to the LLM.
        dataset_version_index (Union[None, Unset, int]):
        limit (Union[Unset, int]): Maximum number of dataset rows to process. Default: 100.
        starting_token (Union[None, Unset, int]): Pagination offset into dataset rows.
        sort (Union['ValidateLLMScorerDatasetRequestSortType0', None, Unset]): Optional sort configuration for dataset
            rows.
    """

    query: str
    response: str
    chain_poll_template: "ChainPollTemplate"
    scorer_configuration: "GeneratedScorerConfiguration"
    user_prompt: str
    dataset_id: str
    normalized_input: Union[None, Unset, list[Union["FileContentPart", "TextContentPart"]]] = UNSET
    dataset_version_index: Union[None, Unset, int] = UNSET
    limit: Union[Unset, int] = 100
    starting_token: Union[None, Unset, int] = UNSET
    sort: Union["ValidateLLMScorerDatasetRequestSortType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.text_content_part import TextContentPart
        from ..models.validate_llm_scorer_dataset_request_sort_type_0 import ValidateLLMScorerDatasetRequestSortType0

        query = self.query

        response = self.response

        chain_poll_template = self.chain_poll_template.to_dict()

        scorer_configuration = self.scorer_configuration.to_dict()

        user_prompt = self.user_prompt

        dataset_id = self.dataset_id

        normalized_input: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.normalized_input, Unset):
            normalized_input = UNSET
        elif isinstance(self.normalized_input, list):
            normalized_input = []
            for normalized_input_type_0_item_data in self.normalized_input:
                normalized_input_type_0_item: dict[str, Any]
                if isinstance(normalized_input_type_0_item_data, TextContentPart):
                    normalized_input_type_0_item = normalized_input_type_0_item_data.to_dict()
                else:
                    normalized_input_type_0_item = normalized_input_type_0_item_data.to_dict()

                normalized_input.append(normalized_input_type_0_item)

        else:
            normalized_input = self.normalized_input

        dataset_version_index: Union[None, Unset, int]
        if isinstance(self.dataset_version_index, Unset):
            dataset_version_index = UNSET
        else:
            dataset_version_index = self.dataset_version_index

        limit = self.limit

        starting_token: Union[None, Unset, int]
        if isinstance(self.starting_token, Unset):
            starting_token = UNSET
        else:
            starting_token = self.starting_token

        sort: Union[None, Unset, dict[str, Any]]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, ValidateLLMScorerDatasetRequestSortType0):
            sort = self.sort.to_dict()
        else:
            sort = self.sort

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "response": response,
                "chain_poll_template": chain_poll_template,
                "scorer_configuration": scorer_configuration,
                "user_prompt": user_prompt,
                "dataset_id": dataset_id,
            }
        )
        if normalized_input is not UNSET:
            field_dict["normalized_input"] = normalized_input
        if dataset_version_index is not UNSET:
            field_dict["dataset_version_index"] = dataset_version_index
        if limit is not UNSET:
            field_dict["limit"] = limit
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token
        if sort is not UNSET:
            field_dict["sort"] = sort

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.file_content_part import FileContentPart
        from ..models.generated_scorer_configuration import GeneratedScorerConfiguration
        from ..models.text_content_part import TextContentPart
        from ..models.validate_llm_scorer_dataset_request_sort_type_0 import ValidateLLMScorerDatasetRequestSortType0

        d = dict(src_dict)
        query = d.pop("query")

        response = d.pop("response")

        chain_poll_template = ChainPollTemplate.from_dict(d.pop("chain_poll_template"))

        scorer_configuration = GeneratedScorerConfiguration.from_dict(d.pop("scorer_configuration"))

        user_prompt = d.pop("user_prompt")

        dataset_id = d.pop("dataset_id")

        def _parse_normalized_input(
            data: object,
        ) -> Union[None, Unset, list[Union["FileContentPart", "TextContentPart"]]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                normalized_input_type_0 = []
                _normalized_input_type_0 = data
                for normalized_input_type_0_item_data in _normalized_input_type_0:

                    def _parse_normalized_input_type_0_item(
                        data: object,
                    ) -> Union["FileContentPart", "TextContentPart"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            normalized_input_type_0_item_type_0 = TextContentPart.from_dict(data)

                            return normalized_input_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        normalized_input_type_0_item_type_1 = FileContentPart.from_dict(data)

                        return normalized_input_type_0_item_type_1

                    normalized_input_type_0_item = _parse_normalized_input_type_0_item(
                        normalized_input_type_0_item_data
                    )

                    normalized_input_type_0.append(normalized_input_type_0_item)

                return normalized_input_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Union["FileContentPart", "TextContentPart"]]], data)

        normalized_input = _parse_normalized_input(d.pop("normalized_input", UNSET))

        def _parse_dataset_version_index(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        dataset_version_index = _parse_dataset_version_index(d.pop("dataset_version_index", UNSET))

        limit = d.pop("limit", UNSET)

        def _parse_starting_token(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        starting_token = _parse_starting_token(d.pop("starting_token", UNSET))

        def _parse_sort(data: object) -> Union["ValidateLLMScorerDatasetRequestSortType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0 = ValidateLLMScorerDatasetRequestSortType0.from_dict(data)

                return sort_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ValidateLLMScorerDatasetRequestSortType0", None, Unset], data)

        sort = _parse_sort(d.pop("sort", UNSET))

        validate_llm_scorer_dataset_request = cls(
            query=query,
            response=response,
            chain_poll_template=chain_poll_template,
            scorer_configuration=scorer_configuration,
            user_prompt=user_prompt,
            dataset_id=dataset_id,
            normalized_input=normalized_input,
            dataset_version_index=dataset_version_index,
            limit=limit,
            starting_token=starting_token,
            sort=sort,
        )

        validate_llm_scorer_dataset_request.additional_properties = d
        return validate_llm_scorer_dataset_request

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
