# Datalab Form Filling API Reference

## Table of Contents

- [Installation & Auth](#installation--auth)
- [Client Setup](#client-setup)
- [FormFillingOptions](#formfillingoptions)
- [Field Data Format](#field-data-format)
- [Field Types](#field-types)
- [Result Object](#result-object)
- [Error Handling](#error-handling)
- [Async Client](#async-client)

## Installation & Auth

```bash
pip install datalab-python-sdk python-dotenv
```

Requires Python 3.10+.

**API Key**: Set `DATALAB_API_KEY` as environment variable or in a `.env` file.

## Client Setup

**Recommended pattern** (for a `.py` script file; in a notebook/REPL, `__file__` is undefined—use `Path(".")` or explicit paths):

```python
import os
from pathlib import Path
from dotenv import load_dotenv
from datalab_sdk import DatalabClient

# In a script: script_dir = Path(__file__).parent. In notebook/REPL: Path(".")
script_dir = Path(__file__).parent
load_dotenv(script_dir / ".env")

# Always pass api_key explicitly - don't rely on auto-detection
client = DatalabClient(api_key=os.getenv("DATALAB_API_KEY"))
```

**Why explicit API key passing?**

- `load_dotenv()` without a path only searches the current working directory, which varies based on how the script is invoked
- Relying on `DatalabClient()` auto-detecting the env var fails when .env isn't loaded
- Explicit passing ensures consistent behavior regardless of working directory

**Alternative** (if you're certain the env var is set):

```python
from datalab_sdk import DatalabClient
client = DatalabClient()  # uses DATALAB_API_KEY env var

# Or with explicit config
client = DatalabClient(
    api_key="your_key",
    base_url="https://www.datalab.to",
    timeout=300,
)
```

## FormFillingOptions

```python
from datalab_sdk import FormFillingOptions
```

| Option                 | Type  | Default  | Description                                           |
| ---------------------- | ----- | -------- | ----------------------------------------------------- |
| `field_data`           | dict  | Required | Field names mapped to values and descriptions         |
| `context`              | str   | None     | Additional context to help match fields               |
| `confidence_threshold` | float | 0.5      | Minimum confidence for field matching (0.0-1.0)       |
| `max_pages`            | int   | None     | Maximum pages to process                              |
| `page_range`           | str   | None     | Specific pages, 0-indexed (e.g., `"0-2"` = pages 1-3) |
| `skip_cache`           | bool  | False    | Skip cached results                                   |

### Confidence Threshold Guidance

- **0.3-0.5**: More fields matched, may have incorrect matches
- **0.7-0.9**: Fewer fields matched, more accurate

## Field Data Format

```python
field_data = {
    "field_key": {
        "value": "The value to fill",
        "description": "Description to help match the field"
    }
}
```

The `description` helps match field keys to actual form fields when PDF field names differ from your data structure.

## Field Types

```python
# Text
"name": {"value": "Jane Smith", "description": "Full name"}

# Date
"date": {"value": "2024-01-15", "description": "Today's date"}

# Numeric
"amount": {"value": "1500.00", "description": "Total amount"}

# Checkbox
"agree_terms": {"value": "Yes", "description": "Agreement checkbox"}

# Signature (text rendered)
"signature": {"value": "Jane Smith", "description": "Signature field"}
```

## Result Object

```python
result = client.fill("form.pdf", options=options)
```

| Field              | Type  | Description                          |
| ------------------ | ----- | ------------------------------------ |
| `success`          | bool  | Whether form filling succeeded       |
| `status`           | str   | Processing status                    |
| `output_format`    | str   | `"pdf"` or `"png"`                   |
| `output_base64`    | str   | Base64-encoded filled form           |
| `fields_filled`    | list  | Field names successfully filled      |
| `fields_not_found` | list  | Field names that couldn't be matched |
| `page_count`       | int   | Number of pages processed            |
| `runtime`          | float | Processing time in seconds           |
| `cost_breakdown`   | dict  | Cost details                         |

### Saving Output

```python
result.save_output("filled_form.pdf")

# Or raw base64
import base64
pdf_bytes = base64.b64decode(result.output_base64)
with open("filled.pdf", "wb") as f:
    f.write(pdf_bytes)
```

## Error Handling

```python
from datalab_sdk.exceptions import (
    DatalabAPIError,        # API error (has status_code, response_data)
    DatalabTimeoutError,    # Request exceeded timeout
    DatalabFileError,       # File not found or unreadable
    DatalabValidationError, # Invalid parameters
)
```

Automatic retries for: 408 (timeout), 429 (rate limit), 5xx (server errors) with exponential backoff.

## Async Client

```python
import os
from datalab_sdk import AsyncDatalabClient, FormFillingOptions

# Pass api_key explicitly for consistent behavior (same as sync client)
async with AsyncDatalabClient(api_key=os.getenv("DATALAB_API_KEY")) as client:
    result = await client.fill("form.pdf", options=options)
    result.save_output("filled.pdf")
```

### Batch Processing (Async)

```python
import asyncio
import os
from datalab_sdk import AsyncDatalabClient, FormFillingOptions

async def fill_batch(files, options):
    async with AsyncDatalabClient(api_key=os.getenv("DATALAB_API_KEY")) as client:
        tasks = [client.fill(f, options=options) for f in files]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

## Input Sources

```python
# Local file
result = client.fill("form.pdf", options=options)

# URL
result = client.fill(file_url="https://example.com/form.pdf", options=options)

# Image forms (PNG, JPG)
result = client.fill("scanned_form.png", options=options)
```
