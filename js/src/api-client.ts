import { decode } from "jsonwebtoken";

import axios, { AxiosRequestConfig, AxiosResponse, Method } from "axios";
import { Project, ProjectTypes } from "./types/project.types.js";
import { Routes } from "./types/routes.types";

import querystring from "querystring";
import createClient, { Client } from "openapi-fetch";
import type { components, paths } from "./types/api.types.js";

export enum RequestMethod {
  GET = "GET",
  POST = "POST",
  PUT = "PUT",
  DELETE = "DELETE",
}
import { promises as fs } from "fs";

type DatasetFormat = components["schemas"]["DatasetFormat"];
export type ListDatasetResponse = components["schemas"]["ListDatasetResponse"];
export type DatasetContent = components["schemas"]["DatasetContent"];
export type Dataset = components["schemas"]["DatasetDB"];
export type DatasetRow = components["schemas"]["DatasetRow"];

type CollectionPaths =
  | paths["/datasets"]
  | paths["/datasets/{dataset_id}/content"];
type CollectionResponse = ListDatasetResponse | DatasetContent;

export class GalileoApiClient {
  public type: ProjectTypes | undefined = undefined;
  public projectId: string = "";
  public runId: string = "";
  public datasetId: string = "";
  private apiUrl: string = "";
  private token: string = "";
  private client: Client<paths> | undefined = undefined;

  public async init(
    projectName?: string | undefined,
    datasetId?: string,
  ): Promise<void> {
    this.apiUrl = this.getApiUrl();
    if (await this.healthCheck()) {
      this.token = await this.getToken();
      this.client = createClient({
        baseUrl: this.apiUrl,
        headers: { Authorization: `Bearer ${this.token}` },
      });

      if (datasetId) {
        this.datasetId = datasetId;
      }

      if (projectName) {
        try {
          this.projectId = await this.getProjectIdByName(projectName);
          // eslint-disable-next-line no-console
          console.log(`✅ Using ${projectName}`);
        } catch (err: unknown) {
          const error = err as Error;

          if (error.message.includes("not found")) {
            const project = await this.createProject(projectName);
            this.projectId = project.id;
            // eslint-disable-next-line no-console
            console.log(`✨ ${projectName} created.`);
          } else {
            throw err;
          }
        }
      }
    }
  }

  private processResponse<T>(data: T | undefined, error: object | unknown): T {
    if (data) {
      return data;
    }

    if (error) {
      if (typeof error === "object" && "detail" in error) {
        throw new Error(`Request failed: ${JSON.stringify(error.detail)}`);
      }

      throw new Error(`Request failed: ${JSON.stringify(error)}`);
    }

    throw new Error("Request failed");
  }

  private async fetchAllPaginatedItems<
    Path extends CollectionPaths,
    Response extends CollectionResponse,
    Item,
  >(
    path: "/datasets" | "/datasets/{dataset_id}/content",
    extractItems: (response: Response) => Item[],
    params: Path["get"]["parameters"],
  ): Promise<Item[]> {
    if (!this.client) {
      throw new Error("Client not initialized");
    }

    let items: Item[] = [];
    let startingToken: number | null = 0;

    do {
      const updatedParams: Record<string, unknown> = {
        path: params.path,
        query: { ...params.query, starting_token: startingToken },
      };

      const { data, error } = await this.client.GET(path, {
        params: updatedParams,
      });

      const collection = this.processResponse(data as Response, error);
      items = items.concat(extractItems(collection));
      startingToken = collection.next_starting_token ?? null;
    } while (startingToken !== null);

    return items;
  }

  private getApiUrl(): string {
    const consoleUrl = process.env.GALILEO_CONSOLE_URL;

    if (!consoleUrl) {
      throw new Error("❗ GALILEO_CONSOLE_URL must be set");
    }

    if (consoleUrl.includes("localhost") || consoleUrl.includes("127.0.0.1")) {
      return "http://localhost:8088";
    } else {
      return consoleUrl.replace("console", "api");
    }
  }

  private async healthCheck(): Promise<boolean> {
    return await this.makeRequest<boolean>(
      RequestMethod.GET,
      Routes.healthCheck,
    );
  }

  private async getToken(): Promise<string> {
    const apiKey = process.env.GALILEO_API_KEY;

    if (apiKey) {
      const loginResponse = await this.apiKeyLogin(apiKey);
      return loginResponse.access_token || "";
    }

    const username = process.env.GALILEO_USERNAME;
    const password = process.env.GALILEO_PASSWORD;

    if (username && password) {
      const loginResponse = await this.usernameLogin(username, password);
      return loginResponse.access_token || "";
    }

    throw new Error(
      "❗ GALILEO_API_KEY or GALILEO_USERNAME and GALILEO_PASSWORD must be set",
    );
  }

  private async apiKeyLogin(
    api_key: string,
  ): Promise<{ access_token: string }> {
    return await this.makeRequest<{ access_token: string }>(
      RequestMethod.POST,
      Routes.apiKeyLogin,
      {
        api_key,
      },
    );
  }

  private async usernameLogin(username: string, password: string) {
    return await this.makeRequest<{ access_token: string }>(
      RequestMethod.POST,
      Routes.login,
      querystring.stringify({
        username,
        password,
      }),
    );
  }

  private async getProjectIdByName(project_name: string): Promise<string> {
    const projects = await this.makeRequest<Project[]>(
      RequestMethod.GET,
      Routes.projects,
      null,
      {
        project_name,
        type: this.type,
      },
    );

    if (projects.length < 1) {
      throw new Error(`Galileo project ${project_name} not found`);
    }

    return projects[0].id;
  }

  private async createProject(project_name: string): Promise<{ id: string }> {
    return await this.makeRequest<{ id: string }>(
      RequestMethod.POST,
      Routes.projects,
      {
        name: project_name,
        type: this.type,
      },
    );
  }

  public getDatasets = async (): Promise<Dataset[]> => {
    return await this.fetchAllPaginatedItems<
      paths["/datasets"],
      ListDatasetResponse,
      Dataset
    >(
      "/datasets",
      (response: ListDatasetResponse) => response.datasets ?? [],
      {},
    );
  };

  public async createDataset(
    name: string,
    filePath: string,
    format: DatasetFormat,
  ): Promise<Dataset> {
    if (!this.client) {
      throw new Error("Client not initialized");
    }

    const fileBuffer: Buffer = await fs.readFile(filePath);
    const blob: Blob = new Blob([fileBuffer]);
    const formdata = new FormData();
    formdata.append("file", blob, name);

    const { data, error } = await this.client.POST("/datasets", {
      params: { query: { format } },
      // @ts-expect-error openapi-typescript does not properly translate FormData for uploading files - https://github.com/openapi-ts/openapi-typescript/issues/1214
      body: formdata,
      bodySerializer: (body) => {
        // define a custom serializer to prevent openapi-fetch from serializing the FormData object as JSON
        return body;
      },
    });

    const dataset = this.processResponse(data, error) as Dataset;
    // eslint-disable-next-line no-console
    console.log(
      `✅  Dataset '${dataset.name}' with ${dataset.num_rows} rows uploaded.`,
    );
    return dataset;
  }

  public async getDatasetContent(datasetId: string): Promise<DatasetRow[]> {
    if (!this.client) {
      throw new Error("Client not initialized");
    }

    return await this.fetchAllPaginatedItems<
      paths["/datasets/{dataset_id}/content"],
      DatasetContent,
      DatasetRow
    >(
      `/datasets/{dataset_id}/content`,
      (response: DatasetContent) => response.rows ?? [],
      { path: { dataset_id: datasetId } },
    );
  }

  private getAuthHeader(token: string): { Authorization: string } {
    return { Authorization: `Bearer ${token}` };
  }

  private validateResponse(response: AxiosResponse): void {
    if (response.status >= 300) {
      const msg = `❗ Something didn't go quite right. The API returned a non-ok status code ${response.status} with output: ${response.data}`;
      // TODO: Better error handling
      throw new Error(msg);
    }
  }

  public async makeRequest<T>(
    request_method: Method,
    endpoint: Routes,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    data?: string | Record<string, any> | null,
    params?: Record<string, unknown>,
  ): Promise<T> {
    // Check to see if our token is expired before making a request
    // and refresh token if it's expired
    if (![Routes.login, Routes.apiKeyLogin].includes(endpoint) && this.token) {
      const payload = decode(this.token, { json: true });
      if (payload?.exp && payload.exp < Math.floor(Date.now() / 1000)) {
        this.token = await this.getToken();
      }
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    let headers: Record<string, any> = {};

    if (this.token) {
      headers = this.getAuthHeader(this.token);
    }

    const config: AxiosRequestConfig = {
      method: request_method,
      url: `${this.apiUrl}/${endpoint
        .replace("{project_id}", this.projectId)
        .replace("{run_id}", this.runId)}`,
      params,
      headers,
      data,
    };

    const response = await axios.request<T>(config);

    this.validateResponse(response);

    return response.data;
  }
}
