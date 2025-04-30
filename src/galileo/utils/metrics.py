from galileo.schema.metrics import LocalScorerConfig
from galileo_core.schemas.logging.span import Span, StepWithChildSpans
from galileo_core.schemas.logging.trace import Trace


def populate_local_metrics(step: Trace | Span, local_scorers: list[LocalScorerConfig]) -> None:
    if local_scorers:
        for scorer in local_scorers:
            setattr(step.metrics, scorer.name, scorer.func(step))
        if isinstance(step, StepWithChildSpans):
            for span in step.spans:
                populate_local_metrics(span, local_scorers)
