import { components } from "./api.types";

export type TransactionRecordBatch =
  components["schemas"]["TransactionRecordBatch"];

export enum TransactionLoggingMethod {
  js_langchain = "js_langchain",
  js_logger = "js_logger",
}

export type TransactionRecord =
  components["schemas"]["TransactionRecordIngest"];
