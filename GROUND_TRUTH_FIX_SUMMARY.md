# Ground Truth Column Display Fix

## Problem
When users create datasets via the SDK with `ground_truth` field, the data was appearing in the `input` column instead of the `output` column in the Galileo UI.

Example:
```python
from galileo.datasets import create_dataset

test_data = [
    {"input": "Which continent is Spain in?", "ground_truth": "Europe"},
    {"input": "Which continent is Japan in?", "ground_truth": "Asia"},
]

dataset = create_dataset(name="countries-dataset", content=test_data)
```

**Expected behavior:** `ground_truth` data should appear in the "Ground Truth" column (internally stored as `output`)

**Actual behavior:** `ground_truth` data was appearing merged into the `input` column

## Root Cause
The SDK's `DatasetRecord` schema had a `@model_validator` to normalize `ground_truth` → `output` (PR #458), but this validation was **never executed** during dataset creation.

The `Datasets.create()` method converted the user's data directly to JSONL without passing it through `DatasetRecord`, so the normalization never happened:

```python
# Old flow (broken):
User data with ground_truth → parse_dataset() → JSONL file → API
                              ❌ No normalization!
```

## Solution
Modified `Datasets.create()` in `src/galileo/datasets.py` to validate all records through `DatasetRecord` before converting to JSONL:

```python
# New flow (fixed):
User data with ground_truth → DatasetRecord validation → normalized data → JSONL → API
                              ✅ ground_truth → output
```

### Code Changes

**File:** `src/galileo/datasets.py` (lines 460-479)

Added normalization logic before `parse_dataset()`:

```python
# Normalize records through DatasetRecord to handle ground_truth -> output conversion
# Skip normalization for empty content or when content only has empty dicts
if isinstance(content, list) and len(content) > 0:
    normalized_content = []
    for row in content:
        if isinstance(row, dict) and len(row) > 0:
            # Validate and normalize through DatasetRecord (handles ground_truth -> output)
            record = DatasetRecord(**row)
            # Convert back to dict with normalized field names
            normalized_row = record.model_dump(exclude_none=True)
            normalized_content.append(normalized_row)
        else:
            normalized_content.append(row)
    content = normalized_content
```

**Key implementation details:**
- Only normalizes non-empty lists to avoid breaking empty dataset creation
- Skips empty dicts (`{}`) to preserve existing behavior
- Uses `DatasetRecord(**row)` to trigger Pydantic's `normalize_ground_truth` validator
- Exports normalized data via `model_dump(exclude_none=True)` to remove None fields

### Test Coverage

**File:** `tests/test_datasets.py` (lines 1358-1407)

Added test `test_create_dataset_normalizes_ground_truth_to_output()` which:
1. Creates dataset with `ground_truth` fields
2. Mocks the API call
3. Reads the generated JSONL file
4. Verifies `ground_truth` was converted to `output` before API call

## Verification

Run the test:
```bash
poetry run pytest tests/test_datasets.py::test_create_dataset_normalizes_ground_truth_to_output -v
```

**Result:** ✅ All 42 tests in `test_datasets.py` pass

## Impact
- **Users can now use `ground_truth` field** when creating datasets via SDK
- Data will correctly appear in the "Ground Truth" column in the UI
- Backward compatible: existing code using `output` continues to work
- No API changes needed - the fix is entirely in the SDK

## Related PRs
- SDK Schema PR #458: Added `ground_truth` support to `DatasetRecord`
- Docs PR #496: Documents `ground_truth` field usage

## Testing Checklist
- [x] Unit test added for normalization logic
- [x] All existing tests still pass
- [x] Empty list/dict edge cases handled correctly
- [ ] Manual E2E test with production API (requires API token)
