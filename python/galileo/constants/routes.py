from enum import Enum


class Routes(str, Enum):
    healthcheck = "healthcheck"
    login = "login"
    api_key_login = "login/api_key"
    get_token = "get-token"

    projects = "projects"
    all_projects = "projects/all"

    log_streams = "/projects/{project_id}/log_streams"

    traces = "/projects/{project_id}/traces"
    traces_search = "/projects/{project_id}/traces/search"
    traces_available_columns = "/projects/{project_id}/traces/available_columns"
    trace = "/projects/{project_id}/traces/{trace_id}"
    spans = "/projects/{project_id}/spans"
    spans_search = "/projects/{project_id}/spans/search"
    spans_available_columns = "/projects/{project_id}/spans/available_columns"
    span = "/projects/{project_id}/spans/{span_id}"
