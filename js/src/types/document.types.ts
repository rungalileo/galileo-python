type ChunkMetaDataValueType = boolean | string | number;

interface DocumentMetadata {
  [key: string]: ChunkMetaDataValueType;
}

export interface Document {
  content: string;
  metadata: DocumentMetadata;
}
