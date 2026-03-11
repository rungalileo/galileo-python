#!/usr/bin/env python3
"""
E2E tests for SDK trigger=True migration.

Tests both prompt-driven (regression) and generated-output (new) flows
to ensure the switch from POST /jobs to POST /experiments (trigger=True)
does not cause regressions.

Usage:
    GALILEO_API_KEY="..." GALILEO_CONSOLE_URL="..." python test_sdk_trigger_e2e.py

Environments:
    demo-v2:  GALILEO_CONSOLE_URL=https://console.demo-v2.galileocloud.io
    staging:  GALILEO_CONSOLE_URL=https://console.staging.galileo.ai
"""

import os
import sys
import traceback
from datetime import datetime, timezone

# Add src to path for local dev
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# ─── Configuration ───────────────────────────────────────────────────

API_KEY = os.getenv("GALILEO_API_KEY")
CONSOLE_URL = os.getenv("GALILEO_CONSOLE_URL")
PROJECT_NAME = os.getenv("GALILEO_PROJECT", "Test1")

if not API_KEY or not CONSOLE_URL:
    print("ERROR: Set GALILEO_API_KEY and GALILEO_CONSOLE_URL")
    sys.exit(1)

# ─── Results tracking ────────────────────────────────────────────────

results: list[dict] = []


def record(test_name: str, status: str, detail: str = ""):
    results.append({"test": test_name, "status": status, "detail": detail})
    symbol = "PASS" if status == "PASS" else "FAIL" if status == "FAIL" else "SKIP"
    print(f"  [{symbol}] {test_name}" + (f" — {detail}" if detail else ""))


def print_summary():
    print("\n" + "=" * 70)
    print("E2E TEST SUMMARY")
    print("=" * 70)
    print(f"Environment: {CONSOLE_URL}")
    print(f"Project:     {PROJECT_NAME}")
    print()
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    for r in results:
        symbol = "PASS" if r["status"] == "PASS" else "FAIL" if r["status"] == "FAIL" else "SKIP"
        line = f"  [{symbol}] {r['test']}"
        if r["detail"]:
            line += f" — {r['detail']}"
        print(line)
    print()
    print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed} | Skipped: {skipped}")
    if failed > 0:
        print("\n*** REGRESSION DETECTED — DO NOT SHIP ***")
    else:
        print("\n*** ALL TESTS PASSED — SAFE TO SHIP ***")
    print("=" * 70)
    return failed == 0


# ─── Test helpers ────────────────────────────────────────────────────

def unique_name(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%H%M%S")
    return f"{prefix}-{ts}"


# ─── Test 1: Generated output flow (NEW) ────────────────────────────

def test_1_generated_output_basic():
    """Generated output dataset + no prompt → experiment created + triggered."""
    from galileo.datasets import create_dataset
    from galileo.experiments import run_experiment
    from galileo import GalileoMetrics

    name = unique_name("e2e-genout-basic")
    dataset = create_dataset(
        name=name,
        content=[
            {
                "input": "What is 2+2?",
                "generated_output": "4",
            },
            {
                "input": "What color is the sky?",
                "generated_output": "The sky is blue.",
            },
        ],
    )
    assert dataset.dataset.id is not None, "Dataset not created"

    result = run_experiment(
        name,
        dataset=dataset,
        metrics=[GalileoMetrics.completeness],
        project=PROJECT_NAME,
    )
    assert "experiment" in result, "No experiment in result"
    assert result["experiment"].id is not None, "Experiment ID is None"
    assert "link" in result, "No link in result"
    record("test_1_generated_output_basic", "PASS", f"exp={result['experiment'].id}")


# ─── Test 2: Generated output with ground_truth ─────────────────────

def test_2_generated_output_with_ground_truth():
    """Generated output + ground_truth + ground_truth_adherence metric."""
    from galileo.datasets import create_dataset
    from galileo.experiments import run_experiment
    from galileo import GalileoMetrics

    name = unique_name("e2e-genout-gt")
    dataset = create_dataset(
        name=name,
        content=[
            {
                "input": "Capital of France?",
                "generated_output": "Paris is the capital.",
                "ground_truth": "Paris",
            },
            {
                "input": "Capital of Japan?",
                "generated_output": "Tokyo is the capital of Japan.",
                "ground_truth": "Tokyo",
            },
        ],
    )

    result = run_experiment(
        name,
        dataset=dataset,
        metrics=[
            GalileoMetrics.completeness,
            GalileoMetrics.context_adherence,
            GalileoMetrics.ground_truth_adherence,
        ],
        project=PROJECT_NAME,
    )
    assert result["experiment"].id is not None
    record("test_2_generated_output_with_ground_truth", "PASS", f"exp={result['experiment'].id}")


# ─── Test 3: Error case — no prompt, no generated_output ────────────

def test_3_error_no_prompt_no_generated_output():
    """Dataset without generated_output + no prompt → should return error 3512."""
    from galileo.datasets import create_dataset
    from galileo.experiments import run_experiment
    from galileo import GalileoMetrics

    name = unique_name("e2e-error-3512")
    dataset = create_dataset(
        name=name,
        content=[
            {"input": "What is 2+2?"},
            {"input": "What color is the sky?"},
        ],
    )

    try:
        run_experiment(
            name,
            dataset=dataset,
            metrics=[GalileoMetrics.completeness],
            project=PROJECT_NAME,
        )
        record("test_3_error_no_prompt_no_generated_output", "FAIL", "Expected error but got success")
    except Exception as e:
        error_msg = str(e)
        # Should get error about prompt or generated_output
        if "3512" in error_msg or "prompt" in error_msg.lower() or "generated" in error_msg.lower():
            record("test_3_error_no_prompt_no_generated_output", "PASS", f"Got expected error: {error_msg[:100]}")
        else:
            record("test_3_error_no_prompt_no_generated_output", "FAIL", f"Unexpected error: {error_msg[:150]}")


# ─── Test 4: Prompt-driven flow REGRESSION ───────────────────────────

def test_4_prompt_driven_regression():
    """Prompt template + dataset → experiment created + triggered (REGRESSION TEST)."""
    from galileo.datasets import create_dataset
    from galileo.experiments import run_experiment
    from galileo.prompts import create_prompt_template
    from galileo.resources.models.message import Message
    from galileo.resources.models.message_role import MessageRole
    from galileo import GalileoMetrics

    name = unique_name("e2e-prompt-regr")

    # Create dataset (input only, no generated_output)
    dataset = create_dataset(
        name=name,
        content=[
            {"input": "What is the capital of France?"},
            {"input": "What is 2+2?"},
        ],
    )

    # Create prompt template
    prompt = create_prompt_template(
        name=name,
        project=PROJECT_NAME,
        messages=[Message(role=MessageRole.USER, content="Answer this question: {{input}}")],
    )
    assert prompt.selected_version_id is not None, "Prompt template has no selected_version_id"

    result = run_experiment(
        name,
        dataset=dataset,
        prompt_template=prompt,
        metrics=[GalileoMetrics.completeness],
        project=PROJECT_NAME,
    )
    assert result["experiment"].id is not None
    record("test_4_prompt_driven_regression", "PASS", f"exp={result['experiment'].id}")


# ─── Test 5: Generated output without metrics ───────────────────────

def test_5_generated_output_no_metrics():
    """Generated output + NO metrics → experiment still created."""
    from galileo.datasets import create_dataset
    from galileo.experiments import run_experiment

    name = unique_name("e2e-genout-nomet")
    dataset = create_dataset(
        name=name,
        content=[
            {"input": "Hello", "generated_output": "Hi there!"},
        ],
    )

    result = run_experiment(
        name,
        dataset=dataset,
        project=PROJECT_NAME,
    )
    assert result["experiment"].id is not None
    record("test_5_generated_output_no_metrics", "PASS", f"exp={result['experiment'].id}")


# ─── Test 6: Custom function flow (REGRESSION) ──────────────────────

def test_6_custom_function_regression():
    """Custom function + dataset → should still use trigger=False path (REGRESSION TEST)."""
    from galileo.datasets import create_dataset
    from galileo.experiments import run_experiment

    name = unique_name("e2e-func-regr")
    dataset = create_dataset(
        name=name,
        content=[
            {"input": "What is 2+2?"},
            {"input": "What color is the sky?"},
        ],
    )

    def my_func(input_text):
        return f"Answer: {input_text}"

    result = run_experiment(
        name,
        dataset=dataset,
        function=my_func,
        project=PROJECT_NAME,
    )
    assert result["experiment"].id is not None
    record("test_6_custom_function_regression", "PASS", f"exp={result['experiment'].id}")


# ─── Test 7: Existing dataset via get_dataset ────────────────────────

def test_7_existing_dataset():
    """Create dataset, then fetch it with get_dataset and run experiment."""
    from galileo.datasets import create_dataset, get_dataset
    from galileo.experiments import run_experiment
    from galileo import GalileoMetrics

    name = unique_name("e2e-existing-ds")

    # Create it first
    created = create_dataset(
        name=name,
        content=[
            {"input": "Test question", "generated_output": "Test answer"},
        ],
    )

    # Fetch it back
    fetched = get_dataset(name=name)
    assert fetched is not None, "get_dataset returned None"
    assert str(fetched.dataset.id) == str(created.dataset.id), "Dataset IDs don't match"

    result = run_experiment(
        name,
        dataset=fetched,
        metrics=[GalileoMetrics.completeness],
        project=PROJECT_NAME,
    )
    assert result["experiment"].id is not None
    record("test_7_existing_dataset", "PASS", f"exp={result['experiment'].id}")


# ─── Test 8: Experiment name collision ───────────────────────────────

def test_8_experiment_name_collision():
    """Running same experiment name twice → second gets timestamp suffix."""
    from galileo.datasets import create_dataset
    from galileo.experiments import run_experiment
    from galileo import GalileoMetrics

    name = unique_name("e2e-collision")
    dataset = create_dataset(
        name=name,
        content=[
            {"input": "Q1", "generated_output": "A1"},
        ],
    )

    # First run
    result1 = run_experiment(
        name,
        dataset=dataset,
        metrics=[GalileoMetrics.completeness],
        project=PROJECT_NAME,
    )
    exp_name_1 = result1["experiment"].name

    # Second run with same name
    result2 = run_experiment(
        name,
        dataset=dataset,
        metrics=[GalileoMetrics.completeness],
        project=PROJECT_NAME,
    )
    exp_name_2 = result2["experiment"].name

    assert exp_name_1 != exp_name_2, f"Names should differ: {exp_name_1} vs {exp_name_2}"
    assert name in exp_name_2, f"Second name should contain original: {exp_name_2}"
    record("test_8_experiment_name_collision", "PASS", f"'{exp_name_1}' vs '{exp_name_2}'")


# ─── Test 9: Prompt-driven with prompt_settings ─────────────────────

def test_9_prompt_with_custom_settings():
    """Prompt template + explicit prompt_settings → should use provided settings."""
    from galileo.datasets import create_dataset
    from galileo.experiments import run_experiment
    from galileo.prompts import create_prompt_template
    from galileo.resources.models.message import Message
    from galileo.resources.models.message_role import MessageRole
    from galileo.resources.models.prompt_run_settings import PromptRunSettings
    from galileo import GalileoMetrics

    name = unique_name("e2e-prompt-settings")

    dataset = create_dataset(
        name=name,
        content=[{"input": "Say hello"}],
    )

    prompt = create_prompt_template(
        name=name,
        project=PROJECT_NAME,
        messages=[Message(role=MessageRole.USER, content="{{input}}")],
    )

    settings = PromptRunSettings(
        model_alias="GPT-4o mini",
        temperature=0.1,
        max_tokens=50,
    )

    result = run_experiment(
        name,
        dataset=dataset,
        prompt_template=prompt,
        prompt_settings=settings,
        metrics=[GalileoMetrics.completeness],
        project=PROJECT_NAME,
    )
    assert result["experiment"].id is not None
    record("test_9_prompt_with_custom_settings", "PASS", f"exp={result['experiment'].id}")


# ─── Main ────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print(f"SDK trigger=True E2E Tests")
    print(f"Environment: {CONSOLE_URL}")
    print(f"Project:     {PROJECT_NAME}")
    print("=" * 70)

    tests = [
        ("1. Generated output (basic)", test_1_generated_output_basic),
        ("2. Generated output + ground_truth", test_2_generated_output_with_ground_truth),
        ("3. Error: no prompt, no generated_output", test_3_error_no_prompt_no_generated_output),
        ("4. REGRESSION: Prompt-driven flow", test_4_prompt_driven_regression),
        ("5. Generated output, no metrics", test_5_generated_output_no_metrics),
        ("6. REGRESSION: Custom function flow", test_6_custom_function_regression),
        ("7. Existing dataset via get_dataset", test_7_existing_dataset),
        ("8. Experiment name collision", test_8_experiment_name_collision),
        ("9. REGRESSION: Prompt + custom settings", test_9_prompt_with_custom_settings),
    ]

    for label, test_fn in tests:
        print(f"\n--- {label} ---")
        try:
            test_fn()
        except Exception as e:
            tb = traceback.format_exc()
            record(test_fn.__name__, "FAIL", f"{type(e).__name__}: {str(e)[:150]}")
            print(f"  Traceback:\n{tb}")

    return print_summary()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
