/* global Proxy */

import OpenAI from 'openai';
import { TracesLogger } from './traces-logger';

export function wrapOpenAI(openAIClient: OpenAI, logger: TracesLogger): OpenAI {
  const handler: ProxyHandler<OpenAI> = {
    get(target, prop: keyof OpenAI) {
      const originalMethod = target[prop];

      if (
        prop === 'chat' &&
        typeof originalMethod === 'object' &&
        originalMethod !== null
      ) {
        return new Proxy(originalMethod, {
          get(chatTarget, chatProp) {
            if (
              chatProp === 'completions' &&
              typeof chatTarget[chatProp] === 'object'
            ) {
              return new Proxy(chatTarget[chatProp], {
                get(completionsTarget, completionsProp) {
                  if (
                    completionsProp === 'create' &&
                    typeof completionsTarget[completionsProp] === 'function'
                  ) {
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    return async function wrappedCreate(...args: any[]) {
                      const [requestData] = args;
                      const trace = logger.addTrace(
                        JSON.stringify(requestData.messages)
                      );

                      const startTime = process.hrtime.bigint();
                      let response;
                      try {
                        response = await completionsTarget[completionsProp](
                          ...args
                        );
                        // eslint-disable-next-line @typescript-eslint/no-explicit-any
                      } catch (error: any) {
                        logger.conclude({
                          output: `Error: ${error.message}`,
                          durationNs: Number(
                            process.hrtime.bigint() - startTime
                          )
                        });
                        throw error;
                      }

                      const output = response.choices
                        // eslint-disable-next-line @typescript-eslint/no-explicit-any
                        .map((choice: any) => JSON.stringify(choice.message))
                        .join('\n');

                      trace.addLlmSpan({
                        input: JSON.stringify(requestData.messages),
                        output,
                        model: requestData.model || 'unknown',
                        inputTokens: response.usage?.prompt_tokens || 0,
                        outputTokens: response.usage?.completion_tokens || 0,
                        durationNs: Number(process.hrtime.bigint() - startTime),
                        metadata: requestData.metadata || {}
                      });

                      trace.conclude({
                        output,
                        durationNs: Number(process.hrtime.bigint() - startTime)
                      });

                      //logger.flush();

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
