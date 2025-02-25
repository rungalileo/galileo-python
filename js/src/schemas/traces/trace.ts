import {
  LlmSpan,
  RetrieverSpan,
  StepWithChildSpans,
  ToolSpan,
  Trace,
  WorkflowSpan
} from './types';

import { LlmStepAllowedIOType, RetrieverStepAllowedOutputType } from '../step';
import { StepIOType } from '../../types/step.types';

type Dict<K extends string | number | symbol, V> = Record<K, V>;
type List<T> = Array<T>;

export class Traces {
  /** List of traces. */
  traces: List<Trace> = [];

  /** Current parent context. */
  currentParent: StepWithChildSpans | null = null;

  /**
   * Create a new trace and add it to the list of traces.
   * Simple usage:
   * ```
   * myTraces.addTrace("input")
   * myTraces.addLlmSpan("input", "output", model="<my_model>")
   * myTraces.conclude("output")
   * ```
   * @param input Input to the node.
   * @param output Output of the node.
   * @param name Name of the trace.
   * @param durationNs Duration of the trace in nanoseconds.
   * @param createdAtNs Timestamp of the trace's creation.
   * @param metadata Metadata associated with this trace.
   * @param groundTruth Ground truth, expected output of the trace.
   * @returns The created trace.
   */
  addTrace(
    input: StepIOType,
    output?: StepIOType,
    name?: string,
    durationNs?: number,
    createdAtNs?: number,
    metadata?: Dict<string, string>,
    groundTruth?: string
  ): Trace {
    const trace = new Trace({
      input,
      output: output || '',
      name,
      durationNs,
      createdAtNs,
      metadata,
      groundTruth
    });
    this.traces.push(trace);
    this.currentParent = trace;
    return trace;
  }

  /**
   * Create a new trace with a single span and add it to the list of traces.
   * @param input Input to the node.
   * @param output Output of the node.
   * @param model Model used for this span.
   * @param tools List of available tools passed to LLM on invocation.
   * @param name Name of the span.
   * @param durationNs Duration of the node in nanoseconds.
   * @param createdAtNs Timestamp of the span's creation.
   * @param metadata Metadata associated with this span.
   * @param inputTokens Number of input tokens.
   * @param outputTokens Number of output tokens.
   * @param totalTokens Total number of tokens.
   * @param temperature Temperature used for generation.
   * @param groundTruth Ground truth, expected output of the workflow.
   * @param statusCode Status code of the node execution.
   * @returns The created trace.
   */
  addSingleSpanTrace(
    input: LlmStepAllowedIOType,
    output: LlmStepAllowedIOType,
    model: string,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    tools?: List<Dict<string, any>>,
    name?: string,
    durationNs?: number,
    createdAtNs?: number,
    metadata?: Dict<string, string>,
    inputTokens?: number,
    outputTokens?: number,
    totalTokens?: number,
    temperature?: number,
    groundTruth?: string,
    statusCode?: number
  ): Trace {
    const trace = new Trace({
      input,
      output
    });
    trace.addLlmSpan({
      input,
      output,
      model,
      tools,
      name,
      durationNs,
      createdAtNs,
      metadata,
      inputTokens,
      outputTokens,
      totalTokens,
      temperature,
      statusCode,
      groundTruth
    });
    this.traces.push(trace);
    // Single span traces are automatically concluded so we reset the current parent.
    this.currentParent = null;
    return trace;
  }

  /**
   * Add a new llm span to the current parent.
   * @param input Input to the node.
   * @param output Output of the node.
   * @param model Model used for this span.
   * @param tools List of available tools passed to LLM on invocation.
   * @param name Name of the span.
   * @param durationNs Duration of the node in nanoseconds.
   * @param createdAtNs Timestamp of the span's creation.
   * @param metadata Metadata associated with this span.
   * @param inputTokens Number of input tokens.
   * @param outputTokens Number of output tokens.
   * @param totalTokens Total number of tokens.
   * @param temperature Temperature used for generation.
   * @param statusCode Status code of the node execution.
   * @returns The created span.
   */
  addLlmSpan({
    input,
    output,
    model,
    tools,
    name,
    durationNs,
    createdAtNs,
    metadata,
    inputTokens,
    outputTokens,
    totalTokens,
    temperature,
    statusCode
  }: {
    input: LlmStepAllowedIOType;
    output: LlmStepAllowedIOType;
    model: string;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    tools?: List<Dict<string, any>>;
    name?: string;
    durationNs?: number;
    createdAtNs?: number;
    metadata?: Dict<string, string>;
    inputTokens?: number;
    outputTokens?: number;
    totalTokens?: number;
    temperature?: number;
    statusCode?: number;
  }): LlmSpan {
    if (this.currentParent === null) {
      throw new Error('A trace needs to be created in order to add a span.');
    }
    const span = this.currentParent.addLlmSpan({
      input,
      output,
      model,
      tools,
      name,
      durationNs,
      createdAtNs,
      metadata,
      inputTokens,
      outputTokens,
      totalTokens,
      temperature,
      statusCode
    });
    return span;
  }

  /**
   * Add a new retriever span to the current parent.
   * @param input Input to the node.
   * @param documents Documents retrieved from the retriever.
   * @param name Name of the span.
   * @param durationNs Duration of the node in nanoseconds.
   * @param createdAtNs Timestamp of the span's creation.
   * @param metadata Metadata associated with this span.
   * @param statusCode Status code of the node execution.
   * @returns The created span.
   */
  addRetrieverSpan(
    input: StepIOType,
    documents: RetrieverStepAllowedOutputType,
    name?: string,
    durationNs?: number,
    createdAtNs?: number,
    metadata?: Dict<string, string>,
    statusCode?: number
  ): RetrieverSpan {
    if (this.currentParent === null) {
      throw new Error('A trace needs to be created in order to add a span.');
    }
    const span = this.currentParent.addRetrieverSpan({
      input,
      documents,
      name,
      durationNs,
      createdAtNs,
      metadata,
      statusCode
    });
    return span;
  }

  /**
   * Add a new tool span to the current parent.
   * @param input Input to the node.
   * @param output Output of the node.
   * @param name Name of the span.
   * @param durationNs Duration of the node in nanoseconds.
   * @param createdAtNs Timestamp of the span's creation.
   * @param metadata Metadata associated with this span.
   * @param statusCode Status code of the node execution.
   * @returns The created span.
   */
  addToolSpan(
    input: StepIOType,
    output: StepIOType,
    name?: string,
    durationNs?: number,
    createdAtNs?: number,
    metadata?: Dict<string, string>,
    statusCode?: number
  ): ToolSpan {
    if (this.currentParent === null) {
      throw new Error('A trace needs to be created in order to add a span.');
    }
    const span = this.currentParent.addToolSpan({
      input,
      output,
      name,
      durationNs,
      createdAtNs,
      metadata,
      statusCode
    });
    return span;
  }

  /**
   * Add a workflow span to the current parent. This is useful when you want to create a nested workflow span
   * within the trace or current workflow span. The next span you add will be a child of the current parent. To
   * move out of the nested workflow, use conclude().
   * @param input Input to the node.
   * @param output Output of the node. This can also be set on conclude().
   * @param name Name of the span.
   * @param durationNs Duration of the node in nanoseconds.
   * @param createdAtNs Timestamp of the span's creation.
   * @param metadata Metadata associated with this span.
   * @returns The created span.
   */
  addWorkflowSpan(
    input: StepIOType,
    output?: StepIOType,
    name?: string,
    durationNs?: number,
    createdAtNs?: number,
    metadata?: Dict<string, string>
  ): WorkflowSpan {
    if (this.currentParent === null) {
      throw new Error('A trace needs to be created in order to add a span.');
    }
    const span = this.currentParent.addWorkflowSpan({
      input,
      output,
      name,
      durationNs,
      createdAtNs,
      metadata
    });
    this.currentParent = span;
    return span;
  }

  /**
   * Conclude the current trace or workflow span by setting the output of the current node. In the case of nested
   * workflow spans, this will point the workflow back to the parent of the current workflow span.
   * @param output Output of the node.
   * @param durationNs Duration of the node in nanoseconds.
   * @param statusCode Status code of the node execution.
   * @returns The parent of the current workflow. None if no parent exists.
   */
  conclude(
    output?: StepIOType,
    durationNs?: number,
    statusCode?: number
  ): StepWithChildSpans | null {
    if (this.currentParent === null) {
      throw new Error('No existing workflow to conclude.');
    }
    this.currentParent = this.currentParent.conclude({
      output,
      durationNs,
      statusCode
    });
    return this.currentParent;
  }
}
