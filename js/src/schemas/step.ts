/* eslint-disable @typescript-eslint/no-explicit-any */

import { StepIOType } from '../types/step.types';
import { Document } from './document';
import { Message } from './message';

enum NodeType {
  chain = 'chain',
  chat = 'chat',
  llm = 'llm',
  retriever = 'retriever',
  tool = 'tool',
  agent = 'agent',
  workflow = 'workflow',
  trace = 'trace'
}

// Type definitions

export type LlmStepAllowedIOType =
  | string
  | Record<string, string>
  | Message
  | string[]
  | Record<string, string>[]
  | Message[];

export type RetrieverStepAllowedOutputType =
  | string[]
  | Record<string, string>[]
  | Document[];

// Base classes
export class BaseStep {
  type: NodeType = NodeType.workflow;
  input: StepIOType;
  output: StepIOType = '';
  name: string = '';
  createdAtNs: number = Date.now() * 1000000; // Convert to nanoseconds
  durationNs: number = 0;
  metadata: Record<string, string> = {};
  statusCode?: number;
  groundTruth?: string;

  constructor(data: {
    type?: NodeType;
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    createdAtNs?: number;
    durationNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
    groundTruth?: string;
  }) {
    this.type = data.type || NodeType.workflow;
    this.input = data.input;
    this.output = data.output !== undefined ? data.output : '';
    this.name = data.name || data.type || NodeType.workflow;
    this.createdAtNs =
      data.createdAtNs !== undefined ? data.createdAtNs : Date.now() * 1000000;
    this.durationNs = data.durationNs !== undefined ? data.durationNs : 0;
    this.metadata = data.metadata || {};
    this.statusCode = data.statusCode;
    this.groundTruth = data.groundTruth;

    // Validate serializable
    this.validateInputOutputSerializable(this.input);
    this.validateInputOutputSerializable(this.output);
  }

  validateInputOutputSerializable(val: StepIOType): StepIOType {
    // Make sure we can serialize input/output to JSON string
    JSON.stringify(val);
    return val;
  }

  toJSON(): Record<string, any> {
    return {
      type: this.type,
      input: this.input,
      output: this.output,
      name: this.name,
      createdAtNs: this.createdAtNs,
      durationNs: this.durationNs,
      metadata: this.metadata,
      statusCode: this.statusCode,
      groundTruth: this.groundTruth
    };
  }
}

export abstract class BaseStepWithChildren extends BaseStep {
  abstract children(): BaseStep[];
}

export class StepWithChildren extends BaseStepWithChildren {
  steps: AWorkflowStep[] = [];
  parent?: StepWithChildren;

  constructor(data: {
    type?: NodeType;
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    createdAtNs?: number;
    durationNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
    groundTruth?: string;
    steps?: AWorkflowStep[];
    parent?: StepWithChildren;
  }) {
    super(data);
    this.steps = data.steps || [];
    this.parent = data.parent;
  }

  children(): BaseStep[] {
    return this.steps;
  }

  addLlm(params: {
    input: LlmStepAllowedIOType;
    output: LlmStepAllowedIOType;
    model: string;
    tools?: Record<string, any>[];
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    inputTokens?: number;
    outputTokens?: number;
    totalTokens?: number;
    temperature?: number;
    statusCode?: number;
  }): LlmStep {
    const step = new LlmStep({
      input: params.input,
      output: params.output,
      model: params.model,
      tools: params.tools,
      name: params.name,
      durationNs: params.durationNs,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata,
      inputTokens: params.inputTokens,
      outputTokens: params.outputTokens,
      totalTokens: params.totalTokens,
      temperature: params.temperature,
      statusCode: params.statusCode
    });
    this.steps.push(step);
    return step;
  }

  addRetriever(params: {
    input: StepIOType;
    documents: RetrieverStepAllowedOutputType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
  }): RetrieverStep {
    const step = new RetrieverStep({
      input: params.input as string,
      output: params.documents,
      name: params.name,
      durationNs: params.durationNs,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata,
      statusCode: params.statusCode
    });
    this.steps.push(step);
    return step;
  }

  addTool(params: {
    input: StepIOType;
    output: StepIOType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
  }): ToolStep {
    const step = new ToolStep({
      input: params.input,
      output: params.output,
      name: params.name,
      durationNs: params.durationNs,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata,
      statusCode: params.statusCode
    });
    this.steps.push(step);
    return step;
  }

  addProtect(params: {
    payload: any; // Payload type
    response: any; // Response type
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
  }): ToolStep {
    const step = new ToolStep({
      input: params.payload,
      output: params.response,
      name: 'GalileoProtect',
      durationNs:
        params.response.traceMetadata.responseAt -
        params.response.traceMetadata.receivedAt,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata,
      statusCode: params.statusCode
    });
    this.steps.push(step);
    return step;
  }

  addSubWorkflow(params: {
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
  }): WorkflowStep {
    const step = new WorkflowStep({
      parent: this,
      input: params.input,
      output: params.output || '',
      name: params.name,
      durationNs: params.durationNs,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata
    });
    this.steps.push(step);
    return step;
  }

  addSubAgent(params: {
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
  }): AgentStep {
    const step = new AgentStep({
      parent: this,
      input: params.input,
      output: params.output || '',
      name: params.name,
      durationNs: params.durationNs,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata
    });
    this.steps.push(step);
    return step;
  }

  conclude(params?: {
    output?: StepIOType;
    durationNs?: number;
    statusCode?: number;
  }): StepWithChildren | undefined {
    if (params?.output !== undefined) {
      this.output = params.output;
    }
    if (params?.statusCode !== undefined) {
      this.statusCode = params.statusCode;
    }
    if (params?.durationNs !== undefined) {
      this.durationNs = params.durationNs;
    }
    return this.parent;
  }
}

export class WorkflowStep extends StepWithChildren {
  type: NodeType = NodeType.workflow;

  constructor(data: {
    type?: NodeType;
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    createdAtNs?: number;
    durationNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
    groundTruth?: string;
    steps?: AWorkflowStep[];
    parent?: StepWithChildren;
  }) {
    super({ ...data, type: NodeType.workflow });
  }
}

export class ChainStep extends StepWithChildren {
  type: NodeType = NodeType.chain;

  constructor(data: {
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    createdAtNs?: number;
    durationNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
    groundTruth?: string;
    steps?: AWorkflowStep[];
    parent?: StepWithChildren;
  }) {
    super({ ...data, type: NodeType.chain });
  }
}

export class LlmStep extends BaseStep {
  type: NodeType = NodeType.llm;
  input: LlmStepAllowedIOType;
  output: LlmStepAllowedIOType = '';
  tools?: Record<string, any>[];
  model?: string;
  inputTokens?: number;
  outputTokens?: number;
  totalTokens?: number;
  temperature?: number;

  constructor(data: {
    input: LlmStepAllowedIOType;
    output: LlmStepAllowedIOType;
    model?: string;
    tools?: Record<string, any>[];
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
    groundTruth?: string;
    inputTokens?: number;
    outputTokens?: number;
    totalTokens?: number;
    temperature?: number;
  }) {
    super({ ...data, type: NodeType.llm });
    this.input = data.input;
    this.output = data.output;
    this.tools = data.tools;
    this.model = data.model;
    this.inputTokens = data.inputTokens;
    this.outputTokens = data.outputTokens;
    this.totalTokens = data.totalTokens;
    this.temperature = data.temperature;
  }
}

export class RetrieverStep extends BaseStep {
  type: NodeType = NodeType.retriever;
  input: StepIOType;
  output: Document[] = [];

  constructor(data: {
    input: StepIOType;
    output: string[] | Record<string, string>[] | Document[];
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
    groundTruth?: string;
  }) {
    super({ ...data, type: NodeType.retriever });
    this.input = data.input;
    this.output = this.setOutput(data.output);
  }

  setOutput(
    value: string[] | Record<string, string>[] | Document[]
  ): Document[] {
    if (typeof value === 'string') {
      try {
        value = JSON.parse(value);
      } catch (e) {
        // If parsing fails, continue with the original value
      }
    }

    if (Array.isArray(value)) {
      if (value.every((doc) => typeof doc === 'string')) {
        return value.map((doc) => new Document({ content: doc }));
      } else if (
        value.every((doc) => typeof doc === 'object' && doc !== null)
      ) {
        // @ts-expect-error - TODO: Type this
        return value.map((doc) => new Document(doc));
      } else if (value.every((doc) => doc instanceof Document)) {
        return value.map((doc) => new Document(doc));
      }
      throw new Error(
        'Retriever output must be a list of strings, a list of dicts, or a list of Documents.'
      );
    }
    throw new Error(
      'Retriever output must be a list of strings, a list of dicts or a list of Documents.'
    );
  }
}

export class ToolStep extends BaseStep {
  type: NodeType = NodeType.tool;

  constructor(data: {
    input: StepIOType;
    output: StepIOType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
    groundTruth?: string;
  }) {
    super({ ...data, type: NodeType.tool });
  }
}

export class AgentStep extends StepWithChildren {
  type: NodeType = NodeType.agent;

  constructor(data: {
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
    groundTruth?: string;
    steps?: AWorkflowStep[];
    parent?: StepWithChildren;
  }) {
    super({ ...data, type: NodeType.agent });
  }
}

// Note: This is a simplified version as TypeScript doesn't have direct equivalent to Python's Annotated union type
// with discriminator. In practice, you'd typically use a type union.
export type AWorkflowStep =
  | WorkflowStep
  | ChainStep
  | LlmStep
  | RetrieverStep
  | ToolStep
  | AgentStep;
