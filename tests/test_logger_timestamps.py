from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

from galileo.logger import GalileoLogger
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
def test_rapid_span_creation_ensures_uniqueness(mock_projects_client: Mock, mock_logstreams_client: Mock):
    """Tests that creating spans in a tight loop results in unique, monotonically increasing timestamps."""
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    logger = GalileoLogger(project="test", log_stream="test")
    logger.start_trace(input="test")
    for _ in range(5):
        logger.add_llm_span(input="test", output="test", model="test")
    logger.conclude(output="test")

    trace = logger.traces[0]
    timestamps = [span.created_at for span in trace.spans]
    assert len(timestamps) == len(set(timestamps)), "Timestamps should be unique"
    assert timestamps == sorted(timestamps), "Timestamps should be monotonically increasing"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
def test_user_provided_timestamps_are_respected(mock_projects_client: Mock, mock_logstreams_client: Mock):
    """Tests that timestamps provided by the user are not modified."""
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    logger = GalileoLogger(project="test", log_stream="test")
    logger.start_trace(input="test")

    # Create timestamps in reverse order to test that the logger doesn't alter them
    now = datetime.now(timezone.utc)
    timestamps = [now - timedelta(seconds=i) for i in range(5)]

    for ts in timestamps:
        logger.add_llm_span(input="test", output="test", model="test", created_at=ts)

    logger.conclude(output="test")

    trace = logger.traces[0]
    span_timestamps = [span.created_at for span in trace.spans]
    assert span_timestamps == timestamps, "User-provided timestamps should be respected"


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
def test_mixed_default_and_user_timestamps(mock_projects_client: Mock, mock_logstreams_client: Mock):
    """Tests that the internal state for default timestamp generation is not affected by user-provided timestamps."""
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    logger = GalileoLogger(project="test", log_stream="test")
    logger.start_trace(input="test")

    # 1. Add a default span
    logger.add_llm_span(input="test", output="test", model="test")

    # 2. Add a user-provided span with a timestamp in the past
    past_timestamp = datetime.now(timezone.utc) - timedelta(seconds=10)
    logger.add_llm_span(input="test", output="test", model="test", created_at=past_timestamp)

    # 3. Add a user-provided span with a timestamp in the future
    future_timestamp = datetime.now(timezone.utc) + timedelta(seconds=10)
    logger.add_llm_span(input="test", output="test", model="test", created_at=future_timestamp)

    # 4. Add a final default span
    logger.add_llm_span(input="test", output="test", model="test")

    logger.conclude(output="test")
    trace = logger.traces[0]

    default_span1_ts = trace.spans[0].created_at
    past_user_span_ts = trace.spans[1].created_at
    future_user_span_ts = trace.spans[2].created_at
    default_span2_ts = trace.spans[3].created_at

    assert past_user_span_ts == past_timestamp, "User-provided past timestamp should be respected"
    assert future_user_span_ts == future_timestamp, "User-provided future timestamp should be respected"
    assert default_span2_ts > default_span1_ts, "Second default timestamp should be greater than the first"
    assert default_span2_ts > past_user_span_ts, "Default timestamps are separate from past user-provided timestamps"
    assert default_span2_ts < future_user_span_ts, (
        "Default timestamps are separate from future user-provided timestamps"
    )
