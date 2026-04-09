# Smoke Tests

## Purpose

The smoke-test scripts validate that your endpoint accepts OpenAI-compatible chat requests before you run a full benchmark.

Available scripts:

- `test.py`
- `test-qwen3-8b.py`

## Environment

Set:

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`

Both smoke tests use the synchronous `OpenAI` client and print the raw completion JSON plus the assistant response.

## Commands

Run the default smoke test:

```bash
uv run python test.py
```

Run the Qwen model smoke test:

```bash
uv run python test-qwen3-8b.py
```

## When to Use These

- Before a new benchmark run against a fresh endpoint
- After changing model names or base URLs
- When the evaluator fails and you need to separate connectivity issues from benchmark logic

## What Success Looks Like

A successful run prints:

- The serialized completion payload
- The assistant's answer to the sample algebra question

If the script fails before that point, verify credentials, base URL format, model name compatibility, and provider support for the chat-completions API.
