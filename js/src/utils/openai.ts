import OpenAI from 'openai';
import { GalileoLogger } from './logger';

interface OpenAIInputData {
  name: string;
  metadata: Record<string, string>;
  input: string;
  model: string | null;
  temperature: number;
}

class OpenAIGalileo {
  private logger: GalileoLogger;
  private openai: OpenAI;

  constructor(apiKey: string, logger: GalileoLogger) {
    this.logger = logger;
    this.openai = new OpenAI({ apiKey });
  }

  private extractInputData(
    name: string,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    args: Record<string, any>
  ): OpenAIInputData {
    return {
      name,
      metadata: args.metadata || {},
      input: args.messages || args.prompt,
      model: args.model || null,
      temperature: args.temperature ?? 1
    };
  }

  async createChatCompletion(params: OpenAI.Chat.ChatCompletionCreateParams) {
    const startTime = Date.now();
    const inputData = this.extractInputData('chat-completion', params);
    const trace = this.logger.startTrace(inputData.input);

    try {
      const response = await this.openai.chat.completions.create(params);
      const duration = Date.now() - startTime;

      this.logger.addLLMSpan({
        // @ts-expect-error - TODO: Fix this
        output: response.choices,
        model: inputData.model,
        // @ts-expect-error - TODO: Fix this
        duration_ns: duration * 1e6,
        metadata: inputData.metadata
      });

      this.logger.conclude({
        trace,
        // @ts-expect-error - TODO: Fix this
        output: response.choices,
        durationNs: duration * 1e6
      });
      return response;
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }
}

export { OpenAIGalileo };
