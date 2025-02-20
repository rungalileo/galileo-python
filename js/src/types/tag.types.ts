import { components } from './api.types';

export enum TagType {
  GENERIC = 'generic',
  RAG = 'rag'
}

export type RunTag = components['schemas']['RunTagCreateRequest'];
