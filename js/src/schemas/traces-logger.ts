/* eslint-disable @typescript-eslint/no-explicit-any */
import { Document } from './document';
import { Message } from './message';

interface Metrics {
  durationNs?: number;
}

interface LlmMetrics extends Metrics {
  numInputTokens?: number;
  numOutputTokens?: number;
  numTotalTokens?: number;
  timeToFirstTokenNs?: number;
}

abstract class Span {
  name?: string;
  createdAt?: number;
  userMetadata?: Record<string, string>;
  tags?: string[];
  input: any;
  output?: any;
  metrics: Metrics;
  statusCode?: number;

  constructor(
    input: any,
    output?: any,
    name?: string,
    createdAt?: number,
    userMetadata?: Record<string, string>,
    tags?: string[],
    statusCode?: number,
    metrics?: Metrics
  ) {
    this.input = input;
    this.output = output;
    this.name = name;
    this.createdAt = createdAt;
    this.userMetadata = userMetadata;
    this.tags = tags;
    this.statusCode = statusCode;
    this.metrics = metrics || { durationNs: undefined };
  }
}

abstract class StepWithChildSpans extends Span {
  childSpans: Span[] = [];

  addChildSpan(span: Span): void {
    this.childSpans.push(span);
  }
}

class Trace extends StepWithChildSpans {}

class LlmSpan extends Span {
  tools?: any[];
  model?: string;
  temperature?: number;

  constructor(
    input: Message[],
    output: Message,
    model?: string,
    tools?: any[],
    name?: string,
    createdAt?: number,
    userMetadata?: Record<string, string>,
    tags?: string[],
    metrics?: LlmMetrics,
    temperature?: number,
    statusCode?: number
  ) {
    super(
      input,
      output,
      name,
      createdAt,
      userMetadata,
      tags,
      statusCode,
      metrics
    );
    this.tools = tools;
    this.model = model;
    this.temperature = temperature;
  }
}

class RetrieverSpan extends Span {
  constructor(
    input: string,
    output: Document[],
    name?: string,
    createdAt?: number,
    userMetadata?: Record<string, string>,
    tags?: string[],
    statusCode?: number,
    metrics?: Metrics
  ) {
    super(
      input,
      output,
      name,
      createdAt,
      userMetadata,
      tags,
      statusCode,
      metrics
    );
  }
}

class ToolSpan extends Span {
  toolCallId?: string;

  constructor(
    input: string,
    output?: string,
    name?: string,
    createdAt?: number,
    userMetadata?: Record<string, string>,
    tags?: string[],
    statusCode?: number,
    toolCallId?: string,
    metrics?: Metrics
  ) {
    super(
      input,
      output,
      name,
      createdAt,
      userMetadata,
      tags,
      statusCode,
      metrics
    );
    this.toolCallId = toolCallId;
  }
}

class WorkflowSpan extends StepWithChildSpans {}

class TracesLogger {
  traces: Trace[] = [];
  private parentStack: StepWithChildSpans[] = [];

  currentParent(): StepWithChildSpans | undefined {
    return this.parentStack.length > 0
      ? this.parentStack[this.parentStack.length - 1]
      : undefined;
  }

  addChildSpanToParent(span: Span): void {
    const currentParent = this.currentParent();
    if (currentParent === undefined) {
      throw new Error('A trace needs to be created in order to add a span.');
    }
    currentParent.addChildSpan(span);
  }

  addTrace(
    input: string,
    output?: string,
    name?: string,
    createdAt?: number,
    durationNs?: number,
    userMetadata?: Record<string, string>,
    tags?: string[]
  ): Trace {
    /**
     * Create a new trace and add it to the list of traces.
     * Simple usage:
     * ```
     * myTraces.addTrace("input");
     * myTraces.addLlmSpan("input", "output", model: "<my_model>");
     * myTraces.conclude("output");
     * ```
     */
    if (this.currentParent() !== undefined) {
      throw new Error(
        'You must conclude the existing trace before adding a new one.'
      );
    }

    const trace = new Trace(
      input,
      output,
      name,
      createdAt,
      userMetadata,
      tags,
      undefined,
      { durationNs }
    );

    this.traces.push(trace);
    this.parentStack.push(trace);
    return trace;
  }

  addSingleLlmSpanTrace(
    input: Message[],
    output: Message,
    model?: string,
    tools?: any[],
    name?: string,
    createdAt?: number,
    durationNs?: number,
    userMetadata?: Record<string, string>,
    tags?: string[],
    numInputTokens?: number,
    numOutputTokens?: number,
    totalTokens?: number,
    temperature?: number,
    statusCode?: number,
    timeToFirstTokenNs?: number
  ): Trace {
    /**
     * Create a new trace with a single span and add it to the list of traces.
     */
    if (this.currentParent() !== undefined) {
      throw new Error(
        'A trace cannot be created within a parent trace or span, it must always be the root.'
      );
    }

    const trace = new Trace(
      JSON.stringify(input),
      JSON.stringify(output),
      name,
      createdAt,
      userMetadata,
      tags
    );

    trace.addChildSpan(
      new LlmSpan(
        input,
        output,
        model,
        tools,
        name,
        createdAt,
        userMetadata,
        tags,
        {
          durationNs,
          numInputTokens,
          numOutputTokens,
          numTotalTokens: totalTokens,
          timeToFirstTokenNs
        },
        temperature,
        statusCode
      )
    );

    this.traces.push(trace);
    // Single span traces are automatically concluded so we reset the current parent.
    this.parentStack = [];
    return trace;
  }

  addLlmSpan(
    input: Message[],
    output: Message,
    model?: string,
    tools?: any[],
    name?: string,
    createdAt?: number,
    durationNs?: number,
    userMetadata?: Record<string, string>,
    tags?: string[],
    numInputTokens?: number,
    numOutputTokens?: number,
    totalTokens?: number,
    temperature?: number,
    statusCode?: number,
    timeToFirstTokenNs?: number
  ): LlmSpan {
    /**
     * Add a new llm span to the current parent.
     */
    const span = new LlmSpan(
      input,
      output,
      model,
      tools,
      name,
      createdAt,
      userMetadata,
      tags,
      {
        durationNs,
        numInputTokens,
        numOutputTokens,
        numTotalTokens: totalTokens,
        timeToFirstTokenNs
      },
      temperature,
      statusCode
    );

    this.addChildSpanToParent(span);
    return span;
  }

  addRetrieverSpan(
    input: string,
    documents: Document[],
    name?: string,
    durationNs?: number,
    createdAt?: number,
    userMetadata?: Record<string, string>,
    tags?: string[],
    statusCode?: number
  ): RetrieverSpan {
    /**
     * Add a new retriever span to the current parent.
     */
    const span = new RetrieverSpan(
      input,
      documents,
      name,
      createdAt,
      userMetadata,
      tags,
      statusCode,
      { durationNs }
    );

    this.addChildSpanToParent(span);
    return span;
  }

  addToolSpan(
    input: string,
    output?: string,
    name?: string,
    durationNs?: number,
    createdAt?: number,
    userMetadata?: Record<string, string>,
    tags?: string[],
    statusCode?: number,
    toolCallId?: string
  ): ToolSpan {
    /**
     * Add a new tool span to the current parent.
     */
    const span = new ToolSpan(
      input,
      output,
      name,
      createdAt,
      userMetadata,
      tags,
      statusCode,
      toolCallId,
      { durationNs }
    );

    this.addChildSpanToParent(span);
    return span;
  }

  addWorkflowSpan(
    input: string,
    output?: string,
    name?: string,
    durationNs?: number,
    createdAt?: number,
    userMetadata?: Record<string, string>,
    tags?: string[]
  ): WorkflowSpan {
    /**
     * Add a workflow span to the current parent. This is useful when you want to create a nested workflow span
     * within the trace or current workflow span. The next span you add will be a child of the current parent. To
     * move out of the nested workflow, use conclude().
     */
    const span = new WorkflowSpan(
      input,
      output,
      name,
      createdAt,
      userMetadata,
      tags,
      undefined,
      { durationNs }
    );

    this.addChildSpanToParent(span);
    this.parentStack.push(span);
    return span;
  }

  conclude(
    output?: string,
    durationNs?: number,
    statusCode?: number
  ): StepWithChildSpans | undefined {
    /**
     * Conclude the current trace or workflow span by setting the output of the current node. In the case of nested
     * workflow spans, this will point the workflow back to the parent of the current workflow span.
     */
    const currentParent = this.currentParent();
    if (currentParent === undefined) {
      throw new Error('No existing workflow to conclude.');
    }

    currentParent.output = output || currentParent.output;
    currentParent.statusCode = statusCode;
    if (durationNs !== undefined) {
      currentParent.metrics.durationNs = durationNs;
    }

    const finishedStep = this.parentStack.pop();
    if (
      this.currentParent() === undefined &&
      !(finishedStep instanceof Trace)
    ) {
      throw new Error(
        'Finished step is not a trace, but has no parent. Not added to the list of traces.'
      );
    }
    return this.currentParent();
  }
}

export {
  TracesLogger,
  Trace,
  Span,
  StepWithChildSpans,
  LlmSpan,
  RetrieverSpan,
  ToolSpan,
  WorkflowSpan,
  Metrics,
  LlmMetrics
};
