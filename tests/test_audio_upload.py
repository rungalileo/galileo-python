import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

import pytest

from galileo.utils.audio_file import upload_audio_file
from galileo.logger import GalileoLogger


class TestAudioFileUpload(unittest.TestCase):
    @patch('galileo.utils.audio_file.sync')
    @patch('galileo.utils.audio_file.GalileoApiClient')
    def test_upload_audio_file(self, mock_client, mock_sync):
        # Setup mock client
        mock_client.return_value.client = 'fake_client'
        mock_client.return_value.get_project_id.return_value = 'fake_project_id'
        
        # Setup mock sync response
        mock_sync.return_value = {'id': 'fake_audio_file_id'}
        
        # Create a temporary wav file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(b'fake audio content')
            temp_file_path = temp_file.name
        
        try:
            # Call the function
            result = upload_audio_file(temp_file_path)
            
            # Assertions
            self.assertEqual(result, 'fake_audio_file_id')
            mock_sync.assert_called_once()
        finally:
            # Clean up
            os.unlink(temp_file_path)

    @patch('galileo.utils.audio_file.upload_audio_file')
    @patch('galileo.logger.TracesLogger.add_trace')
    @patch('galileo.logger.GalileoLogger._init_project')
    def test_start_trace_with_audio(self, mock_init, mock_add_trace, mock_upload):
        # Setup mocks
        mock_upload.return_value = 'fake_audio_file_id'
        mock_add_trace.return_value = MagicMock()
        
        # Create logger
        logger = GalileoLogger(project='test_project', log_stream='test_log_stream')
        
        # Call start_trace with audio files
        logger.start_trace(
            input="Test input",
            input_audio_file_path='/fake/path/input.wav',
            output_audio_file_path='/fake/path/output.wav'
        )
        
        # Assertions
        mock_upload.assert_any_call('/fake/path/input.wav')
        mock_upload.assert_any_call('/fake/path/output.wav')
        self.assertEqual(mock_upload.call_count, 2)
        
        # Verify add_trace was called with the audio file IDs
        _, kwargs = mock_add_trace.call_args
        self.assertEqual(kwargs['input_audio_file_id'], 'fake_audio_file_id')
        self.assertEqual(kwargs['output_audio_file_id'], 'fake_audio_file_id')


@pytest.mark.e2e
def test_audio_integration():
    """Integration test that requires actual audio files and project access to run."""
    # This test would be run manually or in a CI environment with proper credentials
    pass