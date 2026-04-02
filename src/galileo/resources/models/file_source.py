from enum import Enum


class FileSource(str, Enum):
    ASSEMBLED_STREAM = "assembled_stream"
    DIRECT_UPLOAD = "direct_upload"
    EXTERNAL_FILES_API = "external_files_api"
    EXTERNAL_URL = "external_url"

    def __str__(self) -> str:
        return str(self.value)
