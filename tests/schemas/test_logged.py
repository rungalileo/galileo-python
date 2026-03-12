"""Tests for SDK-local ingestion models (Logged variants and content blocks)."""

import pytest
from pydantic import ValidationError

from galileo.schema.content_blocks import DataContentBlock, TextContentBlock
from galileo.schema.logged import LoggedAgentSpan, LoggedLlmSpan, LoggedTrace, LoggedWorkflowSpan
from galileo.schema.message import LoggedMessage
from galileo.schema.trace import TracesIngestRequest
from galileo_core.schemas.logging.llm import MessageRole
from galileo_core.schemas.logging.span import AgentSpan, LlmSpan, WorkflowSpan
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.multimodal import ContentModality


class TestTextContentBlock:
    def test_basic_text_block(self) -> None:
        # Given: a plain text string
        block = TextContentBlock(text="hello world")

        # Then: fields are set correctly
        assert block.type == "text"
        assert block.text == "hello world"
        assert block.index is None
        assert block.metadata is None

    def test_text_block_with_metadata(self) -> None:
        # Given: a text block with index and metadata
        block = TextContentBlock(text="chunk", index=0, metadata={"source": "doc1"})

        # Then: all fields are preserved
        assert block.index == 0
        assert block.metadata == {"source": "doc1"}


class TestDataContentBlock:
    def test_base64_source(self) -> None:
        # Given: a data block with base64 content
        block = DataContentBlock(modality=ContentModality.image, mime_type="image/png", base64="iVBORw0KGgoAAAANS")

        # Then: source is base64
        assert block.type == "data"
        assert block.modality == ContentModality.image
        assert block.base64 is not None
        assert block.url is None
        assert block.provider_file_id is None

    def test_url_source(self) -> None:
        # Given: a data block with URL content
        block = DataContentBlock(modality=ContentModality.image, url="https://example.com/image.png")

        # Then: source is url
        assert block.url == "https://example.com/image.png"
        assert block.base64 is None

    def test_provider_file_id_source(self) -> None:
        # Given: a data block with provider file ID
        block = DataContentBlock(modality=ContentModality.audio, provider_file_id="file-abc123", provider_name="openai")

        # Then: source is provider_file_id with provider_name
        assert block.provider_file_id == "file-abc123"
        assert block.provider_name == "openai"

    def test_no_source_raises(self) -> None:
        # When/Then: missing all source fields raises
        with pytest.raises(ValidationError, match="Exactly one of"):
            DataContentBlock(modality=ContentModality.image)

    def test_multiple_sources_raises(self) -> None:
        # When/Then: multiple source fields raises
        with pytest.raises(ValidationError, match="Exactly one of"):
            DataContentBlock(modality=ContentModality.image, base64="abc", url="https://example.com/img.png")

    def test_provider_file_id_without_name_raises(self) -> None:
        # When/Then: provider_file_id without provider_name raises
        with pytest.raises(ValidationError, match="provider_name is required"):
            DataContentBlock(modality=ContentModality.image, provider_file_id="file-abc123")


class TestLoggedMessage:
    def test_string_content(self) -> None:
        # Given: a LoggedMessage with plain string content
        msg = LoggedMessage(content="Hello", role=MessageRole.user)

        # Then: content is the string
        assert msg.content == "Hello"
        assert msg.role == MessageRole.user

    def test_multimodal_content(self) -> None:
        # Given: a LoggedMessage with mixed text + data content
        msg = LoggedMessage(
            content=[
                TextContentBlock(text="Describe this image"),
                DataContentBlock(modality=ContentModality.image, url="https://example.com/photo.jpg"),
            ],
            role=MessageRole.user,
        )

        # Then: content is a list of IngestContentBlocks
        assert isinstance(msg.content, list)
        assert len(msg.content) == 2
        assert isinstance(msg.content[0], TextContentBlock)
        assert isinstance(msg.content[1], DataContentBlock)


class TestLoggedTrace:
    def test_string_input_output(self) -> None:
        # Given: a LoggedTrace with simple string input/output
        trace = LoggedTrace(input="hello", output="world")

        # Then: fields are set correctly and it's a Trace subclass
        assert trace.input == "hello"
        assert trace.output == "world"
        assert isinstance(trace, Trace)

    def test_multimodal_input(self) -> None:
        # Given: a LoggedTrace with multimodal message input
        trace = LoggedTrace(
            input=[
                LoggedMessage(
                    content=[
                        TextContentBlock(text="Analyze this"),
                        DataContentBlock(modality=ContentModality.image, base64="abc123"),
                    ],
                    role=MessageRole.user,
                )
            ]
        )

        # Then: input contains a LoggedMessage with multimodal content
        assert isinstance(trace.input, list)
        assert len(trace.input) == 1
        assert isinstance(trace.input[0].content, list)
        assert len(trace.input[0].content) == 2


class TestLoggedWorkflowSpan:
    def test_string_input_output(self) -> None:
        # Given: a LoggedWorkflowSpan with string input/output
        span = LoggedWorkflowSpan(input="start", output="done")

        # Then: fields are correct
        assert span.input == "start"
        assert span.output == "done"
        assert span.type == "workflow"

    def test_multimodal_input(self) -> None:
        # Given: a LoggedWorkflowSpan with multimodal message input
        span = LoggedWorkflowSpan(input=[LoggedMessage(content="process this", role=MessageRole.user)])

        # Then: input contains a LoggedMessage
        assert isinstance(span.input, list)
        assert len(span.input) == 1


class TestLoggedAgentSpan:
    def test_string_input_output(self) -> None:
        # Given: a LoggedAgentSpan with string input/output
        span = LoggedAgentSpan(input="query", output="answer")

        # Then: fields are correct
        assert span.input == "query"
        assert span.output == "answer"
        assert span.type == "agent"


class TestLoggedLlmSpan:
    def test_string_messages(self) -> None:
        # Given: a LoggedLlmSpan with string content messages
        span = LoggedLlmSpan(
            input=[LoggedMessage(content="Hello", role=MessageRole.user)],
            output=LoggedMessage(content="Hi there", role=MessageRole.assistant),
        )

        # Then: input and output are LoggedMessage instances
        assert len(span.input) == 1
        assert span.input[0].content == "Hello"
        assert span.output.content == "Hi there"

    def test_multimodal_messages(self) -> None:
        # Given: a LoggedLlmSpan with multimodal message content
        span = LoggedLlmSpan(
            input=[
                LoggedMessage(
                    content=[
                        TextContentBlock(text="What is this?"),
                        DataContentBlock(modality=ContentModality.image, url="https://example.com/img.png"),
                    ],
                    role=MessageRole.user,
                )
            ],
            output=LoggedMessage(content="That is a photo of a cat.", role=MessageRole.assistant),
        )

        # Then: input message has multimodal content
        assert isinstance(span.input[0].content, list)
        assert len(span.input[0].content) == 2
        assert isinstance(span.output.content, str)


class TestTracesIngestRequest:
    def test_accepts_logged_trace_with_string(self) -> None:
        # Given: a TracesIngestRequest with a LoggedTrace using simple string input
        request = TracesIngestRequest(traces=[LoggedTrace(input="hello")])

        # Then: the trace is accepted and is a LoggedTrace (which is also a Trace)
        assert len(request.traces) == 1
        assert isinstance(request.traces[0], LoggedTrace)
        assert isinstance(request.traces[0], Trace)

    def test_accepts_logged_trace_with_multimodal(self) -> None:
        # Given: a TracesIngestRequest with a LoggedTrace containing multimodal content
        request = TracesIngestRequest(
            traces=[
                LoggedTrace(
                    input=[
                        LoggedMessage(
                            content=[
                                TextContentBlock(text="multimodal"),
                                DataContentBlock(modality=ContentModality.image, base64="abc"),
                            ],
                            role=MessageRole.user,
                        )
                    ]
                )
            ]
        )

        # Then: the logged trace is accepted
        assert len(request.traces) == 1
        assert isinstance(request.traces[0], LoggedTrace)

    def test_rejects_core_trace(self) -> None:
        # When/Then: a plain core Trace is rejected since TracesIngestRequest expects LoggedTrace
        with pytest.raises(ValidationError, match="LoggedTrace"):
            TracesIngestRequest(traces=[Trace(input="plain text")])


class TestTypeRetention:
    """Verify that concrete types are preserved through object construction, not coerced."""

    def test_logged_message_retains_content_block_types(self) -> None:
        # Given: a LoggedMessage with text and data content blocks
        text_block = TextContentBlock(text="hello")
        data_block = DataContentBlock(modality=ContentModality.image, base64="abc")
        msg = LoggedMessage(content=[text_block, data_block], role=MessageRole.user)

        # Then: each content block retains its exact type
        assert type(msg.content[0]) is TextContentBlock
        assert type(msg.content[1]) is DataContentBlock
        assert msg.content[0].text == "hello"
        assert msg.content[1].modality == ContentModality.image
        assert msg.content[1].base64 == "abc"

    def test_logged_trace_retains_logged_message_in_input(self) -> None:
        # Given: a LoggedTrace with a LoggedMessage containing multimodal content
        msg = LoggedMessage(
            content=[
                TextContentBlock(text="describe"),
                DataContentBlock(modality=ContentModality.image, url="https://img.test/a.png"),
            ],
            role=MessageRole.user,
        )
        trace = LoggedTrace(input=[msg])

        # Then: input[0] is a LoggedMessage, and its content blocks retain types
        assert type(trace.input[0]) is LoggedMessage
        assert trace.input[0].role == MessageRole.user
        assert type(trace.input[0].content[0]) is TextContentBlock
        assert type(trace.input[0].content[1]) is DataContentBlock
        assert trace.input[0].content[1].url == "https://img.test/a.png"

    def test_logged_workflow_span_retains_types(self) -> None:
        # Given: a LoggedWorkflowSpan with LoggedMessage input and output
        span = LoggedWorkflowSpan(
            input=[LoggedMessage(content="start workflow", role=MessageRole.user)],
            output=LoggedMessage(
                content=[DataContentBlock(modality=ContentModality.audio, base64="audio_data")],
                role=MessageRole.assistant,
            ),
        )

        # Then: input and output retain LoggedMessage types with inner blocks
        assert type(span.input[0]) is LoggedMessage
        assert span.input[0].content == "start workflow"
        assert type(span.output) is LoggedMessage
        assert type(span.output.content[0]) is DataContentBlock
        assert span.output.content[0].modality == ContentModality.audio

    def test_logged_agent_span_retains_types(self) -> None:
        # Given: a LoggedAgentSpan with multimodal LoggedMessage input
        span = LoggedAgentSpan(
            input=[
                LoggedMessage(
                    content=[
                        TextContentBlock(text="analyze"),
                        DataContentBlock(
                            modality=ContentModality.document, provider_file_id="file-xyz", provider_name="openai"
                        ),
                    ],
                    role=MessageRole.user,
                )
            ]
        )

        # Then: types are retained all the way down
        assert type(span.input[0]) is LoggedMessage
        assert type(span.input[0].content[0]) is TextContentBlock
        assert type(span.input[0].content[1]) is DataContentBlock
        assert span.input[0].content[1].provider_file_id == "file-xyz"
        assert span.input[0].content[1].provider_name == "openai"

    def test_logged_llm_span_retains_message_types(self) -> None:
        # Given: a LoggedLlmSpan with multimodal input and string output
        span = LoggedLlmSpan(
            input=[
                LoggedMessage(
                    content=[
                        TextContentBlock(text="What do you see?"),
                        DataContentBlock(modality=ContentModality.image, base64="img_bytes"),
                    ],
                    role=MessageRole.user,
                )
            ],
            output=LoggedMessage(content="I see a cat.", role=MessageRole.assistant),
        )

        # Then: input messages retain LoggedMessage with typed content blocks
        assert type(span.input[0]) is LoggedMessage
        assert type(span.input[0].content[0]) is TextContentBlock
        assert type(span.input[0].content[1]) is DataContentBlock
        assert span.input[0].content[1].base64 == "img_bytes"
        # Then: output retains LoggedMessage with string content
        assert type(span.output) is LoggedMessage
        assert span.output.content == "I see a cat."
        assert span.output.role == MessageRole.assistant

    def test_data_content_block_retains_all_fields(self) -> None:
        # Given: a fully populated DataContentBlock
        block = DataContentBlock(
            modality=ContentModality.video,
            mime_type="video/mp4",
            url="https://video.test/clip.mp4",
            index=3,
            metadata={"source": "camera", "duration": "30s"},
        )

        # Then: every field is retained with exact values
        assert block.type == "data"
        assert block.modality == ContentModality.video
        assert block.mime_type == "video/mp4"
        assert block.url == "https://video.test/clip.mp4"
        assert block.index == 3
        assert block.metadata == {"source": "camera", "duration": "30s"}
        assert block.base64 is None
        assert block.provider_file_id is None

    def test_trace_ingest_request_retains_logged_trace(self) -> None:
        # Given: a TracesIngestRequest with a LoggedTrace that has multimodal content
        trace = LoggedTrace(
            input=[
                LoggedMessage(
                    content=[
                        TextContentBlock(text="analyze"),
                        DataContentBlock(modality=ContentModality.image, base64="abc"),
                    ],
                    role=MessageRole.user,
                )
            ],
            output="result",
        )
        request = TracesIngestRequest(traces=[trace])

        # Then: the trace inside the request retains its exact type and nested content
        assert type(request.traces[0]) is LoggedTrace
        assert type(request.traces[0].input[0]) is LoggedMessage
        assert type(request.traces[0].input[0].content[0]) is TextContentBlock
        assert type(request.traces[0].input[0].content[1]) is DataContentBlock


class TestSerialization:
    def test_logged_trace_round_trip(self) -> None:
        # Given: a LoggedTrace with multimodal message input
        trace = LoggedTrace(
            input=[
                LoggedMessage(
                    content=[
                        TextContentBlock(text="Describe this"),
                        DataContentBlock(modality=ContentModality.image, url="https://example.com/photo.jpg"),
                    ],
                    role=MessageRole.user,
                )
            ],
            output="A photo of a sunset",
        )

        # When: serializing
        data = trace.model_dump()

        # Then: input is serialized as a list of message dicts with content blocks
        assert isinstance(data["input"], list)
        assert len(data["input"]) == 1
        assert data["input"][0]["content"][0]["type"] == "text"
        assert data["input"][0]["content"][1]["type"] == "data"
        assert data["output"] == "A photo of a sunset"

    def test_logged_message_round_trip(self) -> None:
        # Given: a LoggedMessage with multimodal content
        msg = LoggedMessage(
            content=[
                TextContentBlock(text="Look at this"),
                DataContentBlock(modality=ContentModality.image, base64="dGVzdA=="),
            ],
            role=MessageRole.user,
        )

        # When: serializing
        data = msg.model_dump()

        # Then: content is serialized as a list of dicts
        assert isinstance(data["content"], list)
        assert len(data["content"]) == 2


class TestLoggedAndCoreParity:
    """Verify Trace/LoggedTrace and Span/LoggedSpan behave identically for plain string content."""

    def test_trace_string_io_parity(self) -> None:
        # Given: the same plain-string fields
        kwargs = dict(input="hello", output="world", name="t")

        # When: constructing both variants
        core = Trace(**kwargs)
        logged = LoggedTrace(**kwargs)

        # Then: field values and serialized output match
        assert core.input == logged.input
        assert core.output == logged.output
        assert core.model_dump(include={"input", "output", "name"}) == logged.model_dump(
            include={"input", "output", "name"}
        )

    def test_workflow_span_string_io_parity(self) -> None:
        kwargs = dict(input="query", output="answer", name="wf")
        core = WorkflowSpan(**kwargs)
        logged = LoggedWorkflowSpan(**kwargs)

        assert core.input == logged.input
        assert core.output == logged.output
        assert core.model_dump(include={"input", "output", "name"}) == logged.model_dump(
            include={"input", "output", "name"}
        )

    def test_agent_span_string_io_parity(self) -> None:
        kwargs = dict(input="task", output="result", name="ag")
        core = AgentSpan(**kwargs)
        logged = LoggedAgentSpan(**kwargs)

        assert core.input == logged.input
        assert core.output == logged.output
        assert core.model_dump(include={"input", "output", "name"}) == logged.model_dump(
            include={"input", "output", "name"}
        )

    def test_llm_span_string_io_parity(self) -> None:
        core = LlmSpan(input="prompt", output="completion", name="llm", model="gpt-4")
        logged = LoggedLlmSpan(input="prompt", output="completion", name="llm", model="gpt-4")

        assert core.input == logged.input
        assert core.output == logged.output
        assert core.model_dump(include={"input", "output", "name", "model"}) == logged.model_dump(
            include={"input", "output", "name", "model"}
        )

    def test_logged_trace_is_instance_of_trace(self) -> None:
        logged = LoggedTrace(input="x")

        assert isinstance(logged, Trace)
        assert isinstance(logged, LoggedTrace)

    def test_logged_spans_are_instances_of_core(self) -> None:
        assert isinstance(LoggedWorkflowSpan(input="x"), WorkflowSpan)
        assert isinstance(LoggedAgentSpan(input="x"), AgentSpan)
        assert isinstance(LoggedLlmSpan(input="x"), LlmSpan)
