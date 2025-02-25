import { GalileoApiClient } from '../api-client';
import { Traces } from '../schemas/traces/trace';
import { Trace } from '../schemas/traces/types';
import { StepIOType } from '../types/step.types';

export class GalileoLogger extends Traces {
  private projectName?: string;
  private logStreamId?: string;
  private projectId?: string;
  private client = new GalileoApiClient();

  constructor(project?: string, logStream?: string) {
    super();
    try {
      this.projectName = project || process.env.GALILEO_PROJECT || '';
      this.logStreamId = logStream || process.env.GALILEO_LOG_STREAM || '';

      if (!this.projectName || !this.logStreamId) {
        throw new Error(
          'Project and logStream are required to initialize GalileoLogger.'
        );
      }

      this.client.init(this.projectName, undefined, this.logStreamId);

      process.on('exit', () => this.terminate());
    } catch (error) {
      console.error(error);
    }
  }

  startTrace(
    input: StepIOType,
    name?: string,
    durationNs?: number,
    createdAtNs?: number,
    metadata?: Record<string, string>,
    groundTruth?: string
  ): Trace {
    return super.addTrace({
      input,
      name,
      durationNs,
      createdAtNs,
      metadata,
      groundTruth
    });
  }

  async flush(): Promise<Trace[]> {
    try {
      if (!this.traces.length) {
        console.warn('No traces to flush.');
        return [];
      }
      console.info(`Flushing ${this.traces.length} traces...`);
      const loggedTraces = [...this.traces];

      // @ts-expect-error - FIXME
      await this.client.ingestTraces(loggedTraces);

      console.info(`Successfully flushed ${loggedTraces.length} traces.`);
      this.traces = []; // Clear after uploading
      this.currentParent = null;
      return loggedTraces;
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  terminate(): void {
    try {
      this.flush();
    } catch (error) {
      console.error(error);
    }
  }
}

export default GalileoLogger;
