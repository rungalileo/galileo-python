export enum ProjectTypes {
  evaluate = 'prompt_evaluation',
  observe = 'llm_monitor'
}

export interface Project {
  id: string;
  name: string;
  type: ProjectTypes;
}
