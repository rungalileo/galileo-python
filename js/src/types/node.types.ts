export interface Node {
  node_id: string;
  node_type: string;
  node_name?: string;
  node_input: string;
  node_output: string;
  chain_root_id: string;
  step: number;
  chain_id?: string;
  has_children: boolean;
  inputs: Record<string, unknown>;
  prompt?: string;
  response?: string;
  creation_timestamp: number;
  finish_reason: string;
  latency?: number | null;
  query_input_tokens: number;
  query_output_tokens: number;
  query_total_tokens: number;
  params: Record<string, unknown>;
  target?: string;
  tools?: string;
}
