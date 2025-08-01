
## init

```
python -m venv .venv

source .venv/bin/activate

pip install langchain-mcp-adapters langgraph "langchain[openai]"
```

## MCP server
```
langchain-mcp  main @ python math_server.py

```

## MCP client

```
(.venv) ➜  langchain-mcp git:(main) ✗ python mcp_client.py
Processing request of type ListToolsRequest
Processing request of type CallToolRequest
Processing request of type CallToolRequest
Agent Response: {'messages': [HumanMessage(content="what's (3 + 5) x 12?", additional_kwargs={}, response_metadata={}, id='03c92d76-ca88-4b59-a142-3fce93a63969'), AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_mI85VgtajSNCcFtgmcTKTpfH', 'function': {'arguments': '{"a": 3, "b": 5}', 'name': 'add'}, 'type': 'function', 'index': 0}, {'id': 'call_tUvEPEalcukfdChDHPXRcV7Z', 'function': {'arguments': '{"a": 8, "b": 12}', 'name': 'multiply'}, 'type': 'function', 'index': 1}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 50, 'prompt_tokens': 77, 'total_tokens': 127, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_name': 'openai/gpt-4o', 'system_fingerprint': 'fp_a288987b44', 'id': 'gen-1754034597-GBfScY8g1FEP35L7F8eK', 'service_tier': None, 'finish_reason': 'tool_calls', 'logprobs': None}, id='run--6890f57d-15fd-4558-a345-c16cc4a3c293-0', tool_calls=[{'name': 'add', 'args': {'a': 3, 'b': 5}, 'id': 'call_mI85VgtajSNCcFtgmcTKTpfH', 'type': 'tool_call'}, {'name': 'multiply', 'args': {'a': 8, 'b': 12}, 'id': 'call_tUvEPEalcukfdChDHPXRcV7Z', 'type': 'tool_call'}], usage_metadata={'input_tokens': 77, 'output_tokens': 50, 'total_tokens': 127, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}), ToolMessage(content='8', name='add', id='9346037f-d1c3-4ac4-82da-a974a14a9882', tool_call_id='call_mI85VgtajSNCcFtgmcTKTpfH'), ToolMessage(content='96', name='multiply', id='6c718f01-9af3-4fa1-a410-2b94255cf6ea', tool_call_id='call_tUvEPEalcukfdChDHPXRcV7Z'), AIMessage(content='The result of \\((3 + 5) \\times 12\\) is 96.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 21, 'prompt_tokens': 143, 'total_tokens': 164, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_name': 'openai/gpt-4o', 'system_fingerprint': 'fp_a288987b44', 'id': 'gen-1754034598-IRhPxKS1h0RdE0V85gqW', 'service_tier': None, 'finish_reason': 'stop', 'logprobs': None}, id='run--941d958c-eb91-4ad6-9779-31746c658bee-0', usage_metadata={'input_tokens': 143, 'output_tokens': 21, 'total_tokens': 164, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}})]}
(.venv) ➜  langchain-mcp git:(main) ✗ 

```
