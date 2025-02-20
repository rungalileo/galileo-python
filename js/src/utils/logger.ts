import { GalileoApiClient } from '../api-client';

interface Trace {
  input: string;
  output?: string;
  model?: string | null;
  inputTokens?: number;
  outputTokens?: number;
  totalTokens?: number;
  durationNs?: number;
  metadata?: Record<string, string>;
}

interface AddLLMSpanArgs {
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
    const trace: Trace = { input };
    this.traces.push(trace);
    return trace;
  }

  addLLMSpan({
    trace,
    output,
    model,
    inputTokens,
    outputTokens,
    durationNs,
    metadata
  }: AddLLMSpanArgs) {
    trace.output = output;
    trace.model = model;
    trace.inputTokens = inputTokens;
    trace.outputTokens = outputTokens;
    trace.totalTokens = inputTokens + outputTokens;
    trace.durationNs = durationNs;
    trace.metadata = metadata;
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
