interface PayloadProps {
  input?: string;
  output?: string;
}

export class Payload {
  input?: string;
  output?: string;

  constructor(props: PayloadProps) {
    this.input = props.input;
    this.output = props.output;

    this.ensureInputOrOutput();
  }

  private ensureInputOrOutput(): void {
    if (!this.input && !this.output) {
      throw new Error('Either input or output must be set.');
    }
  }

  // Replicating cached_property behavior with a getter
  get text(): string {
    if (this.output) {
      return this.output;
    } else if (this.input) {
      return this.input;
    } else {
      throw new Error('Either input or output must be set.');
    }
  }

  // Static factory method similar to Pydantic model validation
  static validate(data: PayloadProps): Payload {
    return new Payload(data);
  }
}
