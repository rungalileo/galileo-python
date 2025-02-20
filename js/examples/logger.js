import 'dotenv/config';

import { GalileoLogger } from '@galileo/ts-sdk'; // Import your OpenAI wrapper

const logger = new GalileoLogger(
  process.env.GALILEO_PROJECT,
  process.env.GALILEO_LOG_STREAM
);

// Start a trace
const trace = logger.startTrace('Hello, AI!');

// Add an LLM span
logger.addLLMSpan({
  trace: trace,
  output: 'Hi there!',
  model: 'gpt4o',
  inputTokens: 10,
  outputTokens: 5,
  durationNs: 1500
});

// Conclude the trace
logger.conclude({ trace, output: 'Hi there!', durationNs: 1500 });

// Flush the logs
logger.flush();
