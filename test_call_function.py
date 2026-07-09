from types import SimpleNamespace

from call_function import call_function


tool_call = SimpleNamespace(
    id="call_123",
    type="function",
    function=SimpleNamespace(
        name="get_files_info",
        arguments='{"directory": "."}',
    ),
)

result = call_function(tool_call, verbose=True)
assert result["role"] == "tool"
assert result["tool_call_id"] == "call_123"
assert "Error:" not in result["content"]

print(result["content"])
