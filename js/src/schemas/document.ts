type ChunkMetaDataValueType = boolean | string | number;

export class Document {
  content: string;
  metadata: Record<string, ChunkMetaDataValueType>;

  constructor(data: {
    content: string;
    metadata?: Record<string, ChunkMetaDataValueType>;
  }) {
    this.content = data.content;
    this.metadata = this.filterMetadata(data.metadata || {});
  }

  private filterMetadata(
    metadata: Record<string, ChunkMetaDataValueType>
  ): Record<string, ChunkMetaDataValueType> {
    return Object.fromEntries(
      Object.entries(metadata).filter(([, value]) =>
        ['boolean', 'string', 'number'].includes(typeof value)
      )
    );
  }
}
