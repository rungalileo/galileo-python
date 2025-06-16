# Audio File Support in Galileo SDK

This document demonstrates how to use the audio file support in the Galileo SDK.

## Basic Usage

```python
from galileo import GalileoLogger

# Initialize the logger
logger = GalileoLogger(project="my_project", log_stream="my_log_stream")

# Track a trace with audio files
trace = logger.start_trace(
    input="Convert this audio to text",
    input_audio_file_path="path/to/input.wav",  # Path to input .wav file
    output_audio_file_path="path/to/output.wav"  # Path to output .wav file
)

# Add spans if needed
logger.add_llm_span(
    input="Convert this audio to text",
    output="Here is the transcription...",
    model="whisper-large-v3"
)

# Conclude the trace
logger.conclude(output="Text transcription complete")

# Flush to send data to Galileo
logger.flush()
```

## How It Works

1. When you provide an audio file path to `start_trace()`, the file is automatically uploaded to Galileo's servers.
2. The audio file is attached to the trace with a unique file ID.
3. The audio file can be played back and analyzed in the Galileo UI.

## Requirements

- Audio files must be in `.wav` format
- The file paths must be valid and accessible
- The SDK must have proper authentication set up

## Advanced Usage

For more complex scenarios, you can:

```python
# Upload audio files manually if needed
from galileo.utils.audio_file import upload_audio_file

# Upload a file and get its ID
audio_file_id = upload_audio_file("path/to/audio.wav")

# Use the ID directly if you've pre-uploaded the files
trace = logger.start_trace(
    input="Process the audio I uploaded earlier",
    # These fields are added internally when you use input_audio_file_path
    # but can be set directly if needed
    input_audio_file_id=audio_file_id,
    output_audio_file_id=another_audio_file_id
)
```