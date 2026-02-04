#!/usr/bin/env python3
"""Fill a PDF or image form using the Datalab SDK.

Usage:
    python fill_form.py <form_path_or_url> <field_data_json> [options]

Arguments:
    form_path_or_url    Path to local file or URL of the form
    field_data_json     Path to JSON file with field data

Options:
    --output, -o        Output file path (default: filled_<input_name>)
    --context, -c       Context string to improve field matching
    --threshold, -t     Confidence threshold 0.0-1.0 (default: 0.5)
    --page-range, -p    Page range to process (e.g., "0-2")
    --async             Use async client for processing

Field data JSON format:
{
    "field_name": {
        "value": "field value",
        "description": "description to help match"
    }
}
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

# Load .env from script's directory or parent directories
try:
    from dotenv import load_dotenv
    script_dir = Path(__file__).parent
    # Try script dir first, then parent (skill root), then project root
    for env_path in [script_dir / ".env", script_dir.parent / ".env", Path.cwd() / ".env"]:
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    pass  # dotenv not installed, rely on environment variables


def parse_args():
    parser = argparse.ArgumentParser(description="Fill a form using Datalab SDK")
    parser.add_argument("form", help="Path to form file or URL")
    parser.add_argument("field_data", help="Path to JSON file with field data")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-c", "--context", help="Context for field matching")
    parser.add_argument(
        "-t", "--threshold", type=float, default=0.5, help="Confidence threshold"
    )
    parser.add_argument("-p", "--page-range", help="Page range (e.g., '0-2')")
    parser.add_argument(
        "--async", dest="use_async", action="store_true", help="Use async client"
    )
    return parser.parse_args()


def load_field_data(path):
    with open(path, "r") as f:
        return json.load(f)


def build_options(field_data, context=None, threshold=0.5, page_range=None):
    from datalab_sdk import FormFillingOptions

    kwargs = {"field_data": field_data, "confidence_threshold": threshold}
    if context:
        kwargs["context"] = context
    if page_range:
        kwargs["page_range"] = page_range
    return FormFillingOptions(**kwargs)


def default_output_path(form_path):
    base, ext = os.path.splitext(os.path.basename(form_path))
    return f"filled_{base}{ext}"


def print_result_summary(result):
    print(f"Success: {result.success}")
    print(f"Status: {result.status}")
    print(f"Output format: {result.output_format}")
    print(f"Pages processed: {result.page_count}")
    print(f"Fields filled: {result.fields_filled}")
    if result.fields_not_found:
        print(f"Fields not found: {result.fields_not_found}")


def fill_sync(form, options, output_path):
    from datalab_sdk import DatalabClient

    # Explicitly pass API key to avoid environment loading issues
    api_key = os.getenv("DATALAB_API_KEY")
    if not api_key:
        print("Error: DATALAB_API_KEY not found. Set it in .env or as environment variable.", file=sys.stderr)
        sys.exit(1)

    client = DatalabClient(api_key=api_key)
    is_url = form.startswith("http://") or form.startswith("https://")
    if is_url:
        result = client.fill(file_url=form, options=options)
    else:
        result = client.fill(form, options=options)
    print_result_summary(result)
    result.save_output(output_path)
    print(f"Saved to: {output_path}")
    return result


async def fill_async(form, options, output_path):
    from datalab_sdk import AsyncDatalabClient

    # Explicitly pass API key to avoid environment loading issues
    api_key = os.getenv("DATALAB_API_KEY")
    if not api_key:
        print("Error: DATALAB_API_KEY not found. Set it in .env or as environment variable.", file=sys.stderr)
        sys.exit(1)

    async with AsyncDatalabClient(api_key=api_key) as client:
        is_url = form.startswith("http://") or form.startswith("https://")
        if is_url:
            result = await client.fill(file_url=form, options=options)
        else:
            result = await client.fill(form, options=options)
        print_result_summary(result)
        result.save_output(output_path)
        print(f"Saved to: {output_path}")
        return result


def main():
    args = parse_args()
    field_data = load_field_data(args.field_data)
    options = build_options(field_data, args.context, args.threshold, args.page_range)
    output_path = args.output or default_output_path(args.form)

    try:
        if args.use_async:
            asyncio.run(fill_async(args.form, options, output_path))
        else:
            fill_sync(args.form, options, output_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
