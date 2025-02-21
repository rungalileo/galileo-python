/* global Proxy */

import OpenAI from 'openai';
import { GalileoLogger } from './logger';

export function wrapOpenAI(
  openAIClient: OpenAI,
  logger: GalileoLogger
): OpenAI {
  const handler: ProxyHandler<OpenAI> = {
    get(target, prop: keyof OpenAI) {
      const originalMethod = target[prop];

      if (typeof originalMethod === 'function' && prop === 'chat') {
        return new Proxy(originalMethod, {
          get(chatTarget, chatProp) {
            if (chatProp === 'completions') {
              return new Proxy(chatTarget[chatProp], {
                get(completionsTarget, completionsProp) {
                  if (completionsProp === 'create') {
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    return async function wrappedCreate(...args: any[]) {
                      const [requestData] = args;

                      // Start tracing
                      const trace = logger.startTrace(
                        JSON.stringify(requestData.messages)
                      );

                      const startTime = process.hrtime.bigint();
                      let response;
                      try {
                        response = await completionsTarget[completionsProp](
                          ...args
                        );
                      } catch (error) {
                        console.log('🚀 ~ wrappedCreate ~ error:', error);
                        logger.conclude({
                          trace,
                          // @ts-expect-error - Fixme
                          output: `Error: ${error.message}`,
                          durationNs: Number(
                            process.hrtime.bigint() - startTime
                          )
                        });
                        throw error;
                      }

                      // Extract OpenAI response data
                      const output = response.choices
                        // eslint-disable-next-line @typescript-eslint/no-explicit-any
                        .map((choice: any) => choice.message)
                        .join('\n');

                      // Log the LLM span
                      logger.addLLMSpan({
                        input: JSON.stringify(requestData.messages),
                        trace,
                        output,
                        model: requestData.model || 'unknown',
                        inputTokens: response.usage?.prompt_tokens || 0,
                        outputTokens: response.usage?.completion_tokens || 0,
                        durationNs: Number(process.hrtime.bigint() - startTime),
                        metadata: requestData.metadata || {}
                      });

                      // Conclude the trace
                      logger.conclude({
                        trace,
                        output,
                        durationNs: Number(process.hrtime.bigint() - startTime)
                      });

                      return response;
                    };
                  }
                  return completionsTarget[completionsProp];
                }
              });
            }
            return chatTarget[chatProp];
          }
        });
      }

      return originalMethod;
    }
  };

  return new Proxy(openAIClient, handler);
}
