import os
import json
from typing import Optional, Dict
from pathlib import Path

from ..resources.models.body_upload_file_projects_project_id_upload_file_post import BodyUploadFileProjectsProjectIdUploadFilePost
from ..resources.api.projects.upload_file_projects_project_id_upload_file_post import sync
from ..resources.client import AuthenticatedClient
from ..resources.types import File
from ..api_client import GalileoApiClient


def upload_audio_file(file_path: str, metadata: Optional[Dict[str, str]] = None) -> str:
    """
    Upload an audio file to Galileo and return the file ID.
    
    Args:
        file_path: Path to the audio file to upload
        metadata: Optional metadata to associate with the file
        
    Returns:
        str: The ID of the uploaded audio file
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not a valid audio file or other upload issues
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found at {file_path}")
    
    # Check if file is a wav file by extension
    if not file_path.lower().endswith(".wav"):
        raise ValueError(f"File {file_path} is not a .wav audio file")
    
    # Get the project ID from the client
    api_client = GalileoApiClient()
    client = api_client.client
    project_id = api_client.get_project_id()
    
    # Prepare metadata
    upload_metadata = {
        "file_type": "audio",
        "content_type": "audio/wav"
    }
    
    # Add any additional metadata
    if metadata:
        upload_metadata.update(metadata)
    
    # Convert to JSON string
    upload_metadata_str = json.dumps(upload_metadata)
    
    # Open file and create upload body
    with open(file_path, "rb") as f:
        file_content = f.read()
        
    file = File(
        payload=file_content,
        file_name=Path(file_path).name,
        mime_type="audio/wav"
    )
    
    body = BodyUploadFileProjectsProjectIdUploadFilePost(
        file=file,
        upload_metadata=upload_metadata_str
    )
    
    # Upload the file
    response = sync(project_id=project_id, client=client, body=body)
    
    if not response or not isinstance(response, dict) or "id" not in response:
        raise ValueError(f"Failed to upload audio file {file_path}. Response: {response}")
    
    return response["id"]