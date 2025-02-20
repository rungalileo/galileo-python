import { OpenAIGalileo } from '@galileo/ts-sdk'; // Import your OpenAI wrapper

async function main() {
  const openai = new OpenAIGalileo(); // Create an instance of the OpenAI wrapper

  try {
    const response = await openai.createChatCompletion({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: 'Tell me a joke!' }
      ],
      temperature: 0.7
    });

    console.log('Response from OpenAI:', response);
  } catch (error) {
    console.error('Error calling OpenAI:', error);
  }
}

main();
