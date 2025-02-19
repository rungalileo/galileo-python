enum MessageRole {
  agent = 'agent',
  assistant = 'assistant',
  function = 'function',
  system = 'system',
  tool = 'tool',
  user = 'user'
}

export interface Message {
  content: string;
  role: MessageRole;
}
