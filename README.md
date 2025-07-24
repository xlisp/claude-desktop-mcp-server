# Claude Desktop MCP Server

![](./demo3.png)

![](./demo1.png)
![](./demo2.png)

## config: 
/Users/clojure/Library/Application\ Support/Claude/claude_desktop_config.json 

```json

{
  "mcpServers": {
    "weather": {
      "command": "/Users/clojure/Desktop/quickstart-resources/weather-server-python/.venv/bin/python",
      "args": [
        "/Users/clojure/Desktop/quickstart-resources/weather-server-python/weather.py"
      ]
    }
  }
}
```

change config file , need ` pkill -f "Claude"  ` then restart Claude desktop

## run mcp server:

```
➜  weather-server-python git:(main) ✗ pwd
/Users/clojure/Desktop/quickstart-resources/weather-server-python
➜  weather-server-python git:(main) ✗ ls
README.md      pyproject.toml uv.lock        weather.py
➜  weather-server-python git:(main) ✗ source .venv/bin/activate

(weather-server-python) ➜  weather-server-python git:(main) ✗ uv add "mcp[cli]" httpx

Resolved 36 packages in 1ms
Installed 34 packages in 64ms
 + annotated-types==0.7.0
 + anyio==4.9.0
 + attrs==25.3.0
 + certifi==2025.7.14
 + click==8.2.1
 + exceptiongroup==1.3.0
 + h11==0.16.0
 + httpcore==1.0.9
 + httpx==0.28.1
 + httpx-sse==0.4.1
 + idna==3.10
 + jsonschema==4.25.0
 + jsonschema-specifications==2025.4.1
 + markdown-it-py==3.0.0
 + mcp==1.12.1
 + mdurl==0.1.2
 + pydantic==2.11.7
 + pydantic-core==2.33.2
 + pydantic-settings==2.10.1
 + pygments==2.19.2
 + python-dotenv==1.1.1
 + python-multipart==0.0.20
 + referencing==0.36.2
 + rich==14.0.0
 + rpds-py==0.26.0
 + shellingham==1.5.4
 + sniffio==1.3.1
 + sse-starlette==2.4.1
 + starlette==0.47.2
 + typer==0.16.0
 + typing-extensions==4.14.1
 + typing-inspection==0.4.1
 + uvicorn==0.35.0
 + weather==0.1.0 (from file:///Users/clojure/Desktop/quickstart-resources/weather-server-python)
(weather-server-python) ➜  weather-server-python git:(main) ✗ 
(weather-server-python) ➜  weather-server-python git:(main) ✗ uv run weather.py

```

* test mcp is work fine:

```
➜  ~ echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}' | uv --directory /Users/clojure/Desktop/quickstart-resources/weather-server-python run weather.py


{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"experimental":{},"prompts":{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":false}},"serverInfo":{"name":"weather","version":"1.12.1"}}}
➜  ~ 
➜  ~ 

```

## FAQ:

check mcp server log

* use full env python path:

```
2025-07-23T15:09:15.405Z [weather] [info] Server started and connected successfully { metadata: undefined }
2025-07-23T15:09:15.427Z [weather] [info] Message from client: {"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"claude-ai","version":"0.1.0"}},"jsonrpc":"2.0","id":0} { metadata: undefined }
Traceback (most recent call last):
  File "/Users/clojure/Desktop/quickstart-resources/weather-server-python/weather.py", line 2, in <module>
    import httpx
ModuleNotFoundError: No module named 'httpx'
2025-07-23T15:09:15.487Z [weather] [info] Server transport closed { metadata: undefined }
2025-07-23T15:09:15.487Z [weather] [info] Client transport closed { metadata: undefined }
```

* use full uv cmd
```
uv not found ...
```

## File System Mcp Server

```

(weather-server-python) ➜  weather-server-python git:(main) ✗ uv run filesystem.py 


➜  weather-server-python git:(main) ✗ echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}' | uv --directory /Users/clojure/Desktop/quickstart-resources/weather-server-python run filesystem.py 

{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"experimental":{},"prompts":{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":false}},"serverInfo":{"name":"filesystem-command","version":"1.12.1"}}}
➜  weather-server-python git:(main) ✗ 

```
