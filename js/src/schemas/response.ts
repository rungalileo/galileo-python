import { v4 as uuid4 } from 'uuid';

// Helper function to get current time in nanoseconds
function time_ns(): number {
  // JavaScript's Date.now() returns milliseconds, so we multiply by 1,000,000 to get nanoseconds
  return Date.now() * 1_000_000;
}

interface BaseTraceMetadataProps {
  id?: string; // Using string for UUID
  received_at?: number;
}

class BaseTraceMetadata {
  id: string;
  received_at: number;

  constructor(props: BaseTraceMetadataProps = {}) {
    this.id = props.id || uuid4();
    this.received_at = props.received_at || time_ns();
  }
}

interface TraceMetadataProps extends BaseTraceMetadataProps {
  response_at?: number;
  execution_time?: number;
}

class TraceMetadata extends BaseTraceMetadata {
  response_at: number;
  execution_time: number;

  constructor(props: TraceMetadataProps = {}) {
    super(props);

    this.response_at = props.response_at || time_ns();

    // Handle execution_time calculation
    this.execution_time = this.setExecutionTime(props.execution_time);
  }

  private setExecutionTime(value?: number): number {
    // If execution_time is not provided or is negative/zero, calculate it
    if (!value || value <= 0) {
      // Convert nanoseconds to seconds with 1e-9
      return (this.response_at - this.received_at) * 1e-9;
    }
    return value;
  }

  // Static factory method
  static create(data: TraceMetadataProps = {}): TraceMetadata {
    return new TraceMetadata(data);
  }
}
enum ExecutionStatus {
  triggered = 'triggered',
  failed = 'failed',
  error = 'error',
  timeout = 'timeout',
  paused = 'paused',
  not_triggered = 'not_triggered'
}

interface ResponseProps {
  text: string;
  status?: ExecutionStatus;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [key: string]: any; // For the "extra='allow'" equivalent
}

export class Response {
  status: ExecutionStatus;
  trace_metadata: TraceMetadata;
  text: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  model_config: Record<string, any>; // For the "extra='allow'" equivalent
  constructor(props: ResponseProps) {
    this.text = props.text;
    this.model_config = props.model_config;
    this.status = props.status || ExecutionStatus.not_triggered;
    this.trace_metadata = TraceMetadata.create(props.trace_metadata);
  }

  // Static factory method similar to Pydantic model creation
  static create(data: ResponseProps): Response {
    return new Response(data);
  }
}
