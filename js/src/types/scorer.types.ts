import { Models } from './models.types';

export interface ScorersConfiguration {
  adherence_nli?: boolean;
  chunk_attribution_utilization_gpt?: boolean;
  chunk_attribution_utilization_nli?: boolean;
  completeness_gpt?: boolean;
  completeness_nli?: boolean;
  context_relevance?: boolean;
  factuality?: boolean;
  groundedness?: boolean;
  instruction_adherence?: boolean;
  ground_truth_adherence?: boolean;
  pii?: boolean;
  prompt_injection?: boolean;
  prompt_perplexity?: boolean;
  sexist?: boolean;
  tone?: boolean;
  tool_selection_quality?: boolean;
  tool_errors?: boolean;
  toxicity?: boolean;
}

export interface RegisteredScorer {
  registered_scorer_id: string;
  metric_name: string;
  score_type?: string;
  scoreable_node_types?: string[];
}

enum CustomizedScorerName {
  chunk_attribution_utilization_plus = '_customized_chunk_attribution_utilization_gpt',
  completeness_plus = '_customized_completeness_gpt',
  context_adherence_plus = '_customized_groundedness',
  correctness = '_customized_factuality',
  instruction_adherence = '_customized_instruction_adherence',
  tool_selection_quality = '_customized_ tool_selection_quality',
  tool_errors = '_customized_tool_errors'
}

export interface CustomizedScorer {
  scorer_name: CustomizedScorerName;
  model_alias?: Models;
  num_judges?: number;
}
