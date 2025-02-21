import 'dotenv/config';
import { GalileoLogger, wrapOpenAI } from '@galileo/ts-sdk'; // Import your OpenAI wrapper
import OpenAI from 'openai';

// Initialize the logger and OpenAI client

const logger = new GalileoLogger(
  process.env.GALILEO_PROJECT,
  process.env.GALILEO_LOG_STREAM
);
const client = wrapOpenAI(
  new OpenAI({ apiKey: process.env.OPENAI_API_KEY }),
  logger
);

async function test() {
  const response = await client.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: 'Tell me a joke' }]
  });

  console.log(response);
}

test();
