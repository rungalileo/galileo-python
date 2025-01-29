from enum import Enum


class Routes(str, Enum):
    healthcheck = "healthcheck"
    login = "login"
    api_key_login = "login/api_key"
    get_token = "get-token"

    projects = "projects"
    all_projects = "projects/all"

    log_streams = "/v2/projects/{project_id}/log_streams"

    traces = "/v2/projects/{project_id}/traces"
    traces_search = "/v2/projects/{project_id}/traces/search"
    traces_available_columns = "/v2/projects/{project_id}/traces/available_columns"
    trace = "/v2/projects/{project_id}/traces/{trace_id}"
    spans = "/v2/projects/{project_id}/spans"
    spans_search = "/v2/projects/{project_id}/spans/search"
    spans_available_columns = "/v2/projects/{project_id}/spans/available_columns"
    span = "/v2/projects/{project_id}/spans/{span_id}"
