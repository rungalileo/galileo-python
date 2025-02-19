import {
  AgentStep,
  AgentStepType,
  AWorkflow,
  LlmStep,
  LlmStepType,
  RetrieverStep,
  RetrieverStepType,
  StepIOType,
  StepWithoutChildren,
  ToolStep,
  ToolStepType,
  WorkflowStep,
  WorkflowStepType
} from './types/step.types';

export default class GalileoWorkflow {
  public projectName: string;

  constructor(projectName: string) {
    this.projectName = projectName;
  }

  public workflows: AWorkflow[] = [];
  private currentWorkflow: AWorkflow | null = null;

  private pushWorkflow(step: AWorkflow) {
    const nestedWorkflow =
      step instanceof WorkflowStep || step instanceof AgentStep;

    this.workflows.push(step);
    this.currentWorkflow = nestedWorkflow ? step : null;

    // eslint-disable-next-line no-console
    console.log('➕ New workflow added…');

    return step;
  }

  public addWorkflow(step: WorkflowStepType) {
    return this.pushWorkflow(new WorkflowStep(step));
  }

  public addAgentWorkflow(step: AgentStepType) {
    return this.pushWorkflow(new AgentStep(step));
  }

  public addSingleStepWorkflow(step: LlmStepType) {
    return this.pushWorkflow(new LlmStep(step));
  }

  private stepErrorMessage =
    '❗ No active workflows. Add a valid workflow to add a step.';

  private validWorkflow(errorMessage: string): WorkflowStep | AgentStep | null {
    if (
      this.currentWorkflow === null ||
      this.currentWorkflow instanceof StepWithoutChildren
    ) {
      throw new Error(errorMessage);
    }
    return this.currentWorkflow;
  }

  public addLlmStep(step: LlmStepType) {
    return this.validWorkflow(this.stepErrorMessage)?.addStep(
      new LlmStep(step)
    );
  }

  public addRetrieverStep(step: RetrieverStepType) {
    return this.validWorkflow(this.stepErrorMessage)?.addStep(
      new RetrieverStep(step)
    );
  }

  public addToolStep(step: ToolStepType) {
    return this.validWorkflow(this.stepErrorMessage)?.addStep(
      new ToolStep(step)
    );
  }

  public addWorkflowStep(step: WorkflowStepType) {
    step.parent = this.currentWorkflow;
    return this.validWorkflow(this.stepErrorMessage)?.addStep(
      new WorkflowStep(step)
    );
  }

  public addAgentStep(step: AgentStepType) {
    step.parent = this.currentWorkflow;
    return this.validWorkflow(this.stepErrorMessage)?.addStep(
      new AgentStep(step)
    );
  }

  public concludeWorkflow(
    output?: StepIOType,
    durationNs?: number,
    statusCode?: number
  ): AWorkflow | null {
    const errorMessage = '❗ There is no workflow to conclude.';
    this.currentWorkflow =
      this.validWorkflow(errorMessage)?.conclude(
        output,
        durationNs,
        statusCode
      ) ?? null;
    return this.currentWorkflow;
  }
}
