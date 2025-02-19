enum TagType {
  GENERIC = 'generic',
  RAG = 'rag'
}

export interface RunTag {
  key: string;
  value: string;
  tag_type: TagType;
}
