export enum Routes {
  healthCheck = 'healthcheck',
  login = 'login',
  apiKeyLogin = 'login/api_key',
  getToken = 'get-token',
  projects = 'projects',
  runs = 'projects/{project_id}/runs',
  observeMetrics = 'projects/{project_id}/observe/metrics',
  observeIngest = 'projects/{project_id}/observe/ingest',
  observeRows = 'projects/{project_id}/observe/rows',
  observeDelete = 'projects/{project_id}/observe/delete',
  evaluateIngest = 'projects/{project_id}/runs/{run_id}/chains/ingest',
  datasets = 'datasets',
  traces = '/v2/projects/{project_id}/traces'
}
