import { GalileoApiClient } from '../api-client';
import { components } from '../types/api.types';

interface Trace {
  id: number;
  input: string;
  output?: string;
  model?: string | null;
  inputTokens?: number;
  outputTokens?: number;
  totalTokens?: number;
  durationNs?: number;
  metadata?: Record<string, string>;
  spans: components['schemas']['LlmSpan'][];
}

interface AddLLMSpanArgs {
  input: string;
  trace: Trace;
  output: string;
  model: string | null;
  inputTokens: number;
  outputTokens: number;
  durationNs: number;
  metadata?: Record<string, string>;
}

export class GalileoLogger {
  private project: string;
  private logStreamId: string;
  private traces: Trace[] = [];
  private apiClient = new GalileoApiClient();

  constructor(project?: string, logStream?: string) {
    this.project = project || process.env.GALILEO_PROJECT || '';
    this.logStreamId = logStream || process.env.GALILEO_LOG_STREAM || '';

    if (!this.project || !this.logStreamId) {
      throw new Error('Project and logStream are required.');
    }

    // Ensure logs are flushed on process exit
    process.on('exit', () => this.terminate());
    process.on('SIGINT', () => {
      this.terminate();
      process.exit();
    });
  }

  startTrace(input: string): Trace {
    const trace: Trace = { input, spans: [], id: this.traces.length };
    this.traces.push(trace);
    return trace;
  }

  addLLMSpan({
    input,
    trace,
    output,
    model,
    inputTokens,
    outputTokens,
    durationNs,
    metadata
  }: AddLLMSpanArgs) {
    this.traces = this.traces.map((tr) => {
      if (tr.id === trace.id) {
        return {
          ...trace,
          spans: [
            ...trace.spans,
            {
              output,
              input,
              model,
              input_tokens: inputTokens,
              output_tokens: outputTokens,
              total_tokens: inputTokens + outputTokens,
              duration_ns: durationNs,
              type: 'llm',
              metadata
            }
          ]
        };
      }
      return trace;
    });
  }

  conclude({
    trace,
    output,
    durationNs
  }: {
    trace: Trace;
    output: string;
    durationNs: number;
  }) {
    trace.output = output;
    trace.durationNs = durationNs;
  }

  async flush(): Promise<void> {
    if (this.traces.length === 0) {
      console.warn('No traces to flush.');
      return;
    }

    try {
      await this.apiClient.init(this.project, undefined, this.logStreamId);
      await this.apiClient.ingestTraces(this.traces);
      console.log('Traces uploaded successfully.');
      this.traces = []; // Clear after upload
    } catch (error) {
      console.error('Error uploading traces:', error);
    }
  }

  terminate() {
    this.flush();
  }
}
