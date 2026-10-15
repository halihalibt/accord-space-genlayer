"""Narrow test-only correction for gltest 0.29.2's text-response mock.

The released mock auto-json-decodes strings even with response_format='text'.
The actual pinned SDK declares text mode -> str. Preserve raw mocked text here
so strict duplicate-key parsing is tested; do not modify installed SDK code.
"""
import pytest


@pytest.fixture(autouse=True)
def preserve_text_mock_response(monkeypatch):
    from gltest.direct import wasi_mock
    original = wasi_mock._handle_llm_request

    def handle(vm, data):
        if data.get("response_format", "text") == "text":
            response = vm._match_llm_mock(data.get("prompt", ""))
            if response is not None:
                return {"ok": response}
        return original(vm, data)

    monkeypatch.setattr(wasi_mock, "_handle_llm_request", handle)
