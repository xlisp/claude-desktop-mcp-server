我将根据您提供的MCP服务器代码创建一个对应的MCP客户端，支持自定义OpenAI API地址。​​​​​​​​​​​​​​​​

我已经为您创建了一个完整的MCP客户端，它可以与您的天气服务器进行交互，并支持自定义OpenAI API地址。以下是主要特性：

## 主要功能

1. **自定义OpenAI API地址** - 支持使用任何兼容OpenAI格式的API服务
1. **MCP工具集成** - 自动连接到您的天气服务器并获取可用工具
1. **智能对话** - 使用OpenAI的函数调用功能自动调用合适的工具
1. **配置管理** - 支持配置文件和交互式配置

## 使用方法

### 1. 安装依赖

```bash
pip install openai httpx mcp
```

### 2. 基本使用

```python
# 修改配置
OPENAI_API_KEY = "your-api-key"
OPENAI_BASE_URL = "https://api.openai.com/v1"  # 或您的自定义API地址
```

### 3. 创建配置文件（可选）

创建 `config.json`：

```json
{
    "openai_api_key": "your-api-key",
    "openai_base_url": "https://your-custom-api.com/v1",
    "model": "gpt-4",
    "mcp_server_path": "weather_server.py"
}
```

## 核心特性

- **工具自动映射** - 自动将MCP工具转换为OpenAI函数调用格式
- **错误处理** - 完善的异常处理和日志记录
- **异步支持** - 全异步设计，性能优秀
- **交互式界面** - 支持命令行交互
- **灵活配置** - 支持多种配置方式

## 示例查询

客户端可以处理以下类型的查询：

- “查询加州的天气警报”
- “获取纽约市的天气预报（纬度40.7128，经度-74.0060）”
- “德州有没有天气警报？”

客户端会自动理解用户意图，调用相应的MCP工具（`get_alerts` 或 `get_forecast`），并将结果以自然语言形式返回给用户。

您只需要将您的天气服务器脚本保存为 `weather_server.py`，然后运行客户端即可开始使用！​​​​​​​​​​​​​​​​