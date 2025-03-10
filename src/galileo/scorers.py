from galileo.base import BaseClientModel
from galileo.resources.api.data import list_scorers_with_filters_scorers_list_post
from galileo.resources.models import ListScorersRequest, ScorerTypeFilter, ScorerTypeFilterOperator, ScorerTypes


class Scorer(BaseClientModel):
    def list(self):
        body = ListScorersRequest(
            filters=[
                ScorerTypeFilter(value=ScorerTypes.PRESET, operator=ScorerTypeFilterOperator.EQ)
                #     ScorerNameFilter(
                #         value=filter_by_name,
                #         operator=ScorerNameFilterOperator.EQ,
                # )
            ]
        )
        result = list_scorers_with_filters_scorers_list_post.sync(client=self.client, body=body)
        return result.scorers
