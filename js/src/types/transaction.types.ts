import { StepType } from './step.types';

export enum TransactionLoggingMethod {
  js_langchain = 'js_langchain',
  js_logger = 'js_logger'
}

export interface TransactionRecord {
  latency_ms?: number;
  status_code?: number;
  input_text: string;
  output_text?: string;
  tools?: string;
  model?: string;
  num_input_tokens?: number;
  num_output_tokens?: number;
  num_total_tokens?: number;
  finish_reason?: string;
  node_id: string;
  chain_id?: string;
  chain_root_id?: string;
  output_logprobs?: Record<string, unknown>;
  created_at: string;
  tags?: string[];
  user_metadata?: Record<string, unknown>;
  temperature?: number;
  node_type: StepType;
  has_children: boolean;
  time_to_first_token_ms?: number;
  version?: string;
}

export interface TransactionRecordBatch {
  records: TransactionRecord[];
  logging_method: TransactionLoggingMethod;
  client_version: string;
}
