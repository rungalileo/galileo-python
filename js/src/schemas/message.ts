export enum MessageRole {
  Agent = 'agent',
  Assistant = 'assistant',
  Function = 'function',
  System = 'system',
  Tool = 'tool',
  User = 'user'
}

export class Message {
  content: string;
  role: MessageRole;

  constructor(data: { content: string; role: MessageRole }) {
    this.content = data.content;
    this.role = data.role;
  }

  get message(): string {
    return `${this.role}: ${this.content}`;
  }
}
