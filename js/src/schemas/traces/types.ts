/* eslint-disable @typescript-eslint/no-explicit-any */

enum NodeType {
  trace = 'trace',
  workflow = 'workflow',
  llm = 'llm',
  retriever = 'retriever',
  tool = 'tool'
}

import { StepIOType } from '../../types/step.types';
import { Document } from '../document';
import {
  BaseStep,
  BaseStepWithChildren,
  LlmStep,
  RetrieverStep,
  ToolStep,
  LlmStepAllowedIOType,
  RetrieverStepAllowedOutputType
} from '../step';

export class SpanWithParentStep extends BaseStep {
  parent?: StepWithChildSpans;

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
    parent?: StepWithChildSpans;
  }) {
    super(data);
    this.parent = data.parent;
  }
}
interface IStepWithChildSpans {
  spans: Span[];
  children(): BaseStep[];
  addChild(...spans: Span[]): void;
  addLlmSpan(params: {
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
    groundTruth?: string;
  }): LlmSpan;
  addRetrieverSpan(params: {
    input: StepIOType;
    documents: RetrieverStepAllowedOutputType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
  }): RetrieverSpan;
  addToolSpan(params: {
    input: StepIOType;
    output: StepIOType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
  }): ToolSpan;
  addWorkflowSpan(params: {
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
  }): WorkflowSpan;
  conclude(params?: {
    output?: StepIOType;
    durationNs?: number;
    statusCode?: number;
  }): StepWithChildSpans | null;
}
export class StepWithChildSpans extends BaseStepWithChildren {
  spans: Span[] = [];

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
    spans?: Span[];
  }) {
    super(data);
    this.spans = data.spans || [];
  }

  children(): BaseStep[] {
    return this.spans;
  }

  addChild(...spans: Span[]): void {
    for (const span of spans) {
      span.parent = this;
      this.spans.push(span);
    }
  }

  addLlmSpan(params: {
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
    groundTruth?: string;
  }): LlmSpan {
    const span = new LlmSpan({
      parent: this,
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
      statusCode: params.statusCode,
      groundTruth: params.groundTruth
    });
    this.addChild(span);
    return span;
  }

  addRetrieverSpan(params: {
    input: StepIOType;
    documents: RetrieverStepAllowedOutputType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
  }): RetrieverSpan {
    const span = new RetrieverSpan({
      parent: this,
      input: params.input,
      output: params.documents,
      name: params.name,
      durationNs: params.durationNs,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata,
      statusCode: params.statusCode
    });
    this.addChild(span);
    return span;
  }

  addToolSpan(params: {
    input: StepIOType;
    output: StepIOType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
  }): ToolSpan {
    const span = new ToolSpan({
      parent: this,
      input: params.input,
      output: params.output,
      name: params.name,
      durationNs: params.durationNs,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata,
      statusCode: params.statusCode
    });
    this.addChild(span);
    return span;
  }

  addWorkflowSpan(params: {
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
  }): WorkflowSpan {
    const span = new WorkflowSpan({
      parent: this,
      input: params.input,
      output: params.output || '',
      name: params.name,
      durationNs: params.durationNs,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata
    });
    this.addChild(span);
    return span;
  }

  conclude(params?: {
    output?: StepIOType;
    durationNs?: number;
    statusCode?: number;
  }): StepWithChildSpans | null {
    if (params?.output !== undefined) {
      this.output = params.output;
    }
    if (params?.statusCode !== undefined) {
      this.statusCode = params.statusCode;
    }
    if (params?.durationNs !== undefined) {
      this.durationNs = params.durationNs;
    }

    if (this instanceof SpanWithParentStep) {
      return (this as SpanWithParentStep).parent || null;
    }
    return null;
  }
}

export class Trace extends StepWithChildSpans {
  type: NodeType = NodeType.trace;

  constructor(data: {
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    createdAtNs?: number;
    durationNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
    groundTruth?: string;
    spans?: Span[];
  }) {
    super({ ...data, type: NodeType.trace });
  }
}

export class WorkflowSpan
  extends StepWithChildSpans
  implements StepWithChildSpans, IStepWithChildSpans
{
  type: NodeType = NodeType.workflow;
  parent?: StepWithChildSpans;

  constructor(data: {
    parent?: StepWithChildSpans;
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    createdAtNs?: number;
    durationNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
    groundTruth?: string;
    spans?: Span[];
  }) {
    super({ ...data, type: NodeType.workflow });
    this.spans = data.spans || [];
  }

  children(): BaseStep[] {
    return this.spans;
  }

  addChild(...spans: Span[]): void {
    for (const span of spans) {
      span.parent = this;
      this.spans.push(span);
    }
  }

  // Include implementations from StepWithChildSpans
  // In TypeScript, we need to duplicate these methods due to limitations with multiple inheritance
  addLlmSpan(params: {
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
    groundTruth?: string;
  }): LlmSpan {
    const span = new LlmSpan({
      parent: this,
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
      statusCode: params.statusCode,
      groundTruth: params.groundTruth
    });
    this.addChild(span);
    return span;
  }

  addRetrieverSpan(params: {
    input: StepIOType;
    documents: RetrieverStepAllowedOutputType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
  }): RetrieverSpan {
    const span = new RetrieverSpan({
      parent: this,
      input: params.input,
      output: params.documents,
      name: params.name,
      durationNs: params.durationNs,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata,
      statusCode: params.statusCode
    });
    this.addChild(span);
    return span;
  }

  addToolSpan(params: {
    input: StepIOType;
    output: StepIOType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
  }): ToolSpan {
    const span = new ToolSpan({
      parent: this,
      input: params.input,
      output: params.output,
      name: params.name,
      durationNs: params.durationNs,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata,
      statusCode: params.statusCode
    });
    this.addChild(span);
    return span;
  }

  addWorkflowSpan(params: {
    input: StepIOType;
    output?: StepIOType;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
  }): WorkflowSpan {
    const span = new WorkflowSpan({
      parent: this,
      input: params.input,
      output: params.output || '',
      name: params.name,
      durationNs: params.durationNs,
      createdAtNs: params.createdAtNs,
      metadata: params.metadata
    });
    this.addChild(span);
    return span;
  }
}

export class LlmSpan extends SpanWithParentStep implements LlmStep {
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
    parent?: StepWithChildSpans;
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

export class RetrieverSpan extends RetrieverStep {
  type: NodeType = NodeType.retriever;
  parent?: StepWithChildSpans;
  input: StepIOType;
  output: Document[] = [];

  constructor(data: {
    parent?: StepWithChildSpans;
    input: StepIOType;
    output: string[] | Record<string, string>[] | Document[];
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Record<string, string>;
    statusCode?: number;
    groundTruth?: string;
  }) {
    super({ ...data });
    this.input = data.input;
    this.output = this.setOutput(data.output);
  }
}

export class ToolSpan extends SpanWithParentStep implements ToolStep {
  type: NodeType = NodeType.tool;

  constructor(data: {
    parent?: StepWithChildSpans;
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

// Type for all span types
export type Span = WorkflowSpan | LlmSpan | RetrieverSpan | ToolSpan;
